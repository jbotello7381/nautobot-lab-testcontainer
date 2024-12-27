from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.core.utils import raise_for_deprecated_parameter
import requests


class NautobotTestContainer(DockerContainer):
    """
    A test container class for applications that use Nautobot.

    Attributes:
        DEFAULT_IMAGE (str): The default Docker image for Nautobot.
        DEFAULT_PORT (int): The default port for Nautobot.

    Args:
        image (str): The Docker image to use. Defaults to DEFAULT_IMAGE.
        port (int): The port to expose. Defaults to DEFAULT_PORT.
        **kwargs: Additional keyword arguments to pass to the DockerContainer.

    Methods:
        start() -> "NautobotTestContainer":
            Starts the Nautobot container and waits for it to be healthy.
        
        _wait_for_health_check() -> None:
            Waits for the Nautobot container to pass its health check.
        
        stdout() -> str:
            Returns the standard output logs of the Nautobot container.
        
        stderr() -> str:
            Returns the standard error logs of the Nautobot container.
    """

    DEFAULT_IMAGE = "networktocode/nautobot-lab:latest"
    DEFAULT_PORT = 8000

    def __init__(self, image: str = DEFAULT_IMAGE, port: int = DEFAULT_PORT, **kwargs) -> None:
        raise_for_deprecated_parameter(kwargs, "port_to_expose", "port")
        super().__init__(image, **kwargs)
        self.port = port
        self.with_exposed_ports(self.port)

    @wait_container_is_ready(requests.exceptions.RequestException)
    def _wait_for_health_check(self) -> None:
        health_url = f"{self.url}/health/"
        response = requests.get(health_url, timeout=1)
        response.raise_for_status()

    def start(self) -> "NautobotTestContainer":
        super().start()
        host, port = self.get_container_host_ip(), str(self.get_exposed_port(self.port))
        self.url = f"http://{host}:{port}"
        print(f"Nautobot test container starting at {self.url}... wait until ready")
        self._wait_for_health_check()
        print(f"Nautobot test container is ready for use at {self.url}")
        return self
        
    @property
    def stdout(self) -> str:
        return self.get_logs()[0].decode("utf-8")

    @property
    def stderr(self) -> str:
        return self.get_logs()[1].decode("utf-8")

