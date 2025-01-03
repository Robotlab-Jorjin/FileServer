
import asyncio
import datetime
import pathlib

import aiohttp
from typeguard import typechecked

from utils import Base64ToBytes, BytesToBase64, MakeDir

FILE = pathlib.Path(__file__)
DIR = FILE.parents[0]


def ReadFile(path: object, mode):
    ret = None

    with open(path, mode) as f:
        ret = f.read()

    return ret


def WriteFile(path: object, mode, data):
    with open(path, mode) as f:
        f.write(data)


def main1():
    print(f"{FILE=}")
    print(f"{DIR=}")


@typechecked
async def F(pdf_data: bytes):
    file_server_url = "http://jorjinapp.ddns.net:15385"

    url = f"{file_server_url}/convert_pdf_to_jpegs"

    print(f"{url=}")

    pdf = BytesToBase64(pdf_data)

    print(f"{len(pdf)}")

    request_data = {
        "pdf": pdf
    }

    timeout = aiohttp.ClientTimeout(total=datetime.timedelta(hours=1).seconds)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=timeout) as session:
        async with session.get(url, json=request_data, timeout=timeout) as response:
            response_data = await response.json()

    return [Base64ToBytes(jpeg) for jpeg in response_data["jpegs"]]


def main2():

    pdf_data = ReadFile(f"{DIR}/HTT-paper.pdf", "rb")
    jpegs_dir = f"{DIR}/HTT-jpegs"

    jpegs = asyncio.run(F(pdf_data))

    MakeDir(jpegs_dir)

    for page_num, jpeg in enumerate(jpegs):
        WriteFile(f"{jpegs_dir}/page-{page_num:>03}.jpeg", "wb", jpeg)


if __name__ == "__main__":
    main2()
