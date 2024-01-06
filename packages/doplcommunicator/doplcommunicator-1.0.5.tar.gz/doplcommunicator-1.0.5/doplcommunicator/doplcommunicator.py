import socketio
import threading
import time
from doplcommunicator.rwlock import RWLock

from doplcommunicator.controllerdata import ControllerData

class DoplCommunicator:
    __sio = socketio.Client()

    def __init__(self, url):
        self.__url = url
        
        self.__controller_data = ControllerData(False, 0, 0, 0, 0, 0, 0, 1)
        self.__controller_data_to_send: ControllerData = None
        self.__controller_data_lock = RWLock()
        self.__on_controller_data_callback = None
        self.__send_data = False

    @property
    def controller_data(self):
        with self.__controller_data_lock.r_locked():
            return self.__controller_data
    
    @controller_data.setter
    def controller_data(self, value):
        with self.__controller_data_lock.w_locked():
            if(value != self.__controller_data):
                self.__controller_data = value
                self.__controller_data_to_send = self.__controller_data

    def connect(self):
        self.__setup_events()
        self.__sio.connect(self.__url)

        # Start sending data
        self.__send_data = True
        threading.Thread(target=self.__send_data_thread).start()

    def disconnect(self):
        self.__sio.disconnect()
        self.__send_data = False

    def on_controller_data(self, callback):
        self.__on_controller_data_callback = callback

    def on_joined_session(self, callback):
        self.__sio.on("joined_session", callback)

    def __setup_events(self):
        def on_connect():
            print('connection established')

        def on_disconnect():
            print('disconnected from server')

        def on_controller_data(controller_data_dict):
            controller_data = ControllerData.fromDict(controller_data_dict)

            with self.__controller_data_lock.r_locked():
                self.__controller_data = controller_data

            if self.__on_controller_data_callback:
                self.__on_controller_data_callback(controller_data)

        self.__sio.on("connect", on_connect)
        self.__sio.on("disconnect", on_disconnect)
        self.__sio.on("remote_controller_data", on_controller_data)

    def __send_data_thread(self):
        while(self.__send_data):
            with self.__controller_data_lock.r_locked():
                if(self.__controller_data_to_send):
                    self.__sio.emit("remote_controller_data", self.__controller_data_to_send.toDict())
                    self.__controller_data_to_send = None