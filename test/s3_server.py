import os
import socket
import subprocess


class S3ServerMinio(object):
    def __init__(
            self,
            storage_path,
            port=9000,
            access_key="PRJDKN8R6PAXOGTEIK3E",
            secret_key="Avz/QFxGZluv9vjwntFqIwXctNx8niFlMg7MzO5O"):
        """
        Starts a local minio server
        """
        
        self._port = port
        self._tls = False
        self._access_key = access_key
        self._secret_key = secret_key
        self._process_server = None
        self._storage_path = os.path.join(storage_path, "data")

    def __del__(self):
        self.stop()
        pass
        
    def start(self) -> None:
        """
        Start the server
        """

        # Set environment variables for process
        minio_env = os.environ.copy()
        minio_env["MINIO_ACCESS_KEY"] = self._access_key
        minio_env["MINIO_SECRET_KEY"] = self._secret_key
        
        # Start a minio server
        cmd = [
            "minio",
            "server",
            self._storage_path,
            "--address",
            ":" + str(self._port),
        ]
        self._process_server = subprocess.Popen(cmd, env=minio_env, stdout=subprocess.DEVNULL)

    def stop(self):
        if self._process_server is not None:
            self._process_server.terminate()
            self._process_server = None

    @property
    def accesskey(self):
        return self._access_key

    @property
    def secretkey(self):
        return self._secret_key

    @property
    def port(self):
        return self._port

    @property
    def endpoint(self):
        return socket.gethostname()

    @property
    def endpoint_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    pass
