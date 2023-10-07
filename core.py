import concurrent.futures
from model import System

db = "database/systems.db"
table = "system"
columns = ["name", "description", "status"]


def get_obj(obj: tuple) -> System:
    return System(obj[0], obj[1], obj[2], obj[3])


def get_objs(objs: list[tuple]) -> list[System]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for obj in objs:
            futures.append(executor.submit(get_obj, obj))
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results
