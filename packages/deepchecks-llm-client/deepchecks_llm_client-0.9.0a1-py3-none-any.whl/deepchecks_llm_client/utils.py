from __future__ import annotations
from datetime import datetime
import functools
import logging
import json
import typing as t
from typing_extensions import ParamSpec, TypeVar
from json import JSONDecodeError
from types import GeneratorType

import httpx

P = ParamSpec("P")
T = TypeVar("T")


def maybe_raise(
        response: httpx.Response,
        expected: t.Union[int, t.Tuple[int, int]] = (200, 299),
        msg: t.Optional[str] = None
) -> httpx.Response:
    """Verify response status and raise an HTTPError if got unexpected status code.

    Parameters
    ==========
    response : Response
        http response instance
    expected : Union[int, Tuple[int, int]] , default (200, 299)
        HTTP status code that is expected to receive
    msg : Optional[str] , default None
        error message to show in case of unexpected status code,
        next template parameters available:
        - status (HTTP status code)
        - reason (HTTP reason message)
        - url (request url)
        - body (response payload if available)
        - error (default error message that will include all previous parameters)

    Returns
    =======
    Response
    """
    status = response.status_code
    url = response.url
    reason = response.content

    error_template = "Error: {status} {reason} url {url}.\nBody:\n{body}"
    client_error_template = "{status} Client Error: {reason} for url: {url}.\nBody:\n{body}"

    server_error_template = (
        "{status} Server Internal Error: {reason} for url: {url}.\n"
        "Please, reach Deepchecks support team for more information about this problem.\n"
        "Body:\n{body}"
    )

    def select_template(status):
        if 400 <= status <= 499:
            return client_error_template
        elif 500 <= status <= 599:
            return server_error_template
        else:
            return error_template

    def process_body():
        try:
            return json.dumps(response.json(), indent=3)
        except JSONDecodeError:
            return

    if isinstance(expected, int) and status != expected:
        body = process_body()
        error = select_template(status).format(status=status, reason=reason, url=url, body=body)
        raise httpx.HTTPStatusError(
            error if msg is None else msg.format(
                status=status,
                reason=reason,
                url=url,
                body=body,
                error=error
            ),
            request=response.request,
            response=response
        )

    if isinstance(expected, (tuple, list)) and not expected[0] <= status <= expected[1]:
        body = process_body()
        error = select_template(status).format(status=status, reason=reason, url=url, body=body)
        raise httpx.HTTPStatusError(
            error if msg is None else msg.format(
                status=status,
                reason=reason,
                url=url,
                body=body,
                error=error
            ),
            request=response.request,
            response=response

        )
    return response


def null_log_filter(record):  # pylint: disable=unused-argument
    return False


def set_verbosity(verbose, logger: logging.Logger):
    if not verbose:
        logger.addFilter(null_log_filter)


class HandleExceptions:
    def __init__(self, logger: logging.Logger, return_self: bool = False):
        self.logger = logger
        self.return_self = return_self

    def __call__(self, original_func: t.Callable[P, T]) -> t.Callable[P, T]:
        return self.wraps(original_func)

    def wraps(self, original_func: t.Callable[..., t.Any]):
        @functools.wraps(original_func)
        def wrapper(*args, **kwargs):
            try:
                return original_func(*args, **kwargs)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                self.logger.error("Deepchecks SDK encountered a problem in %s: %s", original_func.__name__, str(ex))
                if self.return_self:
                    return args[0]
                return None

        return wrapper


class HandleGeneratorExceptions(HandleExceptions):
    def wraps(self, original_func: t.Callable[..., GeneratorType]):
        @functools.wraps(original_func)
        def wrapper(*args, **kwargs):
            try:
                gen = original_func(*args, **kwargs)
                for value in gen:
                    yield value
            except Exception as ex:  # pylint: disable=broad-exception-caught
                self.logger.error("Deepchecks SDK encountered a problem in %s: %s", original_func.__name__, str(ex))
                return None

        return wrapper


def get_timestamp(time: t.Union[datetime, int, None]):
    return int(time.timestamp()) if isinstance(time, datetime) else time
