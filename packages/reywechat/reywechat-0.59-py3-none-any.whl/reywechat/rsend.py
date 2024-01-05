# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-03 22:53:18
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Send methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Literal, Callable, Optional, NoReturn, overload
from queue import Queue
from reytool.rcomm import get_file_stream_time
from reytool.rnumber import randn
from reytool.rsystem import throw, catch_exc
from reytool.rtime import sleep
from reytool.rwrap import wrap_thread, wrap_exc

from .rwechat import RWeChat


__all__ = (
    "RSend",
)


class RSend(object):
    """
    Rey's `send` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        bandwidth_upstream: float
    ) -> None:
        """
        Build `send` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        bandwidth_upstream : Upload bandwidth, impact send interval, unit Mpbs.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.bandwidth_upstream = bandwidth_upstream
        self.queue: Queue[Dict] = Queue()
        self.handlers: List[Callable[[Dict], Any]] = []
        self.started: Optional[bool] = False

        # Start.
        self._start_sender()


    @wrap_thread
    def _start_sender(self) -> None:
        """
        Start sender, that will sequentially send message in the send queue.
        """

        # Loop.
        while True:

            ## Stop.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Send.
            exc_reports: List[str] = []
            params = self.queue.get()
            try:
                self._send(params)
            except:
                exc_report, *_ = catch_exc()
                exc_reports.append(exc_report)

            ## Handle.
            else:


                ### Define.
                def handle_handler_exception() -> None:
                    """
                    Handle Handler exception.
                    """

                    # Catch exception.
                    exc_report, *_ = catch_exc()

                    # Save.
                    exc_reports.append(exc_report)


                for handler in self.handlers:
                    wrap_exc(
                        handler,
                        params,
                        _handler=handle_handler_exception,
                    )

            ## Log.
            self.rwechat.rlog.log_send(params, exc_reports)


    def _send(
        self,
        params: Any
    ) -> None:
        """
        Send message.

        Parameters
        ----------
        params : Send parameters.
        """

        # Get parameter.
        send_type: str = params["send_type"]
        receive_id: str = params["receive_id"]

        # Send.

        ## Text.
        if send_type == "text":
            self.rwechat.rclient.send_text(
                receive_id,
                params["text"]
            )

        ## Text with "@".
        elif send_type == "at":
            self.rwechat.rclient.send_text_at(
                receive_id,
                params["user_id"],
                params["text"]
            )

        ## File.
        elif send_type == "file":
            self.rwechat.rclient.send_file(
                receive_id,
                params["path"]
            )

        ## Image.
        elif send_type == "image":
            self.rwechat.rclient.send_image(
                receive_id,
                params["path"]
            )

        ## Emotion.
        elif send_type == "emotion":
            self.rwechat.rclient.send_emotion(
                receive_id,
                params["path"]
            )

        ## Pat.
        elif send_type == "pat":
            self.rwechat.rclient.send_pat(
                receive_id,
                params["user_id"]
            )

        ## Public account.
        elif send_type == "public":
            self.rwechat.rclient.send_public(
                receive_id,
                params["page_url"],
                params["title"],
                params["text"],
                params["image_url"],
                params["public_name"],
                params["public_id"]
            )

        ## Forward.
        elif send_type == "forward":
            self.rwechat.rclient.send_forward(
                receive_id,
                params["message_id"]
            )

        ## Raise.
        else:
            throw(ValueError, send_type)

        # Wait.
        self._wait(params)


    def _wait(
        self,
        params: Any
    ) -> None:
        """
        Waiting after sending.

        Parameters
        ----------
        params : Send parameters.
        """

        # Get parameter.
        send_type: str = params["send_type"]
        seconds = randn(0.8, 1.2, precision=2)

        ## File.
        if send_type in (
            "file",
            "image",
            "emotion"
        ):
            stream_time = get_file_stream_time(params["path"], self.bandwidth_upstream)
            if stream_time > seconds:
                seconds = stream_time

        sleep(seconds)


    @overload
    def send(
        self,
        send_type: Literal[
            "text",
            "at",
            "file",
            "image",
            "emotion",
            "pat",
            "public",
            "forward"
        ],
        receive_id: str,
        **params: Dict[str, Any]
    ) -> None: ...

    @overload
    def send(
        self,
        send_type: Any,
        receive_id: str,
        **params: Dict[str, Any]
    ) -> NoReturn: ...

    def send(
        self,
        send_type: Literal[
            "text",
            "at",
            "file",
            "image",
            "emotion",
            "pat",
            "public",
            "forward"
        ],
        receive_id: str,
        **params: Dict[str, Any]
    ) -> None:
        """
        Put parameters into the send queue.

        Parameters
        ----------
        send_type : Send type.
            - `Literal['text']` : Send text message, use `RClient.send_text` method.
            - `Literal['at']` : Send text message with `@`, use `RClient.send_text_at` method.
            - `Literal['file']` : Send file message, use `RClient.send_file` method.
            - `Literal['image']` : Send image message, use `RClient.send_image` method.
            - `Literal['emotion']` : Send emotion message, use `RClient.send_emotion` method.
            - `Literal['pat']` : Send pat message, use `RClient.send_pat` method.
            - `Literal['public']` : Send public account message, use `RClient.send_public` method.
            - `Literal['forward']` : Forward message, use `RClient.send_forward` method.

        receive_id : User ID or chat room ID of receive message.
        params : Send parameters.
        """

        # Check parameter.
        if send_type not in (
            "text",
            "at",
            "file",
            "image",
            "emotion",
            "pat",
            "public",
            "forward"
        ):
            throw(ValueError, send_type)

        # Set parameters.
        params = {
            "send_type": send_type,
            "receive_id": receive_id,
            **params
        }

        # Put.
        self.queue.put(params)


    def start(self) -> None:
        """
        Start sender.
        """

        # Start.
        self.started = True

        # Report.
        print("Start sender.")


    def stop(self) -> None:
        """
        Stop sender.
        """

        # Stop.
        self.started = False

        # Report.
        print("Stop sender.")


    def end(self) -> None:
        """
        End sender.
        """

        # End.
        self.started = None

        # Report.
        print("End sender.")


    __call__ = send


    __del__ = end