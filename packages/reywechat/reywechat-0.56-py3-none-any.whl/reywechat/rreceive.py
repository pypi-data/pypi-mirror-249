# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-26 11:18:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Receive methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Literal, Callable, Optional
from queue import Queue
from json import loads as json_loads
from reytool.rcomm import listen_socket
from reytool.ros import RFile, os_exists
from reytool.rregex import search
from reytool.rsystem import catch_exc
from reytool.rtime import sleep
from reytool.rwrap import wrap_thread, wrap_wait, wrap_exc
from reytool.rmultitask import RThreadPool

from .rwechat import RWeChat


__all__ = (
    "RMessage",
    "RReceiver"
)


class RMessage(object):
    """
    Rey's `message` type.
    """


    def __init__(
        self,
        time: int,
        id_: int,
        number: int,
        type_: int,
        display: str,
        data: str,
        user: Optional[str] = None,
        room: Optional[str] = None,
        file:  Optional[Dict[Literal["path", "name"], str]] = None
    ) -> None:
        """
        Build `message` instance.

        Parameters
        ----------
        time : Message timestamp.
        id : Message ID.
        number : Message local number.
        type : Message type.
        display : Message description text.
        data : Message source data.
        user : Message sender user ID.
            - `None` : System message.
            - `str` : User messages.

        room : Message chat room ID.
            - `None` : Private chat.
            - `str` : Chat room chat.

        file : Message file information.
            - `None` : Non file message.
            - `Dict` : File message.
                * `Key 'path'` : File path.
                * `Key 'name'` : File name.
        """

        # Set attribute.
        self.time = time
        self.id = id_
        self.number = number
        self.type = type_
        self.display = display
        self.data = data
        self.user = user
        self.room = room
        self.file = file


    @property
    def params(self) -> Dict[
        Literal[
            "time",
            "id",
            "number",
            "room",
            "user",
            "type",
            "display",
            "data",
            "file"
        ],
        Any
    ]:
        """
        Return parameters dictionary.

        Returns
        -------
        Parameters dictionary.
        """

        # Get parameter.
        params = {
            "time": self.time,
            "id": self.id,
            "number": self.number,
            "room": self.room,
            "user": self.user,
            "type": self.type,
            "display": self.display,
            "data": self.data,
            "file": self.file
        }

        return params


    def __str__(self) -> str:
        """
        Return parameters dictionary in string format.

        Returns
        -------
        Parameters dictionary in string format.
        """

        # Convert.
        params_str = str(self.params)

        return params_str


