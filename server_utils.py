import enum
import functools
import json
import traceback
from http import HTTPStatus

import quart
from typeguard import typechecked

from utils import Base64ToBytes


class ResponseCode(enum.IntEnum):
    Success = 20

    BadRequest = 30

    ConvertFailed = 40


class RequestException(Exception):
    def __init__(self, response):
        self.response = response


def RequestExceptionHandler(func):
    @functools.wraps(func)
    async def Wrap(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RequestException as e:
            print(traceback.format_exc())
            return e.response

    return Wrap


@typechecked
def JsonResponse(status: HTTPStatus, x: object):
    return quart.Response(status=status,
                          mimetype="application/json",
                          content_type="application/json",
                          response=json.dumps(x))


@typechecked
def TypicalResponse(x: object):
    return quart.Response(status=HTTPStatus.OK,
                          mimetype="application/json",
                          content_type="application/json",
                          response=json.dumps(x))


async def GetRequestDataFromRequest(request):
    request_data = await request.get_json()

    if not isinstance(request_data, dict):
        raise RequestException(
            TypicalResponse({"code": ResponseCode.BadRequest}))

    return request_data


@typechecked
def GetFromRequestData(request_data: dict,
                       key: str,
                       type: object,
                       allow_none: bool):
    val = request_data.get(key)

    if (val is None and allow_none) or isinstance(val, type):
        return val

    raise RequestException(
        TypicalResponse({"code": ResponseCode.BadRequest}))


@typechecked
def GetBytesFromRequestData(request_data: dict, key: str, allow_none: bool):
    val = GetFromRequestData(request_data, key, str, allow_none)

    if val is None and allow_none:
        return None

    try:
        return Base64ToBytes(val)
    except:
        raise RequestException(
            TypicalResponse({"code": ResponseCode.BadRequest}))
