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
            ret = json.dumps({"code": 200, "data": ShareObjects.current_status})
        except Exception as e:
            response.status = 417
            ret = json.dumps({"code": 417, "error": f"{e} {traceback.format_exc()}"})
        return ret

    @staticmethod
    @get('/current')
    def current():
        try:
            response.status = 200
            ret = json.dumps({"code": 200, "data": ShareObjects.history_record_manager.select_latest()})
        except Exception as e:
            response.status = 417
            ret = json.dumps({"code": 417, "error": f"{e} {traceback.format_exc()}"})
        return ret

    @staticmethod
    @get('/history')
    def history():
        """
        /history?page_size=10&page_number=1
        """
        try:
            response.status = 200
            page_size = int(request.query.page_size) if request.query.page_size != "" else 10
            page_number = int(request.query.page_number) if request.query.page_number != "" else 1
            raw = ShareObjects.history_record_manager.select_history(page_size, page_number)
            ret = json.dumps({"code": 200, "data": list(raw)})
        except Exception as e:
            response.status = 417
            ret = json.dumps({"code": 417, "error": f"{e} {traceback.format_exc()}"})
        return ret

    @staticmethod
    @get('/history/html')
    def history():
        """
        /history?page_size=10&page_number=1
        """
        try:
            response.status = 200
            page_size = int(request.query.page_size) if request.query.page_size != "" else 10
            page_number = int(request.query.page_number) if request.query.page_number != "" else 1
            raw = ShareObjects.history_record_manager.select_history(page_size, page_number)
            ret = WebManager.dicts2htmltable(list(raw))
        except Exception as e:
            response.status = 417
            ret = json.dumps({"code": 417, "error": f"{e} {traceback.format_exc()}"})
        return ret

    @staticmethod
    def dicts2htmltable(data):
        html = ''.join(f'<th>{x}</th>' for x in data[0].keys())
        for d in data:
            html += '<tr>' + ''.join(f'<td>{x}</td>' for x in d.values()) + '</tr>'
        return '<table border=1 class="stocktable" id="table1">' + html + '</table>'


