# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Optional, Final
from os.path import abspath as os_abspath
from reytool.rdatabase import RDatabase as RRDatabase
from reytool.ros import create_folder as reytool_create_folder
from reytool.rtime import sleep


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.

    Will start client API service with port `19088` and message callback service with port '19089'.

    Warnings, only applicable to WeChat clients with version `3.9.5.81`.

    Warnings, must close file automatic file download.
    """

    # Environment.
    client_version: Final[str] = "3.9.5.81"
    client_api_port: Final[int] = 19088
    message_callback_port: Final[int] = 19089


    def __init__(
        self,
        rrdatabase: Optional[RRDatabase] = None,
        max_receiver: int = 2
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        """

        # Import.
        from .rclient import RClient
        from .rdatabase import RDatabase
        from .rlog import RLog
        from .rreceive import RReceiver

        # Create folder.
        self._create_folder()

        # Set attribute.

        ## Instance.
        self.rclient = RClient(self)
        self.rlog = RLog(self)
        self.rreceiver = RReceiver(self, max_receiver)
        if rrdatabase is not None:
            self.rdatabase = RDatabase(self, rrdatabase)

        ## Receive.
        self.receive_add_handler = self.rreceiver.add_handler
        self.receive_start = self.rreceiver.start
        self.receive_stop = self.rreceiver.stop

        ## Database.
        if rrdatabase is not None:
            self.database_start = self.rdatabase.to_all


    def _create_folder(self) -> None:
        """
        Create project standard folders.
        """

        # Set parameter.
        paths = [
            "Log",
            "File"
        ]

        # Create.
        reytool_create_folder(*paths)

        # Set attribute.
        self.log_dir = os_abspath("Log")
        self.file_dir = os_abspath("File")


    def start(self) -> None:
        """
        Start all methods.
        """

        # Start.
        self.database_start()
        self.receive_start()


    def keep(self) -> None:
        """
        Blocking the main thread to keep running.
        """

        # Report.
        print("Keep runing.")

        # Blocking.
        while True:
            sleep(1)


    @property
    def print_colour(self) -> bool:
        """
        Whether print colour.

        Returns
        -------
        Result.
        """

        # Get parameter.
        result = self.rlog.rrlog.print_colour

        return result


    @print_colour.setter
    def print_colour(self, value: bool) -> None:
        """
        Set whether print colour.

        Parameters
        ----------
        value : Set value.
        """

        # Set.
        self.rlog.rrlog.print_colour = value
        self.rlog.rrlog_print.print_colour = value
        self.rlog.rrlog_file.print_colour = value