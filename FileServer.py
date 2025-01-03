import asyncio
import io
import pathlib
import traceback
from dataclasses import dataclass
from http import HTTPMethod

import hypercorn
import pdf2image
import quart

from server_utils import (GetFromRequestData, GetRequestDataFromRequest,
                          RequestExceptionHandler, ResponseCode,
                          TypicalResponse)
from utils import Base64ToBytes, BytesToBase64, PrintCurPos

FILE = pathlib.Path(__file__)
DIR = FILE.parents[0]


class FileServer:
    @dataclass
    class Config:
        pass

    def __init__(self, config: Config):
        pass

    def PDFToJPEGs(self, pdf_data: bytes):
        jpegs: list[bytes] = list()

        for img in pdf2image.convert_from_bytes(pdf_data):
            jpeg_bytes = io.BytesIO()
            img.save(jpeg_bytes, format="JPEG")
            jpegs.append(jpeg_bytes.getvalue())

        return jpegs

    @RequestExceptionHandler
    async def View_ConvertPDFToJPEGs(self):
        request_data = await GetRequestDataFromRequest(quart.request)

        pdf_data = GetFromRequestData(
            request_data, "pdf", str, False)

        try:
            jpegs = self.PDFToJPEGs(Base64ToBytes(pdf_data))
        except:
            traceback.print_exc()

            return TypicalResponse({
                "code": ResponseCode.ConvertFailed,
                "jpegs": list(),
            })

        return TypicalResponse({
            "code": ResponseCode.Success,
            "jpegs": [BytesToBase64(jpeg) for jpeg in jpegs],
        })

    def DeployApp(self, app):
        self.app = app

        self.app.add_url_rule(
            "/convert_pdf_to_jpegs",
            methods=[HTTPMethod.GET],
            view_func=self.View_ConvertPDFToJPEGs)


def StartServer():
    config = hypercorn.config.Config()
    config.bind = "jorjinapp.ddns.net:15385"
    # config.certfile = f"{DIR}/file_server_cert.pem"
    # config.keyfile = f"{DIR}/file_server_key.pem"

    file_server = FileServer(FileServer.Config())

    app = quart.Quart("AuthServer")

    file_server.DeployApp(app)

    asyncio.run(hypercorn.asyncio.serve(app, config))


if __name__ == "__main__":
    StartServer()
