import base64
import datetime
import os
import sys
import typing

from typeguard import typechecked


@typechecked
def PrintPos(time: datetime.datetime,
             filename: str,
             lineno: int,
             funcname: str):
    timestr = SerializeDatetime(time, True)

    print(f"{timestr}\t{filename}:{lineno}\t\t{funcname}")


def PrintCurPos_():
    time = datetime.datetime.now()
    frame = sys._getframe(2)

    PrintPos(time,
             frame.f_code.co_filename,
             frame.f_lineno,
             frame.f_code.co_name)


def PrintCurPos():
    PrintCurPos_()


def Pause():
    PrintCurPos_()
    input("pause...")


@typechecked
def FetchOne(x: typing.Iterable):
    try:
        return next(iter(x))
    except StopIteration:
        return None


@typechecked
def MakeDir(dir: object):
    os.makedirs(dir, exist_ok=True)


@typechecked
def BytesToBase64(x: typing.Optional[bytes | bytearray]):
    return None if x is None else base64.b64encode(x).decode("utf-8")


@typechecked
def Base64ToBytes(x: typing.Optional[str]):
    return None if x is None else base64.b64decode(x)


@typechecked
def SerializeDatetime(dt: typing.Optional[datetime.datetime], second_precision: bool):
    if dt is None:
        dt = None

    dt = dt.replace(tzinfo=datetime.timezone.utc)

    return dt.strftime("%Y-%m-%d %H:%M:%S") if second_precision else dt.strftime("%Y-%m-%d")


@typechecked
def DeserializeDatetime(dt_str: typing.Optional[str], second_precision: bool):
    return None if dt_str is None else datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S" if second_precision else "%Y-%m-%d")
