import logging
import lamini
from concurrent.futures import ThreadPoolExecutor
from lamini.api.lamini_config import get_config, get_configured_key, get_configured_url
from lamini.api.rest_requests import make_web_request
from lamini.error.error import RateLimitError

logger = logging.getLogger(__name__)

thread_pool = None


class InferenceQueue:
    MAX_GPU_COUNT = 12
    MAX_BATCH_SIZE = 10

    def __init__(
        self, api_key, api_url, config, num_threads=None, num_inputs_per_thread=None
    ):
        self.config = get_config(config)
        self.api_key = api_key or lamini.api_key or get_configured_key(self.config)
        self.api_url = api_url or lamini.api_url or get_configured_url(self.config)
        self.api_prefix = self.api_url + "/v1/"

        self.num_threads = num_threads
        self.num_inputs_per_thread = num_inputs_per_thread
        self.thread_pool = self.create_thread_pool()

    def submit(self, request):
        # Break the request into batches
        batches = self.form_batches(request)

        results = []

        logger.info(
            f"Launching {len(batches)} batches onto the thread pool of size {self.get_max_workers()}"
        )

        for batch in batches:
            # Submit each batch to the thread pool
            results.append(
                self.thread_pool.submit(
                    process_batch, self.api_key, self.api_prefix, batch
                )
            )

        # Wait for all the results to come back
        for result in results:
            result.result()

        # Combine the results and return them
        return self.combine_results(results)

    def combine_results(self, results):
        combined_results = []
        for result_future in results:
            result = result_future.result()
            logger.info(f"inference result: {result}")
            if isinstance(result, list):
                combined_results.extend(result)
            else:
                combined_results.append(result)

        return combined_results

    def create_thread_pool(self):
        global thread_pool
        if thread_pool is None:
            thread_pool = ThreadPoolExecutor(max_workers=self.get_max_workers())

        return thread_pool

    def get_max_workers(self):
        if self.num_threads and isinstance(self.num_threads, int):
            return min(self.MAX_GPU_COUNT, self.num_threads)
        return self.MAX_GPU_COUNT

    def form_batches(self, request):
        batch_size = self.get_batch_size()
        batches = []

        if isinstance(request["prompt"], str):
            batches.append(request)
        else:
            temp_batches = self.batch_items(
                request["prompt"], self.get_max_workers(), batch_size
            )
            for item_batch in temp_batches:
                batch = request.copy()
                batch["prompt"] = item_batch
                batches.append(batch)

        if len(batches) > self.get_max_batch_count():
            raise RateLimitError(
                f"Too many requests, {len(request['prompt'])} >"
                f" {self.get_max_batch_count() * self.get_batch_size()} (max)",
                "RateLimitError",
            )

        return batches

    def batch_items(self, items, threads, batch_size):
        batches = [[] for _ in range(threads)]
        import math

        i_len = len(items)
        num_buckets_needed = math.ceil(i_len / batch_size)
        if num_buckets_needed > threads:
            batches = [[] for _ in range(num_buckets_needed)]
            i = 0
            while items:
                batches[i] = items[:batch_size]
                i += 1
                items = items[batch_size:]

        else:
            i = 0
            num_per_bucket = math.floor(len(items) / threads)
            remainder = len(items) % threads
            for buck_index in range(len(batches)):
                for _ in range(num_per_bucket):
                    batches[buck_index].append(items[i])
                    i += 1
                if remainder:
                    batches[buck_index].append(items[i])
                    remainder -= 1
                    i += 1
        return [b for b in batches if b]

    def get_batch_size(self):
        if self.num_inputs_per_thread and isinstance(self.num_inputs_per_thread, int):
            return min(self.MAX_BATCH_SIZE, self.num_inputs_per_thread)
        return self.MAX_BATCH_SIZE

    def get_max_batch_count(self):
        return 512


def process_batch(key, api_prefix, batch):
    url = api_prefix + "completions"
    result = make_web_request(key, url, "post", batch)
    return result
