import threading
import UDPServer
import time

BUFF_SIZE = 4096

class UDPServerMultiClient(UDPServer.UDPServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        
    def wait_for_client(self):
        try:
            while True:
                try:
                    print('\n\r waiting to receive messagge...')
                    data, address = self.sock.recvfrom(BUFF_SIZE)
                    
                    thread = threading.Thread(target = self.handle_request,
                                                args= (data, address))
                    thread.daemon = True
                    thread.start()
                    
                    if data.decode('utf8')[0:3] == 'put':
                        time.sleep(1)
                    
                except OSError as err:
                    print(err)
        except KeyboardInterrupt:
            self.shutdown_server()
            
def main():
    UDP_server_multiClient = UDPServerMultiClient('127.0.0.1', 10000)
    UDP_server_multiClient.configure_server()
    UDP_server_multiClient.wait_for_client()
    
if __name__ == '__main__':
    main()    
    