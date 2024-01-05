from rich.console import Console
import time
import json
import uuid
from fastapi import Request, Response
from fastapirichlogger.core.config import settings
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class FastAPIRichLogger(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.console = Console()

    class LogData:
        def __init__(self, status_code, log_id, authorization, content_type, content_length, content_accept, request_method, request_path, execute_time, body, start_time):
            self.status_code = status_code
            self.log_id = log_id
            self.authorization = authorization
            self.content_type = content_type
            self.content_length = content_length
            self.content_accept = content_accept
            self.request_method = request_method
            self.request_path = request_path
            self.start_time = start_time
            self.execute_time = execute_time
            self.body = body
            self.determine_log_level()

        def determine_log_level(self):
            if str(self.status_code)[0] in ["4", "5"]:
                self.level = "Error"
                self.color = "red"
            elif str(self.status_code)[0] in ["3"]:
                self.level = "Warning"
                self.color = "yellow"
            else:
                self.level = "Success"
                self.color = "green"

    async def dispatch(self, request: Request, call_next):
        if settings.debug == "false":
            return await call_next(request)

        headers = self._extract_headers(request)
        start_time = time.time()
        response = await call_next(request)
        elapsed_time = (time.time() - start_time) * 1000

        try:
            response_body = await self._process_response_body(response)
            log_data = self.LogData(
                status_code=response.status_code,
                log_id=headers["log_id"],
                authorization=headers["authorization"],
                content_type=headers["content_type"],
                content_length=headers["content_length"],
                content_accept=headers["content_accept"],
                request_method=request.method,
                request_path=request.url.path,
                execute_time=round(elapsed_time, 3),
                body=response_body,
                start_time=start_time
            )
            self._print_log(log_data)
        except Exception as e:
            self.console.print(f"Error processing log: {e}", style="red")

        return response

    def _extract_headers(self, request):
        return {
            "log_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
            "authorization": request.headers.get("Authorization", None),
            "content_type": request.headers.get("Content-Type", None),
            "content_length": request.headers.get("Content-Length", None),
            "content_accept": request.headers.get("Accept", None),
        }

    async def _process_response_body(self, response):
        body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(body))
        return json.loads(b"".join(body))

    def _print_log(self, log_data):
        request_start_time = time.strftime('%H:%M:%S', time.localtime(log_data.start_time)) + f'.{int((log_data.start_time - int(log_data.start_time)) * 1000):04}'
        request_end_time = time.strftime('%H:%M:%S', time.localtime(time.time())) + f'.{int((time.time() - int(time.time())) * 1000):04}'

        self.console.rule(f"[{log_data.color}]Request Log ID: {log_data.log_id} > {log_data.level} | Status Code: {log_data.status_code} [/]", style=log_data.color)
        self.console.print(f"[white]Method: {log_data.request_method}[/]")
        self.console.print(f"[white]Authorization: {log_data.authorization}[/]")
        self.console.print(f"[white]Content-Type: {log_data.content_type}[/]")
        self.console.print(f"[white]Content-Length: {log_data.content_length}[/]")
        self.console.print(f"[white]Accept: {log_data.content_accept}[/]")
        self.console.print(f"[white]Path: {log_data.request_path}[/]")
        self.console.print("Body:")
        self.console.print(json.dumps(log_data.body, indent=4))
        # self.console.rule(f"[{log_data.color}][/]", style=log_data.color)
        self.console.rule(f"[{log_data.color}]Start: {request_start_time} - End: {request_end_time} - Total Execution Time: {log_data.execute_time} milliseconds[/]")

