from typing import Callable, Optional, List

import json
import hashlib
import logging
import os.path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def get_string_hash(s):
    return hashlib.md5(s.strip().encode("utf-8")).hexdigest()


class CachedParallelProcessor(object):
    def __init__(
        self,
        process_func: Callable[[str], str],
        max_retry_cnt: int = 3,
        cache_filename: Optional[str] = None,
    ):
        self.process_func = process_func
        self.max_retry_cnt = max_retry_cnt
        if cache_filename is None:
            logging.warning("cache_filename is not set, using default cache filename")
            cache_filename = "cache.jsonl"
        self.cache_dic = None
        self.dynamic_cache_set = None
        self.cache_filename = cache_filename

    def read_cache(self):
        if not os.path.exists(self.cache_filename):
            open(self.cache_filename, "a").close()
            return {}
        with open(self.cache_filename, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            cache_dic = {item["shash"]: item["result"] for item in lines}
            return cache_dic

    def append_cache(self, data: dict) -> None:
        self.dynamic_cache_set.add(data["shash"])
        with open(self.cache_filename, "a+") as f:
            f.write(json.dumps(data) + "\n")

    def process_one_sample(self, input_str: str) -> None:
        if not isinstance(input_str, str):
            return
        shash = get_string_hash(input_str)
        if shash in self.dynamic_cache_set:
            return
        for _ in range(self.max_retry_cnt):
            try:
                result = self.process_func(input_str)
                if result is None:
                    continue
                self.append_cache({"shash": shash, "result": result})
                break
            except Exception:
                pass

    def run(self, input_lis: List[str], num_threads: int = 10) -> None:
        self.cache_dic = self.read_cache()
        self.dynamic_cache_set = set(self.cache_dic.keys())
        print("Start processing...")
        print(f"{len(self.cache_dic):,} items in cache")
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            list(
                tqdm(
                    executor.map(self.process_one_sample, input_lis),
                    total=len(input_lis),
                )
            )

    def get_result(self, input_lis: List[str]) -> List[str]:
        self.cache_dic = self.read_cache()
        result_lis = [
            self.cache_dic.get(get_string_hash(input_str), "")
            for input_str in input_lis
        ]
        err_cnt = result_lis.count("")
        print(f"Processed Count: {len(result_lis)}, Failed Count: {err_cnt}")
        return result_lis
