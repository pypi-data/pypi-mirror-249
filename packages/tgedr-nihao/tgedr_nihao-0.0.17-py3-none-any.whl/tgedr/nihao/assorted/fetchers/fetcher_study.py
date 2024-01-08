import asyncio
import collections
import logging
import os
from http import HTTPStatus

import pandas as pd
import tqdm
import http.client
import ssl

# default set low to avoid errors from remote site, such as # 503 - Service Temporarily Unavailable
from pandas import DataFrame


base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FOLDER = f"{base_path}/data"

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000
BONDS = ["0001", "0033"]

logger = logging.getLogger(__name__)


class FetchException(Exception):
    def __init__(self, cause: Exception, msg: str = None):
        self.cause = cause
        self.msg = msg


def get_pickle_file_path(name: str):
    return f"{DATA_FOLDER}/{name.replace(' ', '_')}.pkl"


def store_pickle(data: DataFrame, name: str):
    data.to_pickle(get_pickle_file_path(name))


def read_pickle(name: str):
    return pd.read_pickle(get_pickle_file_path(name))


def is_pickle(name: str):
    return os.path.isfile(get_pickle_file_path(name))


@asyncio.coroutine
def get_bond_info(bond: str, semaphore):
    logger.warning(f"[get_bond_info|in] ({bond})")
    try:
        if is_pickle(bond):
            data = read_pickle(bond)
        else:
            with (yield from semaphore):
                conn = http.client.HTTPSConnection(
                    "synthetic-financial-data.p.rapidapi.com", context=ssl._create_unverified_context()
                )

                headers = {
                    "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
                    "x-rapidapi-host": "synthetic-financial-data.p.rapidapi.com",
                }
                conn.request("GET", "/?asset_class=bond&symbol=0008&size=full", headers=headers)

                res = conn.getresponse()
                str_data = res.read().decode("utf-8")
                dict_data = eval(str_data)
                data = pd.DataFrame(dict_data).transpose()
                loop = asyncio.get_event_loop()
                loop.run_in_executor(None, store_pickle, data, bond)

    except Exception as exc:
        raise FetchException(exc, bond) from exc

    logger.warning(f"[get_bond_info|out] => {data}")
    return data


@asyncio.coroutine
def get_bonds(bonds, verbose, concur_req):
    logger.warning("[get_bonds|in]")
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)

    to_do = [get_bond_info(bond, semaphore) for bond in bonds]
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(bonds))

    for future in to_do_iter:
        try:
            logger.warning("[get_bonds] waiting for bond")
            res = yield from future
            logger.warning("[get_bonds] got bond")
            status = HTTPStatus.OK
        except FetchException as exc:
            cause = exc.cause
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                msg = "*** Error for {}: {}"
                print(msg.format(cause, error_msg))
            status = HTTPStatus.error

        counter[status] += 1
    logger.warning(f"[get_bonds|out] => {counter}")
    return counter


if __name__ == "__main__":
    logger.warning("[main|in]")
    loop = asyncio.get_event_loop()
    coro = get_bonds(BONDS, False, DEFAULT_CONCUR_REQ)
    logger.warning("[main] waiting for bonds")
    counts = loop.run_until_complete(coro)
    logger.warning("[main] got bonds")
    loop.close()
    print(counts)
    logger.warning("[main|out]")