class RReceiver(object):
    """
    Rey's `receiver` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        max_receiver: int
    ) -> None:
        """
        Build `receiver` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        max_receiver : Maximum number of receivers.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.queue: Queue[RMessage] = Queue()
        self.handlers: List[Callable[[RMessage], Any]] = []
        self.started: Optional[bool] = False

        # Start.
        self._start_callback()
        self._start_receiver(max_receiver)
        self.rwechat.rclient.hook_message(
            "127.0.0.1",
            self.rwechat.message_callback_port,
            60
        )


    @wrap_thread
    def _start_callback(self) -> None:
        """
        Start callback socket.
        """


        # Define.
        def put_queue(data: bytes) -> None:
            """
            Put message data into receive queue.

            Parameters
            ----------
            data : Socket receive data.
            """

            # Decode.
            data: Dict = json_loads(data)

            # Break.
            if "msgId" not in data: return

            # Extract.
            message = RMessage(
                data["createTime"],
                data["msgId"],
                data["msgSequence"],
                data["type"],
                data["displayFullContent"],
                data["content"],
                data["fromUser"]
            )

            # Put.
            self.queue.put(message)


        # Listen socket.
        listen_socket(
            "127.0.0.1",
            self.rwechat.message_callback_port,
            put_queue
        )


    @wrap_thread
    def _start_receiver(
        self,
        max_receiver: int
    ) -> None:
        """
        Create receiver, that will sequentially handle message in the receive queue.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        """


        # Define.
        def handles(message: RMessage) -> None:
            """
            Use handlers to handle message.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Set parameter.
            exc_reports: List[str] = []
            handlers = [
                self._handler_room,
                self._handler_file,
                *self.handlers
            ]


            # Define.
            def handle_handler_exception() -> None:
                """
                Handle Handler exception.
                """

                # Catch exception.
                exc_report, _, _, _ = catch_exc()

                # Save.
                exc_reports.append(exc_report)


            # Default Handle.
            for handler in handlers:
                wrap_exc(
                    handler,
                    message,
                    _handler=handle_handler_exception,
                )

            # Log.
            self.rwechat.rlog.log_receive(
                message,
                exc_reports
            )


        # Thread pool.
        thread_pool = RThreadPool(
            handles,
            _max_workers=max_receiver
        )

        # Loop.
        while True:

            ## Stop.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Submit.
            message = self.queue.get()
            thread_pool(message)


    def add_handler(
        self,
        handler: Callable[[RMessage], Any]
    ) -> None:
        """
        Add message handler function.

        Parameters
        ----------
        handler : Handler method, input parameter is `RMessage` instance.
        """

        # Add.
        self.handlers.append(handler)


    def _handler_room(
        self,
        message: RMessage
    ) -> None:
        """
        Handle room message.
        """

        # Break.
        if (
            message.user.__class__ != str
            or message.user[-9:] != "@chatroom"
        ):
            return

        # Set attribute.
        message.room = message.user
        if ":\n" in message.data:
            user, data = message.data.split(":\n", 1)
            message.user = user
            message.data = data
        else:
            message.user = None


    def _handler_file(
        self,
        message: RMessage
    ) -> None:
        """
        Handle file message.
        """

        # Save.

        ## Image.
        if message.type == 3:
            self.rwechat.rclient.download_file(message.id)
            download_path = "%swxhelper\\image\\%s.dat" % (
                self.rwechat.rclient.login_info["account_data_path"],
                message.id
            )
            file_name = f"{message.id}.jpg"

        ## Voice.
        elif message.type == 34:
            self.rwechat.rclient.download_voice(
                message.id,
                self.rwechat.file_dir
            )
            download_path = "%s\\%s.amr" % (
                self.rwechat.file_dir,
                message.id
            )
            file_name = f"{message.id}.amr"

        ## Vidoe.
        elif message.type == 43:
            self.rwechat.rclient.download_file(message.id)
            download_path = "%swxhelper\\video\\%s.mp4" % (
                self.rwechat.rclient.login_info["account_data_path"],
                message.id
            )
            file_name = f"{message.id}.mp4"

        ## Other.
        elif message.type == 49:

            ## Check.
            pattern = "^.+ : \[文件\](.+)$"
            result = search(pattern, message.display)
            if result is None:
                return
            keyword = "<type>6</type>"
            if keyword not in message.data:
                return

            self.rwechat.rclient.download_file(message.id)
            download_path = "%swxhelper\\file\\%s_%s" % (
                self.rwechat.rclient.login_info["account_data_path"],
                message.id,
                result
            )
            file_name = result

        ## Break.
        else:
            return

        # Wait.
        wrap_wait(
            os_exists,
            download_path,
            _interval = 0.05,
            _timeout=60
        )
        sleep(0.1)

        # Set parameter.
        rfile = RFile(download_path)
        file_path = "%s\\%s" % (
            self.rwechat.file_dir,
            message.id
        )
        rfile.move(file_path)
        file = {
            "path": file_path,
            "name": file_name
        }
        message.file = file


    def start(self) -> None:
        """
        Start receiver.
        """

        # Start.
        self.started = True

        # Report.
        print("Start receive and handle message.")


    def stop(self) -> None:
        """
        Stop receiver.
        """

        # Stop.
        self.started = False

        # Report.
        print("Stop receive and handle message.")


    def end(self) -> None:
        """
        End receiver.
        """

        # End.
        self.started = None

        # Report.
        print("End receive and handle message.")


    __del__ = end