# nautobot-lab-testcontainer
Python Class to assist on Nautobot integration testing

## Installation

To install the package, clone the repository and use Poetry:

```bash
git clone https://github.com/yourusername/nautobot-lab-testcontainer.git
cd nautobot-lab-testcontainer
poetry install
```

Alternatively, you can add it directly via git:

```bash
poetry add git+https://github.com/yourusername/nautobot-lab-testcontainer.git
```

## Usage

Here's a basic example of how to use the `nautobot-lab-testcontainer`:

```python
from pytest import fixture
from typing import Any, List
from testcontainers.nautobot import NautobotTestContainer
from typing import Generator

PynautobotObject = List[Record|Any] | Record | Any

TEST_IMAGE = "networktocode/nautobot-lab:1.6.2"
DEFAULT_PORT = 8000

@fixture(scope="module")
def nautobot_container() -> Generator[NautobotTestContainer, Any, None]:
    with NautobotTestContainer(image=TEST_IMAGE, port=DEFAULT_PORT) as nautobot_container:
        yield nautobot_container

def test_nautobot_version(nautobot_container):
    requested_version = TEST_IMAGE.split(":")[1]
    version = nautobot_container.exec("nautobot-server --version")[1]
    assert version.decode("utf-8").strip() == requested_version
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

