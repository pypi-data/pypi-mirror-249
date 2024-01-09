import os
import threading
import time 

from base64 import b64encode


class SenderTransferer:

    def __init__(self, network):
        self.server = network.server
        self.network = network
        self.current_dir_path = os.getcwd()


    def _wait_for_previous_sending(self, interval):
        time.sleep(interval)


    def _read_file(self, path):
        with open(path, 'rb') as file:
            return b64encode(file.read()).decode()


    def _send_file(self, connection, file_path):
        file_name = file_path.replace(self.current_dir_path, '')
        file_content = self._read_file(file_path)
        self.network.send(connection, ('file', file_name, file_content))


    def _send_dir(self, connection, dir_path):
        dir_name = dir_path.replace(self.current_dir_path, '')
        self.network.send(connection, ('dir', dir_name))


    def _transfer(self, connection, dir_path):
        for path in os.listdir(dir_path):
            full_path = os.path.join(dir_path, path)
            if os.path.isfile(full_path):
                self._send_file(connection, full_path)
                self._wait_for_previous_sending(0.5)
            else:
                self._send_dir(connection, full_path)
                self._wait_for_previous_sending(0.5)
                child_dir_path = dir_path + '/' + path
                self._transfer(connection, child_dir_path)
        

    def _stop_transfer(self, connection):
        self.network.send(connection, ('break',))
        self._wait_for_previous_sending(0.5)
        connection.close()


    def _handle(self, connection):
        self._transfer(connection, self.current_dir_path) 
        self._stop_transfer(connection)

    
    def _init_handling_thread(self, connection):
        handling_thread = threading.Thread(target=self._handle, args=(connection,))
        handling_thread.start()


    def run(self):
        print('[+] Listening for incoming connecions')
        while True:
            connection, _ = self.server.accept()
            print('[+] Got a new connection')
            self._init_handling_thread(connection)
