import ssl
import socket

# https://stackoverflow.com/questions/36888882/how-to-mock-a-socket-object-via-the-mock-library

"""
 def setup_method(self):
     socket = Mock()
     socket.recv = Mock()
     socket.send = Mock()
     with patch("socket.create_connection") as create_connection:
         create_connection.return_value = socket
         self.connection = TCPSocketConnection(("localhost", 1234))
"""


class SocketMock:

    _next_reply: List[bytes]

    def __init__(self, sslsocket: bool = False): 
        self._next_reply = []

        if sslsocket:
            self.socket = mocker.patch(
                target='ssl.SSLContext.wrap_socket',
                autospec=True
            )
        else:
            self.socket = mocker.patch(
                target='socket.socket',
                autospec=True
            )

        self.socket.return_value.recv.side_effect = self._recv
        self.socket.return_value.sendall.side_effect = self._sendall
        # self.socket.return_value.sendall.call_args

    def add_reply(
        self,
        request: bytes,
        answer: bytes,
    ) -> None:
        pass

    def send(
        self,
        data: bytes,
    ) -> None:
        pass

    def _add_reply(self, data: bytes) -> None:
        self._next_reply.append(data)

    def _recv(self, *args, **kwargs) -> bytes:
        pass

    def _sendall(self, data, *args, **kwargs) -> None:
        pass

