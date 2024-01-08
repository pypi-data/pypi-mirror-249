# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from typing import Tuple, Dict, Literal, Union, Optional
from os.path import join as os_join
from json import loads as json_loads
from reydb.rconnection import RDatabase as RRDatabase
from reytool.ros import RFile, RFolder
from reytool.rsystem import throw
from reytool.rtime import to_time, time_to, sleep
from reytool.rwrap import wrap_thread

from .rreceive import RMessage
from .rwechat import RWeChat


__all__ = (
    "RDatabase",
)


class RDatabase(object):
    """
    Rey's `database` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        rrdatabase: Union[RRDatabase, Dict[Literal["wechat", "file"], RRDatabase]]
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        rrdatabase : `RDatabase` instance of `reytool` package.
            - `RDatabase` : Set all `RDatabase` instances.
            - `Dict` : Set each `RDatabase` instance, all item is required.
                * `Key is 'wechat'` : `RDatabase` instance used in WeChat methods.
                * `Key is 'file'` : `RDatabase` instance used in file methods.
        """

        # Set attribute.
        self.rwechat = rwechat
        if rrdatabase.__class__ == RRDatabase:
            self.rrdatabase_wechat = self.rrdatabase_file = rrdatabase
        elif rrdatabase.__class__ == dict:
            self.rrdatabase_wechat = rrdatabase.get("wechat")
            self.rrdatabase_file = rrdatabase.get("file")
            if (
                self.rrdatabase_wechat
                or self.rrdatabase_file
            ):
                throw(ValueError, rrdatabase)
        else:
            throw(TypeError, rrdatabase)

        # Build.
        self.build()

        # Start.
        self.to_contact_user()
        self.to_contact_room()
        self.to_contact_room_user()
        self.to_message_receive()
        self.to_message_send()
        self.from_message_send()


    def build(self) -> None:
        """
        Check and build all standard databases and tables.
        """

        # Set parameter.

        ## Database.
        databases = [
            {
                "database": "wechat"
            }
        ]

        ## Table.
        tables = [

            ### "contact_user".
            {
                "path": ("wechat", "contact_user"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "user_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "User ID."
                    },
                    {
                        "name": "user_name",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "User name."
                    },
                    {
                        "name": "is_valid",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Is the valid, 0 is invalid, 1 is valid."
                    }
                ],
                "primary": "user_id",
                "comment": "User contact table."
            },

            ### "contact_room".
            {
                "path": ("wechat", "contact_room"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "room_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room ID."
                    },
                    {
                        "name": "room_name",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room name."
                    },
                    {
                        "name": "is_valid",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Is the valid, 0 is invalid, 1 is valid."
                    }
                ],
                "primary": "room_id",
                "comment": "Chat room contact table."
            },

            ### "contact_room_user".
            {
                "path": ("wechat", "contact_room_user"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "room_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room ID."
                    },
                    {
                        "name": "user_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room user ID."
                    },
                    {
                        "name": "user_name",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room user name."
                    },
                    {
                        "name": "is_valid",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Is the valid, 0 is invalid, 1 is valid."
                    }
                ],
                "primary": ["room_id", "user_id"],
                "comment": "Chat room user contact table."
            },

            ### "message_type".
            {
                "path": ("wechat", "message_type"),
                "fields": [
                    {
                        "name": "message_type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type."
                    },
                    {
                        "name": "description",
                        "type_": "varchar(200)",
                        "constraint": "NOT NULL",
                        "comment": "Message type description."
                    }
                ],
                "primary": "message_type",
                "comment": "Message type table."
            },

            ### "message_receive".
            {
                "path": ("wechat", "message_receive"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "message_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "Message time."
                    },
                    {
                        "name": "message_id",
                        "type_": "bigint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message UUID."
                    },
                    {
                        "name": "room_id",
                        "type_": "char(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message chat room ID, null for private chat."
                    },
                    {
                        "name": "user_id",
                        "type_": "varchar(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message sender user ID, null for system message."
                    },
                    {
                        "name": "message_type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type."
                    },
                    {
                        "name": "data",
                        "type_": "text",
                        "constraint": "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL",
                        "comment": "Message data."
                    },
                    {
                        "name": "file_id",
                        "type_": "mediumint unsigned",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message file ID, from the file database."
                    }
                ],
                "primary": "message_id",
                "indexes": [
                    {
                        "name": "n_message_time",
                        "fields": "message_time",
                        "type": "noraml",
                        "comment": "Message time normal index."
                    },
                    {
                        "name": "n_room_id",
                        "fields": "room_id",
                        "type": "noraml",
                        "comment": "Message chat room ID normal index."
                    },
                    {
                        "name": "n_user_id",
                        "fields": "user_id",
                        "type": "noraml",
                        "comment": "Message sender user ID normal index."
                    }
                ],
                "comment": "Message receive table."
            },

            ### "message_send".
            {
                "path": ("wechat", "message_send"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "plan_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL",
                        "comment": "Send plan time."
                    },
                    {
                        "name": "send_id",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL AUTO_INCREMENT",
                        "comment": "Send self increase ID."
                    },
                    {
                        "name": "send_state",
                        "type_": "tinyint unsigned",
                        "constraint": "NOT NULL",
                        "comment": (
                            "Send state, "
                            "0 is not sent, "
                            "1 is handling, "
                            "2 is send success, "
                            "3 is send fail, "
                            "4 is send cancel."
                        )
                    },
                    {
                        "name": "send_type",
                        "type_": "tinyint unsigned",
                        "constraint": "NOT NULL",
                        "comment": (
                            "Send type, "
                            "0 is text message, "
                            "1 is text message with \"@\", "
                            "2 is file message, "
                            "3 is image message, "
                            "4 is emoticon message, "
                            "5 is pat message, "
                            "6 is public account message, "
                            "7 is forward message."
                        )
                    },
                    {
                        "name": "receive_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Receive to user ID or chat room ID."
                    },
                    {
                        "name": "parameters",
                        "type_": "json",
                        "constraint": "NOT NULL",
                        "comment": (
                            "Send parameters, "
                            "when parameter \"file_id\" exists, then download file and convert to parameter \"path\"."
                        )
                    }
                ],
                "primary": "send_id",
                "indexes": [
                    {
                        "name": "n_update_time",
                        "fields": "update_time",
                        "type": "noraml",
                        "comment": "Record update time normal index."
                    },
                    {
                        "name": "n_receive_id",
                        "fields": "receive_id",
                        "type": "noraml",
                        "comment": "Receive to user ID or chat room ID normal index."
                    }
                ],
                "comment": "Message send table."
            }
        ]

        # Build.

        ## WeChat.
        self.rrdatabase_wechat.build.build(databases, tables)

        ## File.
        self.rrdatabase_file.file.build()

        # Update.
        self.update_message_type()
        self.update_contact_user()
        self.update_contact_room()
        self.update_contact_room_user()


    def update_message_type(self) -> None:
        """
        Update table `message_type`.
        """

        # Generate data.
        data = [
            {"message_type": 1, "description": "text message"},
            {"message_type": 3, "description": "image message"},
            {"message_type": 34, "description": "voice message"},
            {"message_type": 37, "description": "new friend"},
            {"message_type": 42, "description": "business card"},
            {"message_type": 43, "description": "video message"},
            {"message_type": 47, "description": "emoticon message"},
            {"message_type": 48, "description": "position message"},
            {"message_type": 49, "description": "file or quote or forward or share link or transfer money or real time location message"},
            {"message_type": 1000, "description": "system message"},
            {"message_type": 1002, "description": "recall message"}
        ]

        # Insert.
        self.rrdatabase_wechat.execute_insert(
            ("wechat", "message_type"),
            data,
            "update"
        )


    def update_contact_user(self) -> None:
        """
        Update table `contact_user`.
        """

        # Get data.
        contact_table = self.rwechat.rclient.get_contact_table("user")

        user_data = [
            {
                "user_id": row["id"],
                "user_name": row["name"],
                "is_valid": 1
            }
            for row in contact_table
        ]
        user_ids = [
            row["id"]
            for row in contact_table
        ]

        # Insert and update.
        conn = self.rrdatabase_wechat.connect()

        ## Insert.
        if contact_table != []:
            conn.execute_insert(
                ("wechat", "contact_user"),
                user_data,
                "update"
            )

        ## Update.
        if user_ids == []:
            sql = (
                "UPDATE `wechat`.`contact_user`\n"
                "SET `is_valid` = 0"
            )
        else:
            sql = (
                "UPDATE `wechat`.`contact_user`\n"
                "SET `is_valid` = 0\n"
                "WHERE `user_id` NOT IN :user_ids"
            )
        conn.execute(
            sql,
            user_ids=user_ids
        )

        ## Commit.
        conn.commit()

        ## Close.
        conn.close()


    def update_contact_room(self) -> None:
        """
        Update table `contact_room`.
        """

        # Get data.
        contact_table = self.rwechat.rclient.get_contact_table("room")

        room_data = [
            {
                "room_id": row["id"],
                "room_name": row["name"],
                "is_valid": 1
            }
            for row in contact_table
        ]
        room_ids = [
            row["id"]
            for row in contact_table
        ]

        # Insert and update.
        conn = self.rrdatabase_wechat.connect()

        ## Insert.
        if contact_table != []:
            conn.execute_insert(
                ("wechat", "contact_room"),
                room_data,
                "update"
            )

        ## Update.
        if room_ids == []:
            sql = (
                "UPDATE `wechat`.`contact_room`\n"
                "SET `is_valid` = 0"
            )
        else:
            sql = (
                "UPDATE `wechat`.`contact_room`\n"
                "SET `is_valid` = 0\n"
                "WHERE `room_id` NOT IN :room_ids"
            )
        conn.execute(
            sql,
            room_ids=room_ids
        )

        ## Commit.
        conn.commit()

        ## Close.
        conn.close()


    def update_contact_room_user(
        self,
        room_id: Optional[str] = None
    ) -> None:
        """
        Update table `contact_room_user`.

        Parameters
        ----------
        room_id : Chat room ID.
            - `None` : Update all chat room.
            - `str` : Update this chat room.
        """

        # Get data.

        ## All.
        if room_id is None:
            contact_table = self.rwechat.rclient.get_contact_table("room")

        ## Given.
        else:
            contact_table = [{"id": room_id}]

        room_user_data = [
            {
                "room_id": row["id"],
                "user_id": user_id,
                "user_name": user_name,
                "is_valid": 1
            }
            for row in contact_table
            for user_id, user_name
            in self.rwechat.rclient.get_room_member_table(row["id"]).items()
        ]
        room_user_ids = [
            "%s,%s" % (
                row["room_id"],
                row["user_id"]
            )
            for row in room_user_data
        ]

        # Insert and update.
        conn = self.rrdatabase_wechat.connect()

        ## Insert.
        if contact_table != []:
            conn.execute_insert(
                ("wechat", "contact_room_user"),
                room_user_data,
                "update"
            )

        ## Update.
        if room_user_ids == []:
            sql = (
                "UPDATE `wechat`.`contact_room_user`\n"
                "SET `is_valid` = 0"
            )
        elif room_id is None:
            sql = (
                "UPDATE `wechat`.`contact_room_user`\n"
                "SET `is_valid` = 0\n"
                "WHERE CONCAT(`room_id`, ',', `user_id`) NOT IN :room_user_ids"
            )
        else:
            sql = (
                "UPDATE `wechat`.`contact_room_user`\n"
                "SET `is_valid` = 0\n"
                "WHERE (\n"
                "    `room_id` = :room_id\n"
                "    AND CONCAT(`room_id`, ',', `user_id`) NOT IN :room_user_ids\n"
                ")"
            )
        conn.execute(
            sql,
            room_user_ids=room_user_ids,
            room_id=room_id
        )

        ## Commit.
        conn.commit()

        ## Close.
        conn.close()


    def to_contact_user(self) -> None:
        """
        Add handler, write record to table `contact_user`.
        """


        # Define.
        def handler_to_contact_user(message: RMessage) -> None:
            """
            Write record to table `contact_user`.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Break.
            if message.type != 10000: return

            # Add friend.
            if (
                message.data == "以上是打招呼的内容"
                or message.data[:5] == "你已添加了"
            ):

                ## Generate data.
                user_name = self.rwechat.rclient.get_contact_name(message.user)
                data = {
                    "user_id": message.user,
                    "user_name": user_name,
                    "is_valid": 1
                }

                ## Insert.
                self.rrdatabase_wechat.execute_insert(
                    ("wechat", "contact_user"),
                    data,
                    "update"
                )


        # Add handler.
        self.rwechat.rreceive.add_handler(handler_to_contact_user)


    def to_contact_room(self) -> None:
        """
        Add handler, write record to table `contact_room`.
        """


        # Define.
        def handler_to_contact_room(message: RMessage) -> None:
            """
            Write record to table `contact_room`.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Break.
            if message.type != 10000: return

            # Invite.
            if (
                "邀请你和" in message.data[:38]
                or "邀请你加入了群聊" in message.data[:42]
            ):

                ## Generate data.
                room_name = self.rwechat.rclient.get_contact_name(message.room)
                data = {
                    "room_id": message.room,
                    "room_name": room_name,
                    "is_valid": 1
                }

                ## Insert.

                ### "contact_room".
                self.rrdatabase_wechat.execute_insert(
                    ("wechat", "contact_room"),
                    data,
                    "update"
                )

                ### "contact_room_user".
                self.update_contact_room_user(message.room)

            # Modify room name.
            elif "修改群名为“" in message.data[:40]:

                ## Generate data.
                _, room_name = message.data.rsplit("“", 1)
                room_name = room_name[:-1]
                if room_name == "":
                    room_name = "群聊"
                data = {
                    "room_id": message.room,
                    "room_name": room_name
                }

                ## Update.
                self.rrdatabase_wechat.execute_update(
                    ("wechat", "contact_room"),
                    data
                )

            elif (

                # Kick out.
                (
                    message.data[:2] == "你被"
                    and message.data[-4:] == "移出群聊"
                )

                # Dissolve.
                or (
                    message.data[:2] == "群主"
                    and message.data[-6:] == "已解散该群聊"
                )
            ):

                ## Generate data.
                data = {
                    "room_id": message.room,
                    "is_valid": 0
                }

                ## Update.
                self.rrdatabase_wechat.execute_update(
                    ("wechat", "contact_room"),
                    data
                )


        # Add handler.
        self.rwechat.rreceive.add_handler(handler_to_contact_room)


    def to_contact_room_user(self) -> None:
        """
        Add handler, write record to table `contact_room_user`.
        """


        # Define.
        def handler_to_contact_room_user(message: RMessage) -> None:
            """
            Write record to table `contact_room_user`.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Break.
            if message.type != 10000: return

            # Add memeber.
            if (
                "邀请\"" in message.data[:37]
                and message.data[-6:] == "\"加入了群聊"
            ):

                ## Sleep.
                sleep(1)

                ## Insert.
                self.update_contact_room_user(message.room)


        # Add handler.
        self.rwechat.rreceive.add_handler(handler_to_contact_room_user)


    def to_message_receive(self) -> None:
        """
        Add handler, write record to table `message_receive`.
        """


        # Define.
        def handler_to_message_receive(message: RMessage) -> None:
            """
            Write record to table `message_receive`.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Upload file.
            if message.file is None:
                file_id = None
            else:
                file_id = self.rrdatabase_file.file.upload(
                    message.file["path"],
                    message.file["name"],
                    "WeChat"
                )

            # Generate data.
            message_time_obj = to_time(message.time)
            message_time_str = time_to(message_time_obj)
            data = {
                "message_time": message_time_str,
                "message_id": message.id,
                "room_id": message.room,
                "user_id": message.user,
                "message_type": message.type,
                "data": message.data,
                "file_id": file_id
            }

            # Insert.
            self.rrdatabase_wechat.execute_insert(
                ("wechat", "message_receive"),
                data,
                "ignore"
            )


        # Add handler.
        self.rwechat.rreceive.add_handler(handler_to_message_receive)


    def to_message_send(self) -> None:
        """
        Add handler, write record to table `message_send`.
        """


        # Define.
        def handler_to_message_send(
            params: Dict,
            success: bool
        ) -> None:
            """
            Write record to table `message_send`.

            Parameters
            ----------
            params : Send parameters.
            success : Whether the sending was successful.
            """

            # Break.
            is_from_db: Optional[bool] = params.get("is_from_db")
            if is_from_db is True: return

            # Generate data.
            send_type = params["send_type"]
            receive_id = params["receive_id"]
            path = params.get("path")
            params = {
                key: value
                for key, value in params.items()
                if key not in (
                    "send_type",
                    "receive_id",
                    "path"
                )
            }

            ## Upload file.
            if path is not None:
                file_id = self.rrdatabase_file.file.upload(
                    path,
                    note="WeChat"
                )
                params["file_id"] = file_id

            if success:
                send_state = 2
            else:
                send_state = 3
            data = {
                "send_state": send_state,
                "send_type": send_type,
                "receive_id": receive_id,
                "parameters": params
            }

            # Insert.
            self.rrdatabase_wechat.execute_insert(
                ("wechat", "message_send"),
                data
            )


        # Add handler.
        self.rwechat.rsend.add_handler(handler_to_message_send)


    def _download_file(
        self,
        file_id: int
    ) -> Tuple[str, str]:
        """
        Download file by ID.

        Parameters
        ----------
        file_id : File ID.

        Returns
        -------
        File save path and file name.
        """

        # Select.
        file_info = self.rrdatabase_file.file.query(file_id)

        # Check.
        file_md5 = file_info["md5"]
        rfolder = RFolder(self.rwechat.dir_file)
        pattern = f"^{file_md5}$"
        search_path = rfolder.search(pattern)

        # Download.
        if search_path is None:
            save_path = "%s\\%s" % (
                self.rwechat.dir_file,
                file_md5
            )
            self.rrdatabase_file.file.download(
                file_id,
                save_path
            )
        else:
            save_path = search_path

        file_name = file_info["name"]
        return save_path, file_name


    def _from_message_send(self) -> None:
        """
        Read record from table `message_send`, put send queue.
        """

        # Get parameter.
        conn = self.rrdatabase_wechat.connect()

        # Read.
        where = (
            "(\n"
            "    `send_state` = 0\n"
            "    AND (\n"
            "        `plan_time` IS NULL\n"
            "        OR `plan_time` < NOW()\n"
            "    )\n"
            ")"
        )
        result = conn.execute_select(
            ("wechat", "message_send"),
            ["send_id", "send_type", "receive_id", "parameters"],
            where,
            order="`plan_time` DESC, `send_id`"
        )

        # Convert.
        if result.empty:
            return
        table = result.fetch_table()

        # Update.
        send_ids = [
            row["send_id"]
            for row in table
        ]
        sql = (
            "UPDATE `wechat`.`message_send`\n"
            "SET `send_state` = 1\n"
            "WHERE `send_id` IN :send_ids"
        )
        conn.execute(
            sql,
            send_ids=send_ids
        )

        # Put.
        for row in table:
            parameters: Dict = json_loads(row["parameters"])
            parameters["is_from_db"] = True

            ## Save file.
            file_id = parameters.get("file_id")
            if file_id is not None:
                file_path, file_name = self._download_file(file_id)
                parameters["path"] = file_path
                parameters["file_name"] = file_name

            self.rwechat.send(
                row["send_type"],
                row["receive_id"],
                send_id=row["send_id"],
                **parameters
            )

        # Commit.
        conn.commit()


    @wrap_thread
    def from_message_send(self) -> None:
        """
        In the thread, loop read record from table `message_send`, put send queue.
        """


        # Define.
        def handler_update_send_state(
            params: Dict,
            success: bool
        ) -> None:
            """
            Update field `send_state` of table `message_send`.

            Parameters
            ----------
            params : Send parameters.
            success : Whether the sending was successful.
            """

            # Break.
            send_id = params.get("send_id")
            if send_id is None:
                return

            # Get parameter.
            if success:
                send_state = 2
            else:
                send_state = 3
            data = {
                "send_id": send_id,
                "send_state": send_state
            }

            # Update.
            self.rrdatabase_wechat.execute_update(
                ("wechat", "message_send"),
                data
            )


        # Add handler.
        self.rwechat.rsend.add_handler(handler_update_send_state)

        # Loop.
        while True:

            # Put.
            self._from_message_send()

            # Wait.
            sleep(1)