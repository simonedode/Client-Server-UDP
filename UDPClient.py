import socket
import os
import select

BUFF_SIZE = 4096

class UDPClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
                        
    def get_file(self, file, server_address):
        response, serve_address = self.sock.recvfrom(BUFF_SIZE)
        if response.decode('utf8') == 'File exist':
            print('\nwaiting to receive the file...\n')
            f = open(file, 'wb')
            while True:
                read = select.select([self.sock], [], [], 0.1)
                if read[0]:
                    bytes_read, address = self.sock.recvfrom(BUFF_SIZE)
                    f.write(bytes_read)
                else:
                    f.close()
                    break
            print('file received successfully!\n')
        else:
            print(response.decode('utf8'))
    
    def put_file(self, file, server_address):
        if os.path.isfile(file):
            self.sock.sendto('Exist'.encode(), server_address)
            print('\r\nwaiting to send the file...')
            f = open(file, 'rb')
            bytes_read = f.read(BUFF_SIZE)
            while (bytes_read):
                if (self.sock.sendto(bytes_read, server_address)):
                    bytes_read = f.read(BUFF_SIZE)
            f.close()
        else:
            self.sock.sendto('File not exist'.encode(), server_address)
        data, server = self.sock.recvfrom(BUFF_SIZE)
        print(data.decode('utf8'))
        
    def interact_with_server(self, server_address):
        options = 'Available options:\nlist -> returns the list of available files\nget file -> get the specified file\nput file -> upload the file to the server\n\n'

        try:
            message = input(options)
                  
            print('\nsent: %s' % message)
            self.sock.sendto(message.encode(), server_address)
            command = message[0:4]
               
            if command == 'get ':
                self.get_file(message[4:], server_address)
            elif command == 'put ':
                self.put_file(message[4:], server_address)
            else:
                data, server = self.sock.recvfrom(BUFF_SIZE)
                print('\r\nReceved:\n %s' % data.decode('utf8'))
                
        except OSError as err:
            print(err)
        finally:
            print('closing socket')
            self.sock.close()

def main():
    udp_client = UDPClient()
    udp_client.interact_with_server(('127.0.0.1', 10000))

if __name__ == '__main__':
    main()
            