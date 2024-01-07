import socket
from datetime import datetime, timezone

import rsa


class VoteV1:
    def __init__(
        self,
        service_name: str,
        username: str,
        address: str,
        timestamp: datetime = datetime.now(timezone.utc),
    ):
        self.service_name = service_name
        self.username = username
        self.address = address
        self.timestamp = round(timestamp.timestamp() * 1000)

    def __str__(self) -> str:
        return f"""VOTE
{self.service_name}
{self.username}
{self.address}
{self.timestamp}
"""


def ensure_pem_format(key_str: str) -> str:
    pem_header = "-----BEGIN PUBLIC KEY-----"
    pem_footer = "-----END PUBLIC KEY-----"

    if not key_str.startswith(pem_header):
        key_str = pem_header + "\n" + key_str

    if not key_str.endswith(pem_footer):
        key_str = key_str + "\n" + pem_footer

    return key_str


class Client:
    def __init__(
        self,
        host: str,
        public_key: str,
        port: int = 8192,
        timeout: int = 3,
    ):
        self.public_key = public_key
        self.address = (host, port)
        self.timeout = timeout

    def vote(self, vote: VoteV1):
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(
            ensure_pem_format(self.public_key).encode())
        encrypted_message = rsa.encrypt(str(vote).encode(), pub_key)

        # Send the encrypted message
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.settimeout(self.timeout)
            header = s.recv(64).decode().split()
            if len(header) != 2:
                raise Exception("Not a Votifier v1 server")
            s.sendall(encrypted_message)
