"""
LinkAI client

@author LinkAI
@Date 2023/12/31
"""

import socket
import json
import threading
from enum import Enum
from linkai._common.log import logger
import time
import os
import re


class ClientMsgType(Enum):
    LOGIN = "LOGIN"
    PUSH = "PUSH"
    HEARTBEAT = "HEARTBEAT"

    def __str__(self):
        return self.name


class PushMsg:
    def __init__(self, session_id: str, msg_content: str):
        self.session_id = session_id
        self.msg_content = msg_content


CLIENT_CONFIG_FILE = 'client_config.json'
CLIENT_ID_KEY = "client_id"
DEFAULT_HOST = "link-ai.chat"


class LinkAIClient:
    def __init__(self, api_key: str, host: str = "", heartbeat_interval=10, reconnect_times=5, reconnect_interval=5):
        self.client_id = self.fetch_client_id()
        self.api_key = api_key
        self.host = host or DEFAULT_HOST
        self.check_host()
        self.port = 7071
        self.socket = None
        self.connected = False
        self.heartbeat_interval = heartbeat_interval
        self.reconnect_times = reconnect_times
        self.reconnect_interval = reconnect_interval

    def on_message(self, push_msg: PushMsg):
        """
        client push msg callback
        :param push_msg: manual push msg
        :return:
        """
        raise NotImplementedError("Please implement the on_message method.")

    def start(self):
        """
        client startup
        """
        try:
            self._connect()
            self._send_login()
            threading.Thread(target=self._receive_messages).start()
            threading.Thread(target=self._send_heartbeat).start()
        except socket.error as e:
            logger.error(f"Unable to connect to the server: {e}")

    def fetch_client_id(self):
        if os.path.exists(CLIENT_CONFIG_FILE):
            with open(CLIENT_CONFIG_FILE, 'r') as file:
                client_config = json.load(file)
                if client_config:
                    return client_config.get(CLIENT_ID_KEY)
        return None

    def save_client_id(self, client_id: str):
        data = {
            CLIENT_ID_KEY: client_id
        }
        with open(CLIENT_CONFIG_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    def _connect(self):
        attempts = 0
        while attempts < self.reconnect_times and not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.connected = True
                logger.info("Connected to server")
            except socket.error as e:
                logger.warn(f"Connection failed: {e}")
                attempts += 1
                time.sleep(self.reconnect_interval)
        if not self.connected:
            logger.warn("Could not connect to server after several attempts")

    def _send_login(self):
        login_data = {
            "apiKey": self.api_key
        }
        if self.client_id:
            login_data["clientId"] = self.client_id
        login_msg = {
            "type": ClientMsgType.LOGIN.name,
            "data": login_data
        }
        message = json.dumps(login_msg) + "\r\n"
        self.socket.sendall(message.encode('utf-8'))

    def _send_heartbeat(self):
        while True:
            if self.connected:
                try:
                    heart_beat = {
                        "type": ClientMsgType.HEARTBEAT.name,
                    }
                    message = json.dumps(heart_beat) + "\r\n"
                    self.socket.sendall(message.encode('utf-8'))
                    logger.debug("[Client] send heartbeat")
                except socket.error:
                    self.connected = False
            time.sleep(self.heartbeat_interval)
            if not self.connected:
                logger.debug("Heartbeat try to reconnect...")
                self._connect()

    def _receive_messages(self):
        while True:
            try:
                message = self.socket.recv(4096)
                if message:
                    self._msg_handler(message)
                else:
                    self.connected = False
            except ConnectionResetError:
                # 如果服务端关闭了连接，会抛出 ConnectionResetError 异常
                self.connected = False
                logger.warn("Server closed the connection.")
            except socket.error:
                self.connected = False
                logger.warn("Server closed the connection.")
            except Exception as e:
                # 其他错误处理
                logger.warn(f"An error occurred: {e}")

            if not self.connected:
                self._connect()
                logger.debug("Receive handler try to reconnect...")

    def _msg_handler(self, message):
        msg_str = message.decode('utf-8').strip("\x00")
        msg_str = msg_str.split("\0")[0]
        logger.debug(msg_str)
        msg = json.loads(msg_str)

        if msg.get("type") == ClientMsgType.PUSH.name:
            data = msg.get("data")
            session_id = data.get("sessionId")
            msg = data.get("msgContent")
            msg = PushMsg(session_id=session_id, msg_content=msg)
            logger.debug(f"Received message: {msg}, session_id={session_id}")  # 打印接收到的消息
            self.on_message(msg)

        elif msg.get("type") == ClientMsgType.LOGIN.name:
            if msg.get("code") == 200:
                if not self.client_id:
                    client_id = msg.get("data").get("clientId")
                    self.client_id = client_id
                    self.save_client_id(client_id)
                logger.debug(f"Login success, res={msg}, client_id={self.client_id}")
            else:
                logger.info(f"Login failed, res={msg}")

    def check_host(self):
        pattern = re.compile(r'^(.*\.)?(link-ai\.tech|link-ai\.chat|link-ai\.pro)$')
        if not bool(pattern.match(self.host)):
            raise RuntimeError("cannot connect")
