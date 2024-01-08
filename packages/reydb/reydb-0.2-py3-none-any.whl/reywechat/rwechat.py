# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Dict, Literal, Optional, Union, Final
from os.path import abspath as os_abspath
from reydb.rconnection import RDatabase as RRDatabase
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
        rrdatabase: Optional[Union[RRDatabase, Dict[Literal["wechat", "file"], RRDatabase]]] = None,
        max_receiver: int = 2,
        bandwidth_downstream: float = 5,
        bandwidth_upstream: float = 5,
        save_send_file: bool = True
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        rrdatabase : `RDatabase` instance of `reytool` package.
            - `RDatabase` : Set all `RDatabase` instances.
            - `Dict` : Set each `RDatabase` instance, all item is required.
                * `Key is 'wechat'` : `RDatabase` instance used in WeChat methods.
                * `Key is 'file'` : `RDatabase` instance used in file methods.

        max_receiver : Maximum number of receivers.
        bandwidth_downstream : Download bandwidth, impact receive timeout, unit Mpbs.
        bandwidth_upstream : Upload bandwidth, impact send interval, unit Mpbs.
        save_send_file : Whether save send file in the `self.dir_file` directory.
        """

        # Import.
        from .rclient import RClient
        from .rdatabase import RDatabase
        from .rlog import RLog
        from .rreceive import RReceive
        from .rsend import RSend

        # Create folder.
        self._create_folder()

        # Set attribute.

        ## Instance.
        self.rclient = RClient(self)
        self.rlog = RLog(self)
        self.rreceive = RReceive(self, max_receiver, bandwidth_downstream)
        self.rsend = RSend(self, bandwidth_downstream)
        if rrdatabase is not None:
            self.rdatabase = RDatabase(self, rrdatabase)

        ## Receive.
        self.receive_add_handler = self.rreceive.add_handler
        self.receive_start = self.rreceive.start
        self.receive_stop = self.rreceive.stop

        ## Send.
        self.send_add_handler = self.rsend.add_handler
        self.send = self.rsend.send
        self.send_start = self.rsend.start
        self.send_stop = self.rsend.stop

        ## Database.
        if rrdatabase is not None:
            self.database_start = self.rdatabase.start_all


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
        self.dir_log = os_abspath("Log")
        self.dir_file = os_abspath("File")


    def start(self) -> None:
        """
        Start all methods.
        """

        # Start.
        if hasattr(self, "database_start"):
            self.database_start()
        self.receive_start()
        self.send_start()


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