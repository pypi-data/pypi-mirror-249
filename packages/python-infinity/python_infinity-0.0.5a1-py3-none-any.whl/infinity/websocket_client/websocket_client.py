import json
import logging
import threading
import time
import traceback
from collections import deque
from datetime import datetime
import websocket
from infinity.login.infinity_login import LoginClient
from infinity.utils import RepeatTimer, create_thread_with_kwargs, get_default_logger
from infinity.websocket_client import constants


class WebSocketClient:
    def __init__(self, ws_url: str = None, login: LoginClient = None,
                 auto_reconnect_retries: int = 0, logger: logging.Logger = None):
        """
        Initializes the InfinityWebsocket object.

        Args:
            ws_url (str): Websocket
            login (LoginClient): login to use private websocket
            auto_reconnect_retries (int): The number of times to attempt auto-reconnection in case of disconnection.
            logger (logging.Logger): The logger object to use for logging.
        """
        # websocket.enableTrace(True)
        self.__ping_timeout = 30
        self.__ping_interval = 60
        self._WS_URL = ws_url
        self._private_ws = None
        self._public_ws = None
        self._inf_login = login
        self._auto_reconnection_retries = auto_reconnect_retries
        self._pub_request_id = 1
        self._prv_request_id = 1
        self._prv_reconnect_count = 0
        self._pub_reconnect_count = 0
        self._subscribed_data_dict = {
            constants.CHANNEL_USER_TRADE: deque([]),
            constants.CHANNEL_ORDER_BOOK: deque([]),
            constants.CHANNEL_USER_ORDER: deque([]),
            constants.CHANNEL_RECENT_TRADES: deque([])
        }
        self._public_subscribed_channels = set()
        self._private_subscribed_channels = set()

        self.__private_ws_lock = threading.Lock()
        self._is_public_reconnecting = False
        self._is_private_reconnecting = False

        if logger is None:
            self._logger = get_default_logger()
        else:
            self._logger = logger

        if self._inf_login:
            if self._inf_login.is_login_success():
                self._access_token = self._inf_login.get_access_token()
                refresh_interval = self._inf_login.get_refresh_interval()
                refresh_event = RepeatTimer(refresh_interval, self.refresh_private_ws)
                refresh_event.start()
            else:
                self._logger.error("Cannot login, please check login details")

    def refresh_private_ws(self) -> None:
        """
        Refresh the private WebSocket connection when JWT token is refreshed.

        This function is used to refresh the private WebSocket connection by disconnecting from the current connection
        and establishing a new connection.

        Raises:
            ConnectionError: If the connection to the server fails during the refresh process.
        """
        # wait for refreshing/re-logging in process to finish
        while self._inf_login.is_refreshing_token() or self._inf_login.is_re_logging_in():
            time.sleep(1)
        new_token = self._inf_login.get_access_token()
        if self._access_token != new_token:
            self._logger.info("Refreshing private websocket session...")
            try:
                self.__private_ws_lock.acquire()
                self._access_token = new_token
                self._prv_reconnect_count = 0
                new_private_thread = self.create_private_client()
                new_private_thread.start()
                while not self.is_private_connected():
                    time.sleep(1)  # Adjust the delay as needed
                self._logger.info("New private websocket session is established.")
                self._logger.info("Re-subscribe to previous private channels.")
                self.resubscribe_private_channels()
            finally:
                self._logger.info("Private websocket session is refreshed.")
                self.__private_ws_lock.release()

    def resubscribe_private_channels(self) -> None:
        """
        Re-subscribe to previously subscribed private channels after refreshing private websocket connection.

        Iterates through the set of previously subscribed private channels and calls subscribe_private_channel
        to re-subscribe to each channel.

        Returns:
            None
        """
        self._logger.info(f"Re-subscribe to private channels = {self._private_subscribed_channels}")
        resubscribe = {
            "method": "SUBSCRIBE",
            "params": list(self._private_subscribed_channels)
        }
        self.send_private_message(message=resubscribe)

    def resubscribe_public_channels(self) -> None:
        """
        Re-subscribe to previously subscribed public channels.

        Iterates through the set of previously subscribed public channels and calls subscribe_public_channel
        to re-subscribe to each channel.

        Returns:
            None
        """
        self._logger.info(f"Re-subscribe to public channels = {self._private_subscribed_channels}")
        resubscribe = {
            "method": "SUBSCRIBE",
            "params": list(self._public_subscribed_channels)
        }
        self.send_public_message(message=resubscribe)

    def run_all(self) -> None:
        """
        Runs the public and private WebSocket clients in separate threads and waits for the connections to be
        established.

        This method creates separate threads for the public and private WebSocket clients using the
        `create_public_client` and `create_private_client` methods. It starts both threads and waits until both
        connections are established before returning.

        Note: This method should be called after initializing the `InfinityWebsocket` object and performing the login
        process if required.

        Returns:
            None

        Example:
        websocket_client = InfinityWebsocket(environment="PROD", user_agent="MyApp/1.0",
        account_address="0x123456789", private_key="my_private_key", verify_tls=True, do_login=True,
        auto_reconnect_retries=3, logger=my_logger)

        websocket_client.run_all()
        """
        self._logger.info("Initializing Infinity Public Websocket...")
        public_thread = self.create_public_client()
        public_thread.start()
        if self._inf_login:
            self._logger.info("Initializing Infinity Private Websocket...")
            private_thread = self.create_private_client()
            private_thread.start()
            while not (self.is_private_connected() and self.is_public_connected()):
                time.sleep(1)  # Adjust the delay as needed
            self._logger.info("Infinity Public and Private Websockets are connected.")
        else:
            while not self.is_public_connected():
                time.sleep(1)  # Adjust the delay as needed
            self._logger.info("Infinity Public Websocket is connected.")

    def is_public_connected(self) -> bool:
        """
        Check if the public WebSocket connection is currently connected.

        Returns:
            bool: True if the connection is active, False otherwise.
        """
        return self._public_ws and self._public_ws.sock and self._public_ws.sock.connected

    def is_private_connected(self) -> bool:
        """
        Check if the private WebSocket connection is currently connected.

        Returns:
            bool: True if the connection is active, False otherwise.
        """
        return self._private_ws and self._private_ws.sock and self._private_ws.sock.connected and (
                self._access_token is not None)

    def create_public_client(self) -> threading.Thread:
        """
        Creates a thread that connects to the public Infinity server.

        Returns:
            threading.Thread: A thread of the public WebSocket session.
        """
        self.public_connect()
        return create_thread_with_kwargs(func=self._public_ws.run_forever,
                                         kwargs={"ping_timeout": self.__ping_timeout,
                                                 "ping_interval": self.__ping_interval})

    def create_private_client(self) -> threading.Thread:
        """
        Creates a thread that connects to the private Infinity server.
        User need to login first to get access token before connecting private websocket.

        Returns:
            threading.Thread: A thread of the private WebSocket session.
        """
        if self._inf_login.is_login_success():
            self.private_connect()
            return create_thread_with_kwargs(func=self._private_ws.run_forever,
                                             kwargs={"ping_timeout": self.__ping_timeout,
                                                     "ping_interval": self.__ping_interval})
        else:
            self._logger.info("Please login before running private infinity client.")

    def public_connect(self) -> None:
        """
        The public_connect function is used to connect the public websocket client.

        Returns:
            None
        """
        self._logger.debug(f"Connecting infinity public websocket client...")
        new_public_ws = websocket.WebSocketApp(self._WS_URL,
                                               on_open=self.on_public_open,
                                               on_message=self.on_public_message,
                                               on_close=self.on_public_close,
                                               on_error=self.on_public_error,
                                               on_ping=self.on_public_ping,
                                               on_pong=self.on_public_pong)
        if self._public_ws is None:
            self._public_ws = new_public_ws
        else:
            self._logger.info(f"Old public websocket connection will be closed.")
            self._public_ws.close()
            self._public_ws = new_public_ws

    def private_connect(self) -> None:
        """
        The private_connect function is used to connect the private websocket client.

        Returns:
            None
        """
        self._logger.debug(f"Connecting infinity private websocket client...")
        ws_header = "Authorization: Bearer " + self._access_token
        new_private_ws = websocket.WebSocketApp(self._WS_URL,
                                                on_open=self.on_private_open,
                                                on_message=self.on_private_message,
                                                on_close=self.on_private_close,
                                                on_error=self.on_private_error,
                                                header=[ws_header],
                                                on_ping=self.on_private_ping,
                                                on_pong=self.on_private_pong)
        if self._private_ws is None:
            self._private_ws = new_private_ws
        else:
            self._logger.info(f"Expired private websocket connection will be closed.")
            self._private_ws.close()
            self._private_ws = new_private_ws

    def re_connect_public(self) -> None:
        """
        The re_connect_public function is used to re-connect the Infinity public websocket client.
        It will attempt to reconnect for a number of times specified by the user when user initialize
        InfinityWebsocket. (param: auto_reconnection_retries)
        If it fails, it will log a warning message and stop trying.

        Returns:
            None
        """
        if self._auto_reconnection_retries == 0:
            self._logger.info("Auto-reconnection is disabled.")
        elif self._pub_reconnect_count >= self._auto_reconnection_retries:
            self._logger.warning("Cannot re-connect Infinity public websocket client.")
        else:
            self._logger.info(
                f"Re-connecting Infinity public websocket client. Previous reconnects: {self._pub_reconnect_count}")
            public_thread = self.create_public_client()
            public_thread.start()
            while not self.is_public_connected():
                time.sleep(1)  # Adjust the delay as needed
            self._is_public_reconnecting = False
            self._pub_reconnect_count += 1
            if self.is_public_connected():
                self.resubscribe_public_channels()

    def re_connect_private(self) -> None:
        """
        The re_connect_private function is used to re-connect the Infinity private websocket client.
        It will attempt to reconnect for a number of times specified by the user when user initialize
        InfinityWebsocket. (param: auto_reconnection_retries)
        If it fails, it will log a warning message and stop trying.

        Returns:
            None
        """
        if self._auto_reconnection_retries == 0:
            self._logger.info("Auto-reconnection is disabled.")
        elif self._prv_reconnect_count >= self._auto_reconnection_retries:
            self._logger.warning("Cannot re-connect Infinity private websocket client.")
        else:
            self._logger.info(
                f"Re-connecting Infinity private websocket client. Previous reconnects: {self._prv_reconnect_count}")
            self._access_token = self._inf_login.get_access_token()
            private_thread = self.create_private_client()
            private_thread.start()
            while not self.is_private_connected():
                time.sleep(1)  # Adjust the delay as needed
            self._is_private_reconnecting = False
            self._prv_reconnect_count += 1
            if self.is_private_connected():
                self.resubscribe_private_channels()

    def disconnect_all(self) -> None:
        """
        The disconnect function is used to close the websocket connection on
        both private and public websockets.

        Returns:
            None
        """
        self._logger.info(f"Disconnecting websocket client..")
        if self._private_ws:
            self._logger.info("Logout from infinity login client")
            self._inf_login.close_session()
            self._private_ws.close()
        if self._public_ws:
            self._public_ws.close()

    @staticmethod
    def create_subscription_message(channel_str: str) -> dict:
        """
        Create subscribe message.

        Args:
            channel_str (str): Channel name

        Returns:
            dict: Subscribe message
        """
        return {
            "method": "SUBSCRIBE",
            "params": [
                channel_str
            ]
        }

    @staticmethod
    def create_unsubscription_message(channel_str: str) -> dict:
        """
        Create unsubscribe message.

        Args:
            channel_str (str): Channel name to unsubscribe from

        Returns:
            dict: Unsubscribe message
        """
        return {
            "method": "UNSUBSCRIBE",
            "params": [
                channel_str
            ]
        }

    def send_public_message(self, message: dict) -> None:
        """
        Sends a message using the public websocket.

        Args:
            message (str): The message to be sent.

        Returns:
            None
        """
        method = message["method"]
        if method == "SUBSCRIBE":
            self._public_subscribed_channels.update(message.get("params", []))
        elif method == "UNSUBSCRIBE":
            self._public_subscribed_channels -= set(message.get("params", []))
        message["id"] = self._pub_request_id
        self._logger.debug(f"Sending websocket public message {message=}.")
        if self._public_ws:
            self._public_ws.send(json.dumps(message))
            self._pub_request_id += 1

    def send_private_message(self, message: dict) -> None:
        """
        Sends a message using the private websocket.

        Args:
            message (str): The message to be sent.

        Returns:
            None
        """
        method = message["method"]
        if method == "SUBSCRIBE":
            self._private_subscribed_channels.update(message.get("params", []))
        elif method == "UNSUBSCRIBE":
            self._private_subscribed_channels -= set(message.get("params", []))
        message["id"] = self._prv_request_id
        self._logger.debug(f"Sending websocket private message {message=}.")
        if self._private_ws:
            self._private_ws.send(json.dumps(message))
            self._prv_request_id += 1

    def get_public_subscription(self) -> None:
        """
        Get public subscribed channels
        """
        message = {
            "method": "LIST_SUBSCRIPTIONS"
        }
        self.send_public_message(message=message)

    def get_private_subscription(self) -> None:
        """
        Get private subscribed channels
        """
        message = {
            "method": "LIST_SUBSCRIPTIONS"
        }
        self.send_private_message(message=message)

    def get_received_data(self, channel: str) -> dict:
        """
        Retrieves the received data from the subscribed channel.

        Args:
            channel (str): The name of the channel.

        Returns:
            str: The received message.
        """
        if len(self._subscribed_data_dict[channel]) > 0:
            message = self._subscribed_data_dict[channel].popleft()
            return message

    def subscribe_orderbook(self, instrument_id: str) -> None:
        """
        Subscribes to the order book channel for a given instrument id.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_ORDER_BOOK)
        message = self.create_subscription_message(channel_str=channel_str)
        self._logger.info(f"Subscribing orderbook for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_public_message(message=message)

    def unsubscribe_orderbook(self, instrument_id: str) -> None:
        """
        Unsubscribes from the order book channel for a given instrument id.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_ORDER_BOOK)
        message = self.create_unsubscription_message(channel_str=channel_str)
        self._logger.info(f"Unsubscribing orderbook for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_public_message(message=message)

    def subscribe_public_trades(self, instrument_id: str) -> None:
        """
        Subscribes to the public trades channel for a given instrument id.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_RECENT_TRADES)
        message = self.create_subscription_message(channel_str=channel_str)
        self._logger.info(f"Subscribing public trades channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_public_message(message=message)

    def unsubscribe_public_trades(self, instrument_id: str) -> None:
        """
        Unsubscribes from the public trades channel for a given instrument id.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_RECENT_TRADES)
        message = self.create_unsubscription_message(channel_str=channel_str)
        self._logger.info(f"Unsubscribing public trades channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_public_message(message=message)

    def subscribe_user_trade(self, instrument_id: str) -> None:
        """
        Subscribes to the user trade channel for a given instrument id.
        This function is a private function that requires infinity login.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_USER_TRADE)
        message = self.create_subscription_message(channel_str=channel_str)
        self._logger.info(f"Subscribing user trade channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_private_message(message=message)

    def unsubscribe_user_trade(self, instrument_id: str) -> None:
        """
        Unsubscribes from the user trade channel for a given instrument id.
        This function is a private function that requires infinity login.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_USER_TRADE)
        message = self.create_unsubscription_message(channel_str=channel_str)
        self._logger.info(f"Unsubscribing user trade channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_private_message(message=message)

    def subscribe_user_order(self, instrument_id: str) -> None:
        """
        Subscribes to the user order channel for a given instrument id.
        This function is a private function that requires infinity login.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_USER_ORDER)
        message = self.create_subscription_message(channel_str=channel_str)
        self._logger.info(f"Subscribing user order channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_private_message(message=message)

    def unsubscribe_user_order(self, instrument_id: str) -> None:
        """
        Unsubscribes from the user order channel for a given instrument id.
        This function is a private function that requires infinity login.

        Args:
            instrument_id (str): The instrument id of the market (e.g. ETH-SPOT).

        Returns:
            None
        """
        channel_str = self.generate_param_str(instrument_id=instrument_id, channel=constants.CHANNEL_USER_ORDER)
        message = self.create_unsubscription_message(channel_str=channel_str)
        self._logger.info(f"Unsubscribing user order channel for {instrument_id=}, {channel_str=}, {message=}.")
        self.send_private_message(message=message)

    @staticmethod
    def generate_param_str(instrument_id: str, channel: str) -> str:
        """
        Generate the channel parameter for a websocket subscription/unsubscription.

        Args:
            instrument_id (str): The instrument id for which the subscription is being made.
            channel (str): The channel for the subscription.

        Returns:
            str: The string representation of the channel parameter.
        """
        return f"{instrument_id}@{channel}"

    def on_orderbook_data(self, message: dict) -> None:
        """
        Process the orderbook data received from the WebSocket connection.

        Args:
            message (dict): The orderbook data received from the WebSocket connection.

        Returns:
            None

        Example:
            {
                "e": "orderBook",  # Channel name
                "E": 1696584283888,
                "s": "ETH-2023-10-07",  # Market name
                "m": 10358,  # Market id
                "P": {
                    "a": [  # Asks
                        {
                            "p": "0.0351",  # Rate
                            "q": "3.8105"  # Quantity
                        },
                        ...
                    ],
                    "b": [  # Bids
                        {
                            "p": "0.0319",
                            "q": "3.8786"
                        },
                        ...
                    ]
                }
            }
        """
        try:
            instrument_id = message.get("I", None) if message.get("I", None) is not None else message.get("s", None)
            update_time = datetime.utcfromtimestamp(message.get("E", None) / 1000)

            price_dict = message.get("P", None)

            asks_list = price_dict.get("a", None)
            bids_list = price_dict.get("b", None)

            asks_book = {float(price_obj.get("p", 0)): float(price_obj.get("q", 0)) for price_obj in asks_list}
            asks_book = {k: asks_book[k] for k in sorted(asks_book, reverse=True)}

            bids_book = {float(price_obj.get("p", 0)): float(price_obj.get("q", 0)) for price_obj in bids_list}
            bids_book = {k: bids_book[k] for k in sorted(bids_book)}

            book = {constants.INSTRUMENT_ID: instrument_id, constants.UPDATE_TIME: update_time,
                    constants.BIDS: bids_book, constants.ASKS: asks_book}

            self._logger.debug(f"Orderbook: {book=}.")
            self.process_orderbook_data(orderbook=book)
        except Exception as e:
            self._logger.error(f"Exception thrown in on_orderbook_data raw={message}, {e=}. {traceback.format_exc()}")

    def process_orderbook_data(self, orderbook: dict) -> None:
        """
        Process orderbook data.

        Args:
            orderbook (dict): The orderbook data to be processed.

        Returns:
            None
        """
        self._subscribed_data_dict[constants.CHANNEL_ORDER_BOOK].append(orderbook)

    def on_user_trade_data(self, message: dict) -> None:
        """
        Process user trade data received from the WebSocket connection.

        Args: message (dict): The user trade data received from the WebSocket connection.

        Returns:
            None

        Example of user trade raw message:
        {
            "e": "userTrade",
            "E": 1696384117706,
            "s": "ETH-SPOT",
            "m": 1,
            "P": {
                "p": "0.011", (price)
                "q": "0.0074", (quantity)
                "d": 1696384117681, (trade time)
                "t": 38088018, (trade ID)
                "w": 207, (account ID)
                "s": false, (side, True is borrow and False is LEND)
                "o": 54683065 (order ID)
            }
        }
        """
        try:
            symbol = message.get("s", None)
            # private message object
            message = message.get("P", None)
            instrument_id = message.get("I", None) if message.get("I", None) is not None else symbol
            trade_id = message.get("t", None)
            order_id = message.get("o", None)
            account_id = message.get("w", None)
            rate = float(message.get("p", 0))
            quantity = float(message.get("q", 0))
            side = constants.BORROW if message.get("s", None) else constants.LEND
            trade_time = datetime.utcfromtimestamp(message.get("d", None) / 1000)
            user_trade = {
                constants.INSTRUMENT_ID: instrument_id,
                constants.TRADE_ID: trade_id,
                constants.ORDER_ID: order_id,
                constants.ACCOUNT_ID: account_id,
                constants.SIDE: side,
                constants.RATE: rate,
                constants.QUANTITY: quantity,
                constants.TRADE_TIME: trade_time
            }

            self._logger.debug(f"User trade: {user_trade=}.")
            self.process_user_trade(user_trade=user_trade)
        except Exception as e:
            self._logger.error(f"Exception thrown in on_user_trades raw={message}, {e=}. {traceback.format_exc()}")

    def process_user_trade(self, user_trade: dict) -> None:
        """
        Process user trade data.

        Args:
            user_trade (dict): The user trade data to be processed.

        Returns:
            None
        """
        self._subscribed_data_dict[constants.CHANNEL_USER_TRADE].append(user_trade)

    def on_user_order_data(self, message: dict) -> None:
        """
        Process user order data received from the WebSocket connection.

        Args: message (dict): The user order data received from the WebSocket connection.

        Returns:
            None

        Example of user order:
        {
            "e": "userOrder",
            "E": 1696384117706,
            "s": "ETH-SPOT", (symbol)
            "m": 1, (market ID)
            "P": {
                "I": "ETH-SPOT", (instrument ID)
                "m": 1, (market ID)
                "p": "0.01", (price)
                "q": "0.01", (quantity)
                "a": "0.01", (accumulated filled size)
                "d": 1696384117635, (create timestamp)
                "w": 207, (account ID)
                "s": false, (side, True as borrow and False as LEND)
                "i": "f85f64d7", (client order ID)
                "o": 54683065, (order ID)
                "O": 1, (1 as market order and 2 as limit order)
                "M": 1, (1 as floating rate order and 2 as fixed rate order)
                "S": 10 (order status)
            }
        }
        """
        try:
            symbol = message.get("s", None)
            # private message object
            message = message.get("P", None)
            order_id = message.get("o", None)
            client_order_id = message.get("i", None)
            order_type = constants.LIMIT_ORDER if int(message.get("O", None)) == 2 else constants.MARKET_ORDER
            account_id = message.get("w", None)
            instrument_id = message.get("I", None) if message.get("I", None) is not None else symbol
            market_type = constants.FLOATING if int(message.get("M", None)) == 1 else constants.FIXED_RATE
            quantity = float(message.get("q", 0))
            side = constants.BORROW if message.get("s", None) else constants.LEND
            acc_fill_size = float(message.get("a", 0))
            create_date = datetime.utcfromtimestamp(message.get("d", None) / 1000)
            order_status = int(message.get("S", None))
            rate = float(message.get("p", 0))

            user_order = {
                constants.ORDER_ID: order_id,
                constants.CLIENT_ORDER_ID: client_order_id,
                constants.ORDER_TYPE: order_type,
                constants.ACCOUNT_ID: account_id,
                constants.INSTRUMENT_ID: instrument_id,
                constants.MARKET_TYPE: market_type,
                constants.RATE: rate,
                constants.QUANTITY: quantity,
                constants.SIDE: side,
                constants.ACC_FILL_SIZE: acc_fill_size,
                constants.CREATE_TIME: create_date,
                constants.ORDER_STATUS: constants.ORDER_STATUS_TYPE[order_status]
            }
            update_t = message.get("u", None)
            if update_t is not None:
                update_date = datetime.utcfromtimestamp(update_t / 1000)
                user_order[constants.UPDATE_TIME] = update_date
            self._logger.debug(f"User order: {user_order=}.")
            self.process_user_order(user_order=user_order)
        except Exception as e:
            self._logger.error(f"Exception thrown in on_user_orders raw={message}, {e=}. {traceback.format_exc()}")

    def process_user_order(self, user_order: dict) -> None:
        """
        Process user order data.

        Args:
            user_order (dict): The user order data to be processed.

        Returns:
            None
        """
        self._subscribed_data_dict[constants.CHANNEL_USER_ORDER].append(user_order)

    def on_public_trade(self, message: dict) -> None:
        """
        Processes recent trade data received from the WebSocket connection.

        Args: message (dict): The user order data received from the WebSocket connection.

        Returns:
            None

        Example:
        {
            "e": "recentTrades",
            "E": 1702970997315,
            "s": "USDT-2023-12-29",
            "m": 12148,
            "P": [
                {
                    "p": "0.0518",
                    "q": "1353.3",
                    "d": 1702970997296,
                    "s": "True"
                },
                {
                    "p": "0.0514",
                    "q": "4065.21",
                    "d": 1702970997296,
                    "s": "True"
                }
            ]
        }
        """
        try:
            instrument_id = message.get("I", None) if message.get("I", None) is not None else message.get("s", None)
            if instrument_id.split("-")[1] == "SPOT":
                rates_type = constants.FLOATING
            else:
                rates_type = constants.FIXED_RATE
            trades = message.get("P", None)
            if trades is not None and len(trades) > 0:
                for trade_msg in trades:
                    rate = float(trade_msg.get("p", 0))
                    quantity = float(trade_msg.get("q", 0))
                    side = constants.BORROW if trade_msg.get("s", None) else constants.LEND
                    trade_time = datetime.utcfromtimestamp(trade_msg.get("d", None) / 1000)
                    public_trade = {
                        constants.INSTRUMENT_ID: instrument_id,
                        constants.RATES_TYPE: rates_type,
                        constants.TRADE_TIME: trade_time,
                        constants.RATE: rate,
                        constants.QUANTITY: quantity,
                        constants.SIDE: side
                    }
                    self._logger.debug(f"Public trade: {public_trade}.")
                    self.process_public_trade(public_trade=public_trade)
        except Exception as e:
            self._logger.error(f"Exception thrown in on_public_trades raw={message}, {e=}. {traceback.format_exc()}")

    def process_public_trade(self, public_trade: dict) -> None:
        """
        Process a public trade.

        Args:
            public_trade (dict): The trade data received from the websocket.

        Returns:
            None
        """
        self._subscribed_data_dict[constants.CHANNEL_RECENT_TRADES].append(public_trade)

    def on_public_open(self, ws: websocket.WebSocketApp) -> None:
        """
        Handle the event when the public websocket connection is opened.

        Args:
            ws (websocket.WebSocketApp): public websocket app

        Returns:
            None
        """
        self._logger.debug(f"Public WebSocket connection opened")

    def on_private_open(self, ws: websocket.WebSocketApp) -> None:
        """
        Handle the event when the private websocket connection is opened.

        Args:
            ws (websocket.WebSocketApp): private websocket app

        Returns:
            None
        """
        self._logger.debug(f"Private WebSocket connection opened")

    def on_public_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Handle the event when a message is received on the public websocket.

        Args:
            ws (websocket.WebSocketApp): public websocket app
            message (str): The message received from the websocket.

        Returns:
            None
        """
        self._logger.debug(f"Received public message: {message=}.")
        message_obj = json.loads(message)
        result = message_obj.get("data", {}).get("result", None)
        if result is not None and isinstance(result, list) and len(result) > 0:
            self._logger.info(f"Public subscription list: {result}.")
        channel = message_obj.get("e", None)
        if channel is not None:
            if channel == constants.CHANNEL_RECENT_TRADES:
                self.on_public_trade(message=message_obj)
            elif channel == constants.CHANNEL_ORDER_BOOK:
                self.on_orderbook_data(message=message_obj)

    def on_private_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Handle the event when a message is received on the private websocket.

        Args:
            ws (websocket.WebSocketApp): private websocket app
            message (str): The message received from the websocket.

        Returns:
            None
        """
        self._logger.debug(f"Received private message: {message=}.")
        message_obj = json.loads(message)
        result = message_obj.get("data", {}).get("result", None)
        if result is not None and isinstance(result, list) and len(result) > 0:
            self._logger.info(f"Private subscription list: {result}.")
        channel = message_obj.get("e", None)
        if channel is not None:
            if channel == constants.CHANNEL_USER_ORDER:
                self.on_user_order_data(message=message_obj)
            elif channel == constants.CHANNEL_USER_TRADE:
                self.on_user_trade_data(message=message_obj)

    def on_private_close(self, ws: websocket.WebSocketApp, close_status_code: int, message: str) -> None:
        """
        Callback function called when a private WebSocket connection is closed.
        If close status code is not normal and private reconnection is not already in progress, trigger reconnection.

        Args:
            ws (websocket.WebSocketApp): private websocket app
            close_status_code (int): The status code indicating the reason for the closure.
            message (str): A human-readable string explaining the reason for the closure.

        Returns:
            None
        """
        if (close_status_code is not None and close_status_code != websocket.STATUS_NORMAL and
                not self._is_private_reconnecting):
            self._is_private_reconnecting = True
            self._logger.warning(f"Private WebSocket connection closed [{close_status_code=}]. {message=}.")
            self.re_connect_private()
        else:
            self._logger.info(f"Private WebSocket connection normally closed. {message=}.")

    def on_public_close(self, ws: websocket.WebSocketApp, close_status_code: int, message: str) -> None:
        """
        Callback function called when a public WebSocket connection is closed.
        If close status code is not normal and public reconnection is not already in progress, trigger reconnection.

        Args:
            ws (websocket.WebSocketApp): public websocket app
            close_status_code (int): The status code indicating the reason for the closure.
            message (str): A human-readable string explaining the reason for the closure.

        Returns:
            None
        """
        if (close_status_code is not None and close_status_code != websocket.STATUS_NORMAL and
                not self._is_public_reconnecting):
            self._is_public_reconnecting = True
            self._logger.warning(f"Public WebSocket connection closed [{close_status_code=}]. {message=}.")
            self.re_connect_public()
        else:
            self._logger.info(f"Public WebSocket connection normally closed. {message=}.")

    def on_private_error(self, ws: websocket.WebSocketApp, error) -> None:
        """
        Callback function called when an error occurs in a private WebSocket connection.

        Args:
            ws (websocket.WebSocketApp): private websocket app
            error (Exception): The exception object representing the error.

        Returns:
            None
        """
        if not self._is_private_reconnecting and isinstance(error, websocket.WebSocketConnectionClosedException):
            self._is_private_reconnecting = True
            self._logger.warning(f"Private Websocket Error: {error=}.")
            self.re_connect_private()

    def on_public_error(self, ws: websocket.WebSocketApp, error) -> None:
        """
        Callback function called when an error occurs in a private WebSocket connection.

        Args:
            ws (websocket.WebSocketApp): public websocket app
            error (Exception): The exception object representing the error.

        Returns:
            None
        """
        if not self._is_public_reconnecting and isinstance(error, websocket.WebSocketConnectionClosedException):
            self._is_public_reconnecting = True
            self._logger.warning(f"Public Websocket Error: {error=}.")
            self.re_connect_public()

    def on_public_ping(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Callback function called when a public ping message is received.

        Args:
            ws (websocket.WebSocketApp): public websocket app
            message (str): The ping message received from the server.

        Returns:
            None
        """
        self._logger.debug("Public Websocket got ping, reply sent.")

    def on_public_pong(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Callback function called when a public pong message is received.

        Args:
            ws (websocket.WebSocketApp): public websocket app
            message (str): The pong message received from the server.

        Returns:
            None
        """
        self._logger.debug("Public Websocket got pong, no need to reply.")

    def on_private_ping(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Callback function called when a private ping message is received.

        Args:
            ws (websocket.WebSocketApp): private websocket app
            message (str): The ping message received from the server.

        Returns:
            None
        """
        self._logger.debug("Private Websocket got ping, reply sent.")

    def on_private_pong(self, ws: websocket.WebSocketApp, message: str) -> None:
        """
        Callback function called when a private pong message is received.

        Args:
            ws (websocket.WebSocketApp): private websocket app
            message (str): The pong message received from the server.

        Returns:
            None
        """
        self._logger.debug("Private Websocket got pong, no need to reply.")
