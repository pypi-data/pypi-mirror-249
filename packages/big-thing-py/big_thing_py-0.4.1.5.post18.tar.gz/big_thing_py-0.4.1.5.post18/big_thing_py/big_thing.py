from big_thing_py.core.thing import *

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as MXClient
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ServiceInfo
import ssl
import argparse
import socket


# ASCII Art from https://patorjk.com/software/taag/#p=display&h=1&v=1&f=Big

# ======================================================================== #
#    _____         _____   ____   _      _______  _      _                 #
#   / ____|       |  __ \ |  _ \ (_)    |__   __|| |    (_)                #
#  | (___    ___  | |__) || |_) | _   __ _ | |   | |__   _  _ __    __ _   #
#   \___ \  / _ \ |  ___/ |  _ < | | / _` || |   | '_ \ | || '_ \  / _` |  #
#   ____) || (_) || |     | |_) || || (_| || |   | | | || || | | || (_| |  #
#  |_____/  \___/ |_|     |____/ |_| \__, ||_|   |_| |_||_||_| |_| \__, |  #
#                                     __/ |                         __/ |  #
#                                    |___/                         |___/   #
# ======================================================================== #

MIDDLEWARE_ONLINE_CHECK_INTERVAL = 0.5


class MXBigThing(MXThing):
    def __init__(
        self,
        name: str = MXThing.DEFAULT_NAME,
        desc='',
        version=sdk_version(),
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        is_super: bool = False,
        is_parallel: bool = True,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_cert_path: str = '',
        ssl_key_path: str = '',
        log_name: str = '',
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
    ):
        super().__init__(
            name=name, desc=desc, version=version, service_list=service_list, alive_cycle=alive_cycle, is_super=is_super, is_parallel=is_parallel
        )

        # Log
        self._log_mode = log_mode
        self._log_enable = log_enable
        self._log_name = log_name

        # MQTT
        self._mqtt_client: MXClient = None
        self._ip = convert_url_to_ip(ip)
        self._port = port
        self._ssl_ca_path = ssl_ca_path
        self._ssl_cert_path = ssl_cert_path
        self._ssl_key_path = ssl_key_path

        # Util
        self._append_mac_address = append_mac_address

        # Thread
        self._g_exit: Event = Event()
        self._g_comm_exit: Event = Event()
        self._comm_thread_list: List[MXThread] = []
        self._thread_list: List[MXThread] = []

        self._thread_comm_func_list: List[Callable] = [
            self._message_receiving_thread_func,
            self._message_publishing_thread_func,
        ]
        self._thread_func_list: List[Callable] = [
            self._alive_publishing_thread_func,
            self._value_publishing_thread_func,
        ]

        if not is_valid_ip_address(self._ip) or not 1024 < self._port <= 65535:
            raise MXValueError('Invalid IP address, port number')
        else:
            self._ip = convert_url_to_ip(ip)

        if self._is_super and not self._is_parallel:
            raise MXValueError('Super Thing must be parallel')

    def __eq__(self, o: 'MXBigThing') -> bool:
        instance_check = isinstance(o, MXBigThing)
        is_parallel_check = self._is_parallel == o._is_parallel
        is_super_check = self._is_super == o._is_super

        return super().__eq__(o) and instance_check and is_parallel_check and is_super_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_ip'] = self._ip
        state['_port'] = self._port
        state['_ssl_ca_path'] = self._ssl_ca_path
        state['_ssl_cert_path'] = self._ssl_cert_path
        state['_ssl_key_path'] = self._ssl_key_path
        state['_append_mac_address'] = self._append_mac_address

        del state['_log_mode']
        del state['_log_enable']
        del state['_log_name']
        del state['_mqtt_client']
        del state['_g_exit']
        del state['_g_comm_exit']
        del state['_comm_thread_list']
        del state['_thread_list']
        del state['_thread_comm_func_list']
        del state['_thread_func_list']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._ip = state['_ip']
        self._port = state['_port']
        self._ssl_ca_path = state['_ssl_ca_path']
        self._ssl_cert_path = state['_ssl_cert_path']
        self._ssl_key_path = state['_ssl_key_path']
        self._append_mac_address = state['_append_mac_address']

        self._log_mode = MXPrintMode.ABBR
        self._log_enable = True
        self._log_name = ''
        self._mqtt_client = None
        self._g_exit = Event()
        self._g_comm_exit = Event()
        self._comm_thread_list = []
        self._thread_list = []
        self._thread_comm_func_list = [
            self._message_receiving_thread_func,
            self._message_publishing_thread_func,
        ]
        self._thread_func_list = [
            self._alive_publishing_thread_func,
            self._value_publishing_thread_func,
        ]

    def setup(self, avahi_enable=True) -> 'MXBigThing':
        self._init_logger()
        self._update_thing_ID(self._name)

        self._receive_queue = Queue()
        self._publish_queue = Queue()

        self._mqtt_client = MXClient(client_id=self._name)

        # FIXME: Later, username and password options must be given by argument of the MXBigThing class
        self._mqtt_client.username_pw_set('tester', 'test12')
        self._mqtt_client.reconnect_delay_set(min_delay=1, max_delay=10)

        for function in self._function_list:
            function.set_publish_queue(self._publish_queue)

        # TODO: MXThing에서 처리할 것인지 MXBigThing에서 처리할 것인지 정해야함.
        self._value_list = []
        self._function_list = []
        for service in self._service_list:
            self.add_service(service)

        try:
            if avahi_enable:
                check_python_version()
                self._auto_setup_middleware()
            else:
                MXLOG_DEBUG('Skip Middleware discover...')

            if self._check_ssl_enable():
                MXLOG_DEBUG('Connect with SSL...', 'green')
                self._set_ssl_config()
            else:
                MXLOG_DEBUG('[WARN] Connect without SSL...', 'yellow')

            # self._connect(self._ip, self._port)

            # receive, publish쓰레드는 나머지 쓰레드들과 분리하여 exit event를 설정
            # wrapup 할 때 나머지 쓰레드들은 한꺼번에 종료가 되어도 되지만, receive, publish 쓰레드는
            # receive, publish queue에 남아있는 메시지를 모두 전송, 처리하고 종료되어야 하기 때문에
            # exit event를 따로 설정하여 종료시킴
            for func in self._thread_comm_func_list:
                thread = MXThread(target=func, args=(self._g_comm_exit,))
                self._comm_thread_list.append(thread)
            for func in self._thread_func_list:
                thread = MXThread(target=func, args=(self._g_exit,))
                self._thread_list.append(thread)

            return self
        except KeyboardInterrupt:
            MXLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    def run(self):
        try:
            self._connect(self._ip, self._port)
            # Start main threads

            for thread in self._comm_thread_list + self._thread_list:
                thread.start()

            self._register()

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
        except KeyboardInterrupt as e:
            MXLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError as e:
            MXLOG_DEBUG(f'Connection error while connect to broker. Check ip and port - {self._ip}:{self._port}', 'red')
            sys.exit(1)
        except Exception as e:
            print_error(e)
            return self.wrapup()

    def wrapup(self):
        try:
            self._send_TM_UNREGISTER()
            cur_time = get_current_time()

            self._g_exit.set()
            for thread in self._thread_list:
                thread.join()
                MXLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            while not ((self._publish_queue.empty() and self._receive_queue.empty()) or (get_current_time() - cur_time > 3)):
                time.sleep(THREAD_TIME_OUT)

            self._g_comm_exit.set()
            for thread in self._comm_thread_list:
                thread.join()
                MXLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            self._disconnect()
            MXLOG_DEBUG('Thing Exit', 'red')
            return True
        except Exception as e:
            print_error(e)
            return False

    # ================================================================================================= #
    #   _______  _                            _   ______                    _    _                      #
    #  |__   __|| |                          | | |  ____|                  | |  (_)                     #
    #     | |   | |__   _ __  ___   __ _   __| | | |__  _   _  _ __    ___ | |_  _   ___   _ __   ___   #
    #     | |   | '_ \ | '__|/ _ \ / _` | / _` | |  __|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|  #
    #     | |   | | | || |  |  __/| (_| || (_| | | |   | |_| || | | || (__ | |_ | || (_) || | | |\__ \  #
    #     |_|   |_| |_||_|   \___| \__,_| \__,_| |_|    \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/  #
    # ================================================================================================= #

    def _message_receiving_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._receive_queue.empty():
                    continue

                recv_msg = self._receive_queue.get()
                # TODO: 결과에 따라 어떤 동작을 할지 정의
                rc = self._handle_mqtt_message(recv_msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _message_publishing_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._publish_queue.empty():
                    continue

                pub_msg = self._publish_queue.get()
                topic, payload, timestamp = decode_MQTT_message(pub_msg, mode=str)
                self._publish(topic, payload)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _alive_publishing_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._is_reconnected:
                    refresh_msg = self.generate_client_refresh_message().mqtt_message()
                    service_list_topic = MXProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % '+'
                    subscribed_topic_set_copy = self._subscribed_topic_set
                    self._subscribed_topic_set = set()

                    self._subscribe(service_list_topic)
                    while not self._is_middleware_online:
                        self._publish(refresh_msg.topic, refresh_msg.payload)
                        time.sleep(MIDDLEWARE_ONLINE_CHECK_INTERVAL)
                    self._unsubscribe(service_list_topic)

                    for topic in subscribed_topic_set_copy:
                        self._subscribe(topic)
                    # self._register()
                    self._send_TM_ALIVE()
                    self._is_reconnected = False
                elif not self._is_registered:
                    continue

                if get_current_time() - self._last_alive_time > self._alive_cycle:
                    self._send_TM_ALIVE()

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _value_publishing_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if not self._is_registered:
                    continue

                current_time = get_current_time()
                for value in self._value_list:
                    if not (current_time - value.get_last_update_time()) > value.get_cycle():
                        continue

                    is_updated = value.update()
                    if is_updated is not None:
                        self._send_TM_VALUE_PUBLISH(value=value)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # ======================================================================================================================= #
    # _    _                    _  _         __  __   ____  _______  _______   __  __                                         #
    # | |  | |                  | || |       |  \/  | / __ \|__   __||__   __| |  \/  |                                       #
    # | |__| |  __ _  _ __    __| || |  ___  | \  / || |  | |  | |      | |    | \  / |  ___  ___  ___   __ _   __ _   ___    #
    # |  __  | / _` || '_ \  / _` || | / _ \ | |\/| || |  | |  | |      | |    | |\/| | / _ \/ __|/ __| / _` | / _` | / _ \   #
    # | |  | || (_| || | | || (_| || ||  __/ | |  | || |__| |  | |      | |    | |  | ||  __/\__ \\__ \| (_| || (_| ||  __/   #
    # |_|  |_| \__,_||_| |_| \__,_||_| \___| |_|  |_| \___\_\  |_|      |_|    |_|  |_| \___||___/|___/ \__,_| \__, | \___|   #
    #                                                                                                         __/ |           #
    #                                                                                                         |___/           #
    # ======================================================================================================================= #

    def _handle_mqtt_message(self, msg: mqtt.MQTTMessage) -> bool:
        topic_string = decode_MQTT_message(msg)[0]
        protocol = MXProtocolType.get(topic_string)
        msg.timestamp = time.time()

        if protocol == MXProtocolType.Base.MT_RESULT_REGISTER:
            rc = self._handle_MT_RESULT_REGISTER(msg)
        elif protocol == MXProtocolType.Base.MT_RESULT_UNREGISTER:
            rc = self._handle_MT_RESULT_UNREGISTER(msg)
        elif protocol == MXProtocolType.Base.MT_RESULT_BINARY_VALUE:
            rc = self._handle_MT_RESULT_BINARY_VALUE(msg)
        elif protocol in [MXProtocolType.Base.MT_EXECUTE, MXProtocolType.Base.MT_IN_EXECUTE]:
            rc = self._handle_MT_EXECUTE(msg)
        # for Auto Reregister feature
        elif protocol == MXProtocolType.WebClient.ME_RESULT_SERVICE_LIST:
            rc = self._handle_ME_RESULT_SERVICE_LIST(msg)
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected topic! topic: {topic_string}')
            return False

        return rc

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    def _handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage) -> MXErrorCode:
        register_result_msg = MXRegisterResultMessage(msg)
        error = register_result_msg.error

        if self._name != register_result_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {self._name} should be arrive, not {register_result_msg.thing_name}'
            )
            return MXErrorCode.FAIL

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {self._name} register success!')
            self._middleware_name = register_result_msg.middleware_name
            self._is_registered = True
            for service in self._function_list + self._value_list:
                service.set_middleware_name(self._middleware_name)
                service.set_thing_name(self._name)
            self._subscribe_service_topic_list()
            return error
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Thing {self._name} register packet is not valid. error code: {register_result_msg.error}',
                'red',
            )
            return error
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Unexpected error occurred!!! error code: {register_result_msg.error}',
                'red',
            )
            return error

    def _handle_MT_RESULT_UNREGISTER(self, msg: mqtt.MQTTMessage) -> MXErrorCode:
        unregister_result_msg = MXUnregisterResultMessage(msg)
        error = unregister_result_msg.error

        if self._name != unregister_result_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {self._name} should be arrive, not {unregister_result_msg.thing_name}',
                'red',
            )
            return MXErrorCode.FAIL

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {self._name} register success!')
            self._is_registered = False
            self._unsubscribe_all_topic_list()
            return error
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Thing {self._name} unregister packet is not valid. error code: {unregister_result_msg.error}',
                'red',
            )
            return error
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Unexpected error occurred!!! error code: {unregister_result_msg.error}',
                'red',
            )
            return error

    def _handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage):
        execute_msg = MXExecuteMessage(msg)
        target_function = self._get_function(execute_msg.function_name)
        is_inner = execute_msg.protocol_type == MXProtocolType.Base.MT_IN_EXECUTE

        if not target_function:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Target function not found! - topic: {decode_MQTT_message(msg)[0]}')
            return False
        if self._name != execute_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {self._name} should be arrive, not {execute_msg.thing_name}',
                'red',
            )
            return False
        if execute_msg.topic_error or execute_msg.payload_error:
            MXLOG_DEBUG(f'[{get_current_function_name()}] execute_msg error! - topic: {decode_MQTT_message(msg)[0]}{execute_msg.topic_error}')
            return False

        # 서로의 arg_list가 일치하는 지 확인한다.
        if not self._compare_arg_list(target_function.get_arg_list(), list(execute_msg.tuple_arguments())):
            MXLOG_DEBUG(f'Not matched arg_list', 'red')
            target_function._send_TM_RESULT_EXECUTE(
                scenario=execute_msg.scenario,
                error=MXErrorCode.FAIL,
                request_ID=execute_msg.request_ID,
                is_inner=is_inner,
                client_id=execute_msg.client_id,
            )
            return False

        # 병렬실행이 가능한지 옵션을 살펴보고, 이후에 실행 중인지 살펴본다.
        if self._is_parallel:
            # 중복된 시나리오로부터 온 실행 요청이면 -4 에러코드를 보낸다.
            if execute_msg.scenario in target_function.get_running_scenario_list():
                target_function._send_TM_RESULT_EXECUTE(
                    scenario=execute_msg.scenario,
                    error=MXErrorCode.DUPLICATE,
                    request_ID=execute_msg.request_ID,
                    is_inner=is_inner,
                    client_id=execute_msg.client_id,
                )
                return True
            execute_thread = target_function.start_execute_thread(execute_msg)
        elif not target_function._running:
            execute_thread = target_function.start_execute_thread(execute_msg)
        else:
            target_function._send_TM_RESULT_EXECUTE(
                scenario=execute_msg.scenario,
                error=MXErrorCode.FAIL,
                request_ID=execute_msg.request_ID,
                is_inner=is_inner,
                client_id=execute_msg.client_id,
            )
            return True

        if not execute_thread:
            return False
        else:
            return True

    # TODO: complete this function
    def _handle_MT_RESULT_BINARY_VALUE(self, msg: mqtt.MQTTMessage) -> bool:
        execute_msg = MXBinaryValueResultMessage(msg)

        if self._name != execute_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {self._name} should be arrive, not {execute_msg.thing_name}',
                'red',
            )
            return False

        for value in self._value_list:
            if value.get_name() == execute_msg.value_name and value.get_type() == MXType.BINARY:
                value.set_binary_sending(False)
                return True
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Value {execute_msg.value_name} does not exist!!!', 'red')
            return False

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    def _send_TM_REGISTER(self) -> None:
        register_msg = self.generate_register_message()
        self._subscribe_init_topic_list()
        if not register_msg:
            raise Exception('TM_REGISTER packet error')

        register_mqtt_msg = register_msg.mqtt_message()
        self._publish_queue.put(register_mqtt_msg)

    def _send_TM_UNREGISTER(self):
        unregister_msg = self.generate_unregister_message()
        unregister_mqtt_msg = unregister_msg.mqtt_message()
        self._publish_queue.put(unregister_mqtt_msg)

    def _send_TM_ALIVE(self):
        alive_msg = self.generate_alive_message()
        alive_mqtt_msg = alive_msg.mqtt_message()
        self._publish_queue.put(alive_mqtt_msg)
        self._last_alive_time = get_current_time()

    def _send_TM_VALUE_PUBLISH(self, value: MXValue) -> None:
        value_publish_msg = self.generate_value_publish_message(value=value)
        value_publish_mqtt_msg = value_publish_msg.mqtt_message()

        if value.get_type() == MXType.BINARY:
            value.set_binary_sending(True)
        self._publish_queue.put(value_publish_mqtt_msg)

    # ================
    #  __  __  ______
    # |  \/  ||  ____|
    # | \  / || |__
    # | |\/| ||  __|
    # | |  | || |____
    # |_|  |_||______|
    # ================

    # for Auto Reregister feature
    def _handle_ME_RESULT_SERVICE_LIST(self, msg: mqtt.MQTTMessage) -> bool:
        execute_msg = MXClientServiceListResultMessage(msg)
        if 'services' in execute_msg.payload:
            MXLOG_DEBUG(f'Middleware detected!!!')
            self._is_middleware_online = True

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _subscribe_init_topic_list(self) -> None:
        topic_list = [
            MXProtocolType.Base.MT_RESULT_REGISTER.value % self._name,
            MXProtocolType.Base.MT_RESULT_UNREGISTER.value % self._name,
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE.value % self._name,
        ]

        for topic in topic_list:
            self._subscribe(topic)

    def _subscribe_service_topic_list(self):
        topic_list = []

        for function in self._function_list:
            topic_list += [
                MXProtocolType.Base.MT_EXECUTE.value % (function.get_name(), self._name, '+', '+'),
                (MXProtocolType.Base.MT_EXECUTE.value % (function.get_name(), self._name, '', '')).rstrip('/'),
                MXProtocolType.Base.MT_IN_EXECUTE.value % (function.get_name(), self._name),
            ]

        for topic in topic_list:
            self._subscribe(topic)

    def _unsubscribe_all_topic_list(self):
        # whenever _unsubscribe function execute, it remove target topic from self._subscribed_topic_set
        # so it need to iterate with copy of self._subscribed_topic_set
        target_topic_list = list(self._subscribed_topic_set)
        for topic in target_topic_list:
            self._unsubscribe(topic)

    # FIXME: This method will be deprecated. Remove after ManagerThing fixed
    def _check_register_result(self, error: MXErrorCode):
        if not isinstance(error, MXErrorCode):
            error = MXErrorCode.get(error)

        if error == MXErrorCode.NO_ERROR:
            MXLOG_DEBUG(f'{PrintTag.GOOD} Thing {self._name} register success!')
            return True
        elif error == MXErrorCode.DUPLICATE:
            MXLOG_DEBUG(f'{PrintTag.DUP} Thing {self._name} register success!')
            return True
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Thing {self._name} register packet is not valid')
            return False
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected error occurred!!!', 'red')
            return False

    # FIXME: This method will be deprecated. Remove after ManagerThing fixed
    def _check_unregister_result(self, error: MXErrorCode):
        if not isinstance(error, MXErrorCode):
            error = MXErrorCode.get(error)

        if error == MXErrorCode.NO_ERROR:
            MXLOG_DEBUG(f'{PrintTag.GOOD} Thing {self._name} unregister success!')
            return True
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Thing {self._name} unregister packet is not valid')
            return False
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected error occurred!!!', 'red')
            return False

    def _convert_arg_list(self, arg_list: List[Union[MXArgument, Union[int, float, str, bool]]]) -> List[MXType]:
        if isinstance(arg_list, list) and all([isinstance(arg, (int, float, str, bool)) for arg in arg_list]):
            arg_type_list = []
            for arg in arg_list:
                # if is_base64(arg):
                #     arg_type_list.append(MXType.BINARY)
                # else:
                #     arg_type_list.append(MXType.get(type(arg)))
                arg_type_list.append(MXType.get(type(arg)))
        elif isinstance(arg_list, list) and all([isinstance(arg, MXArgument) for arg in arg_list]):
            arg_type_list = [arg.get_type() for arg in arg_list]
        else:
            raise MXTypeError(f'arg_list must be list of MXArgument or list of int, float, str, bool: {arg_list}')

        return arg_type_list

    def _compare_arg_list(
        self,
        arg_list1: List[Union[MXArgument, Union[int, float, str, bool]]],
        arg_list2: List[Union[MXArgument, Union[int, float, str, bool]]],
    ):
        arg_type_list1 = self._convert_arg_list(arg_list1)
        arg_type_list2 = self._convert_arg_list(arg_list2)

        if len(arg_type_list1) != len(arg_type_list2):
            MXLOG_DEBUG(f'Not matched arg_list length: {len(arg_type_list1)} != {len(arg_type_list2)}', 'red')
            return False

        for arg_type1, arg_type2 in zip(arg_type_list1, arg_type_list2):
            if arg_type1 in [MXType.INTEGER, MXType.DOUBLE] and arg_type2 in [MXType.INTEGER, MXType.DOUBLE]:
                pass
            elif arg_type1 != arg_type2:
                MXLOG_DEBUG(f'Not matched arg_list type: {arg_type1} != {arg_type2}', 'red')
                return False
        else:
            return True

    def _print_packet(self, topic: str, payload: str, direction: Direction, mode: MXPrintMode = MXPrintMode.FULL, pretty: bool = False) -> str:
        def prune_payload(payload: str, mode: MXPrintMode) -> str:
            if mode == MXPrintMode.SKIP:
                payload = colored(f'skip... (print_packet mode={mode})', 'yellow')
            elif mode == MXPrintMode.ABBR:
                if payload.count('\n') > 10:
                    payload = '\n'.join(payload.split('\n')[:10]) + '\n' + colored(f'skip... (print_packet mode={mode})', 'yellow')
                elif len(payload) > 1000:
                    payload = payload[:1000] + '\n' + colored(f'skip... (print_packet mode={mode})', 'yellow')
                else:
                    pass
            elif mode == MXPrintMode.FULL:
                pass
            else:
                raise Exception(f'[print_packet] Unknown mode!!! mode should be [skip|abbr|full] mode : {mode}', 'red')

            return payload

        topic_template = MXProtocolType.get(topic)
        if not topic_template:
            MXLOG_DEBUG(f'[print_packet] Unknown topic!!! topic : {topic}')

        topic_indicator = '_'.join([topic_token for topic_token in topic_template.value.split('/') if topic_token != '%s'])
        payload = prune_payload(payload=dict_to_json_string(dict_object=payload, pretty=pretty), mode=mode)

        MXLOG_DEBUG(f'[{topic_indicator:20}][{direction.value}] topic: {topic} payload: {payload}')

    #### MQTT utils ####

    def _register(self):
        self._send_TM_REGISTER()

    def _connect(self, ip: str, port: int):
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_disconnect = self._on_disconnect
        self._mqtt_client.on_publish = self._on_publish
        self._mqtt_client.on_subscribe = self._on_subscribe
        self._mqtt_client.on_unsubscribe = self._on_unsubscribe
        self._mqtt_client.on_message = self._on_message

        if self._mqtt_client.connect(ip, port):
            raise MXConnectionError(f'Connect failed!!! ip: {ip}, port: {port}')

        self._mqtt_client.loop_start()

    def _disconnect(self):
        self._mqtt_client.loop_stop()
        if self._mqtt_client.disconnect():
            raise MXConnectionError(f'Disconnect failed!!!')

    def _subscribe(self, topic: str, qos: int = 0):
        if topic in self._subscribed_topic_set:
            return True

        ret = self._mqtt_client.subscribe(topic, qos=qos)
        if not ret[0] == 0:
            MXLOG_DEBUG(f'{PrintTag.SUBSCRIBE} subscribe failed!!!', 'red')
            return False

        self._subscribed_topic_set.add(topic)
        MXLOG_DEBUG(f'{PrintTag.SUBSCRIBE} {topic}')

        return True

    def _unsubscribe(self, topic: str):
        if topic not in self._subscribed_topic_set:
            return True

        ret = self._mqtt_client.unsubscribe(topic)
        if not ret[0] == 0:
            MXLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} unsubscribe failed!!!', 'red')
            return False

        self._subscribed_topic_set.add(topic)
        MXLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} {topic}')

        return True

    def _publish(self, topic: str, payload, qos: int = 0):
        self._print_packet(topic=topic, payload=payload, direction=Direction.PUBLISH, mode=self._log_mode)
        ret = self._mqtt_client.publish(topic, payload, qos=qos)
        if ret.rc != 0:
            MXLOG_DEBUG(f'Publish failed!!! Topic: {topic}, Payload: {payload}', 'red')
            if not MXProtocolType.get(topic) == MXProtocolType.Base.TM_VALUE_PUBLISH:
                self._publish_queue.put(encode_MQTT_message(topic, payload))
            time.sleep(1)

    def _init_logger(self):
        if self._log_enable:
            START_LOGGER(whole_log_path=self._log_name, logging_mode=MXLogger.LoggingMode.ALL)
        else:
            START_LOGGER(logging_mode=MXLogger.LoggingMode.CONSOLE)

    def _check_ssl_enable(self) -> bool:
        if not self._ssl_ca_path and not self._ssl_cert_path and not self._ssl_key_path:
            return False
        if not os.path.exists(self._ssl_ca_path):
            raise MXNotFoundError(f'SSL CA file not found. invalid path: {self._ssl_ca_path}')
        elif not os.path.exists(self._ssl_cert_path):
            raise MXNotFoundError(f'SSL Cert file not found. invalid path: {self._ssl_cert_path}')
        elif not os.path.exists(self._ssl_key_path):
            raise MXNotFoundError(f'SSL Key file not found.. invalid path: {self._ssl_key_path}')
        else:
            return True

    def _set_ssl_config(self):
        try:
            self._mqtt_client.tls_set(
                ca_certs=self._ssl_ca_path,
                certfile=self._ssl_cert_path,
                keyfile=self._ssl_key_path,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS_CLIENT,
            )
            # self._mqtt_client.tls_insecure_set(True)
        except ValueError:
            MXLOG_DEBUG('SSL/TLS has already been configured.', 'yellow')

    def _check_valid_middleware(self, device_list: List[dict]):
        valid_middleware_list = []
        for device in device_list:
            host = device['host']
            port = device['port']
            try:
                ack_topic = MXProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % (self._name)

                test_mqtt_client = MXClient(client_id=self._name)
                test_mqtt_client.on_message = self._on_message
                # ssl 연결의 경우 ssl 연결을 미리 설정 후 연결해야한다.
                # 그런데 ssl 연결인지 아닌지 판단을 어떻게 해야할지?
                rc = test_mqtt_client.connect(host, port)
                test_mqtt_client.loop_start()

                test_mqtt_client.subscribe(ack_topic)
                refresh_msg = self.generate_client_refresh_message()
                test_mqtt_client.publish(refresh_msg.topic, refresh_msg.payload)

                self._receive_queue.get(timeout=0.5)
                valid_middleware_list.append(device)
                MXLOG_DEBUG(f'valid middleware on {host}:{port}', 'green')
            except Empty:
                MXLOG_DEBUG(f'Not valid middleware on {host}:{port}', 'yellow')
            except ConnectionRefusedError:
                MXLOG_DEBUG(f'No middleware on {host}:{port}', 'yellow')

            test_mqtt_client.unsubscribe(ack_topic)
            test_mqtt_client.loop_stop()
            test_mqtt_client.disconnect()
            del test_mqtt_client

        return valid_middleware_list

    def _discover_middleware(self, timeout: float = 10) -> List[dict]:
        discovered_device_list = []
        # FIXME: rename to sopiot -> mxiot
        service_type_list = ['_mqtt_sopiot._tcp.local.', '_mqtt_ssl_sopiot._tcp.local.']

        def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
            if state_change is ServiceStateChange.Added:
                info = zeroconf.get_service_info(service_type, name)

                if not info:
                    MXLOG_DEBUG('No info')
                    return

                parsed_address_info_list = info.parsed_scoped_addresses()
                if not parsed_address_info_list:
                    MXLOG_DEBUG('No address info')
                    return

                addresses = [f'{address_info}:{cast(int, info.port)}' for address_info in parsed_address_info_list]
                ipv4_address = addresses[0].split(':')[0]
                # ipv6_address = addresses[1]
                port = int(addresses[0].split(':')[1])

                discovered_device_info = dict(name=info.server, host=ipv4_address, port=port)

                MXLOG_DEBUG(f'Server name: {info.server}')
                MXLOG_DEBUG(f'Address: {ipv4_address}')
                MXLOG_DEBUG(f'Weight: {info.weight}, priority: {info.priority}')
                if info.properties:
                    for key, value in info.properties.items():
                        MXLOG_DEBUG(f'Properties -> {key.decode("utf-8")}: {value.decode("utf-8")}')
                else:
                    MXLOG_DEBUG('No properties', 'yellow')

                discovered_device_list.append(discovered_device_info)

        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        browser = ServiceBrowser(zeroconf, service_type_list, handlers=[on_service_state_change], delay=0.1)

        time.sleep(timeout)
        browser.cancel()
        zeroconf.close()

        # Check middleware validity
        valid_middleware_list = self._check_valid_middleware(discovered_device_list)
        return valid_middleware_list

    def _auto_setup_middleware(self, timeout: float = 10) -> List[dict]:
        def save_middleware_info(discovered_middleware_list: List[dict]):
            middleware_info = dict(
                middleware_list=[dict(**middleware, latest_connect_time=get_current_time()) for middleware in discovered_middleware_list]
            )
            json_file_write(f'/tmp/middleware_info-{self._name}.json', middleware_info)

        discovered_middleware_list = self._discover_middleware(timeout=timeout)
        if len(discovered_middleware_list) > 1:
            MXLOG_DEBUG('More than 2 middleware searched...')
            middleware_info = json_file_read(f'/tmp/middleware_info-{self._name}.json')

            if middleware_info:
                middleware_list = sorted(middleware_info['middleware_list'], key=lambda x: x['latest_connect_time'])
                self._ip = middleware_list[0]['host']
                self._port = middleware_list[0]['port']
                MXLOG_DEBUG('Connect to latest connected middleware...')
                return True
            else:
                MXLOG_DEBUG(f'/tmp/middleware_info-{self._name}.json does not exist...', 'yellow')
                for i, discovered_middleware in enumerate(discovered_middleware_list):
                    host = discovered_middleware['host']
                    port = discovered_middleware['port']
                    middleware_name = discovered_middleware['name']
                    MXLOG_DEBUG(f'{i}: {host}:{port} ({middleware_name})')
                while True:
                    user_input = int(input('select middleware : '))
                    if user_input not in range(len(discovered_middleware_list)):
                        MXLOG_DEBUG('Invalid input...', 'red')
                    else:
                        break
                self._ip = discovered_middleware_list[user_input]['host']
                self._port = discovered_middleware_list[user_input]['port']
                save_middleware_info(discovered_middleware_list)
                return True
        elif len(discovered_middleware_list) == 1:
            self._ip = discovered_middleware_list[0]['host']
            self._port = discovered_middleware_list[0]['port']
            save_middleware_info(discovered_middleware_list)
            return True
        else:
            MXLOG_DEBUG('Middleware discover failed... connect to default middleware...', 'red')
            return False

    def _update_thing_ID(self, name: str, interface: str = None) -> None:
        self._name = self.generate_thing_id(name, self._append_mac_address, interface=interface)

    # ===================================================================================
    # ___  ___ _____  _____  _____   _____         _  _  _                   _
    # |  \/  ||  _  ||_   _||_   _| /  __ \       | || || |                 | |
    # | .  . || | | |  | |    | |   | /  \/  __ _ | || || |__    __ _   ___ | | __ ___
    # | |\/| || | | |  | |    | |   | |     / _` || || || '_ \  / _` | / __|| |/ // __|
    # | |  | |\ \/' /  | |    | |   | \__/\| (_| || || || |_) || (_| || (__ |   < \__ \
    # \_|  |_/ \_/\_\  \_/    \_/    \____/ \__,_||_||_||_.__/  \__,_| \___||_|\_\|___/
    # ===================================================================================

    # for MQTT version<5.0
    def _on_connect(self, client: MXClient, userdata, flags, result):
        if result == 0:
            self._connected = True
            MXLOG_DEBUG(f'{PrintTag.CONNECT} Connect to Host: {self._ip}:{self._port}')
            while any([not thread.is_alive() for thread in self._comm_thread_list + self._thread_list]):
                time.sleep(THREAD_TIME_OUT)

            # Auto Reregister feature
            if self._is_registered:
                self._is_reconnected = True
        else:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Bad connection... Returned code: {result}', 'red')

    def _on_disconnect(self, client: MXClient, userdata, rc):
        if rc == 0:
            self._connected = False
            self._is_reconnected = False
            self._is_middleware_online = False
            MXLOG_DEBUG(f'{PrintTag.DISCONNECT} Disconnect from Host: {self._ip}:{self._port}')
        else:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Bad disconnection... Returned code: {rc}', 'red')

    def _on_subscribe(self, client: MXClient, userdata: str, mid, granted_qos):
        pass

    def _on_unsubscribe(self, client: MXClient, userdata: str, mid):
        pass

    def _on_publish(self, client: MXClient, userdata: mqtt.MQTTMessage, mid):
        pass

    def _on_message(self, client: MXClient, userdata: Callable, msg: mqtt.MQTTMessage):
        topic, payload, _ = decode_MQTT_message(msg)
        self._print_packet(topic=topic, payload=payload, direction=Direction.RECEIVED, mode=self._log_mode)
        self._receive_queue.put(msg)

    # TODO: test this functions
    # for MQTT version>=5.0
    def _on_connect_v5(self, client: MXClient, userdata, flags, reason, properties):
        if reason == 0:
            self._connected = True
            MXLOG_DEBUG(f'{PrintTag.CONNECT} Connect to Host: {self._ip}:{self._port}')
            if self._is_registered:
                pass
        else:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Bad connection... Returned code: {reason}', 'red')

    def _on_disconnect_v5(self, client: MXClient, userdata, rc, properties):
        if rc == 0:
            self._connected = False
            MXLOG_DEBUG(f'{PrintTag.DISCONNECT} Disconnect from Host: {self._ip}:{self._port}')
        else:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Bad disconnection... Returned code: {rc}', 'red')

    def _on_subscribe_v5(self, client: MXClient, userdata: str, mid, reasoncodes, properties):
        pass

    def _on_unsubscribe_v5(self, client: MXClient, userdata: str, mid, properties, reasoncodes):
        pass

    def _on_publish_v5(self, client: MXClient, userdata: mqtt.MQTTMessage, mid):
        pass

    def _on_message_v5(self, client: MXClient, userdata: Callable, msg: mqtt.MQTTMessage):
        topic, payload, _ = decode_MQTT_message(msg)
        self._print_packet(topic=topic, payload=payload, direction=Direction.RECEIVED, mode=self._log_mode)
        self._receive_queue.put(msg)

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    def get_log_mode(self) -> MXPrintMode:
        return self._log_mode

    def get_log_enable(self) -> bool:
        return self._log_enable

    def get_log_name(self) -> str:
        return self._log_enable

    def get_ip(self) -> str:
        return self._ip

    def get_port(self) -> int:
        return self._port

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_log_mode(self, mode: MXPrintMode) -> None:
        self._log_mode = mode

    def set_log_enable(self, enable: bool) -> None:
        self._log_enable = enable

    def set_log_name(self, name: str) -> None:
        self._log_name = name

    def set_ip(self, ip: str) -> None:
        self._ip = ip

    def set_port(self, port: int) -> None:
        self._port = port
