# 20250205
import json
import typing
import logging
import traceback
import threading
import dataclasses

from bottle import run, response, get, request

from common.objects import ShareObjects
from utils.logger import get_logger
from utils.config import CONFIG


@dataclasses.dataclass
class ResponseData:
    """返回的结构体"""
    data: typing.Any = None
    code: int = 200
    error: str = ''


class WebManager(threading.Thread):

    _logger: logging.Logger

    def __init__(self):
        super(WebManager, self).__init__(name="WebManager")
        self._logger = get_logger("web")

    def run(self) -> None:
        self._logger.info(f"Start to run {self.name}...")
        run(host=CONFIG.Web.host, port=CONFIG.Web.port)

    @staticmethod
    @get('/health')
    def health():
        try:
            response.status = 200
            ret = json.dumps(ResponseData(data=ShareObjects.current_status, code=200).__dict__)
        except Exception as e:
            response.status = 418
            ret = json.dumps(ResponseData(code=418, error=f"{e} {traceback.format_exc()}").__dict__)
        return ret

    @staticmethod
    @get('/current')
    def current():
        try:
            response.status = 200
            ret = json.dumps(ResponseData(data=ShareObjects.history_record_manager.select_latest().__dict__))
        except Exception as e:
            response.status = 418
            ret = json.dumps(ResponseData(code=418, error=f"{e} {traceback.format_exc()}").__dict__)
        return ret

    @staticmethod
    @get('/history')
    def history():
        """
        /history?page_size=10&page_number=1
        """
        try:
            response.status = 200
            page_size = request.query.page_size
            page_number = request.query.page_number
            ret = json.dumps(ResponseData(
                data=ShareObjects.history_record_manager.select_history(page_size, page_number).__dict__))
        except Exception as e:
            response.status = 418
            ret = json.dumps(ResponseData(code=418, error=f"{e} {traceback.format_exc()}").__dict__)
        return ret

