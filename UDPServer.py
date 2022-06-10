import socket
import os
import select

BUFF_SIZE = 4096

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        
    def configure_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('\n\r starting up on %s port %s' % (self.host, self.port))
        self.sock.bind((self.host, self.port))
       
    def list_files(self, address):
        filelist = ''
        for filename in os.listdir(os.getcwd()):
            if filename != 'UDPServer.py' and filename != 'UDPServerMultiClient.py':
                filelist = filelist + filename + '\n'
        sent = self.sock.sendto(filelist.encode(), address)
        return sent        
            
    def get_file(self, file, address):
        if os.path.isfile(file):
            sent = self.sock.sendto('File exist'.encode(), address)
            f = open(file, 'rb')
            bytes_read = f.read(BUFF_SIZE)
            while (bytes_read):
                check = self.sock.sendto(bytes_read, address)
                if(check):
                    sent = sent + check
                    bytes_read = f.read(BUFF_SIZE)
            f.close()
        else:
            sent = self.sock.sendto('\nError: file not exist!\n'.encode(), address)
        return sent
            
    def put_file(self, file):
            accept, address = self.sock.recvfrom(BUFF_SIZE)
            if accept.decode('utf8') == 'Exist':
                f = open(file, 'wb')
                while True:
                    read = select.select([self.sock], [], [], 0.1)
                    if read[0]:
                        bytes_read, address = self.sock.recvfrom(BUFF_SIZE)
                        f.write(bytes_read)
                    else:
                        f.close()
                        response = '\nfile uploaded successfully!\n'
                        break
            else:
                response = '\nError: impossible to upload the file!\n'
            sent = self.sock.sendto(response.encode(), address)
            return sent
        
    def handle_request(self, data, address):
        message = data.decode('utf8')
        print('\n\r received "%s" from %s' % (message, address))
        if message[0:4] == 'list':
            sent = self.list_files(address)
        elif message[0:3] == 'get':
            sent = self.get_file(message[4:], address)
        elif message[0:3] == 'put':
            sent = self.put_file(message[4:])
        else:
            sent = self.sock.sendto('\nError: command not available!\n'.encode(), address)
        
        print('sent %s bytes back to %s' % (sent, address))
        
    def wait_for_client(self):
        try:
            print('\n\r waiting to receive messagge...')
            data, address = self.sock.recvfrom(BUFF_SIZE)
            self.handle_request(data, address)
        except Exception as err:
            print(err)
    
    def shutdown_server(self):
        print('\nShutting down server...')
        self.sock.close()