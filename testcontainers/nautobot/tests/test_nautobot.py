from typing import Any, Generator, List

from pynautobot import api as NautobotApi
from pynautobot.core.response import Record
from pytest import fixture

from testcontainers.nautobot import NautobotTestContainer

PynautobotObject = List[Record | Any] | Record | Any

TEST_IMAGE = "networktocode/nautobot-lab:1.6.2"
DEFAULT_PORT = 8000


@fixture(scope="module")
def nautobot_container() -> Generator[NautobotTestContainer, Any, None]:
    with NautobotTestContainer(
        image=TEST_IMAGE, port=DEFAULT_PORT
    ) as nautobot_container:
        yield nautobot_container


@fixture(scope="module")
def nautobot(nautobot_container) -> NautobotApi:
    api_key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    nautobot_instance = NautobotApi(url=nautobot_container.url, token=api_key)
    return nautobot_instance


def test_nautobot_version(nautobot_container):
    requested_version = TEST_IMAGE.split(":")[1]
    version = nautobot_container.exec("nautobot-server --version")[1]
    assert version.decode("utf-8").strip() == requested_version


def test_create_circuit_in_nautobot(nautobot):
    try:
        provider: PynautobotObject = nautobot.circuits.providers.create(
            name="TestProvider"
        )
        circuit_type: PynautobotObject = nautobot.circuits.circuit_types.create(
            name="backbone"
        )
        circuit_data = {
            "cid": "CID0001",
            "provider": provider.id,
            "type": circuit_type.id,
            "status": "active",
        }
        circuit: PynautobotObject = nautobot.circuits.circuits.create(**circuit_data)
        assert circuit.cid == circuit_data["cid"]
        assert circuit.provider.id == circuit_data["provider"]
        assert circuit.type.id == circuit_data["type"]
        assert circuit.status.value == circuit_data["status"]
    finally:
        circuit.delete()
        provider.delete()
        circuit_type.delete()


def test_create_device_in_nautobot(nautobot):
    try:
        platform: PynautobotObject = nautobot.dcim.platforms.create(name="JimbOS")
        manufacturer: PynautobotObject = nautobot.dcim.manufacturers.create(
            name="jimbox"
        )
        device_type: PynautobotObject = nautobot.dcim.device_types.create(
            model="router", slug="router", manufacturer=manufacturer.id
        )
        device_role: PynautobotObject = nautobot.dcim.device_roles.create(name="core")
        site: PynautobotObject = nautobot.dcim.sites.create(
            name="TestSite", status="active"
        )

        device_data = {
            "name": "NodeA",
            "device_type": device_type.id,
            "device_role": device_role.id,
            "platform": platform.id,
            "site": site.id,
            "status": "active",
        }

        device: PynautobotObject = nautobot.dcim.devices.create(**device_data)
        assert device.name == device_data["name"]
        assert device.device_type.id == device_data["device_type"]
        assert device.device_role.id == device_data["device_role"]
        assert device.platform.id == device_data["platform"]
        assert device.site.id == device_data["site"]

    finally:
        device.delete()


def test_get_circuit_from_nautobot(nautobot):
    try:
        provider1: PynautobotObject = nautobot.circuits.providers.create(
            name="TestProvider1"
        )
        provider2: PynautobotObject = nautobot.circuits.providers.create(
            name="TestProvider2"
        )
        circuit_type: PynautobotObject = nautobot.circuits.circuit_types.create(
            name="backbone"
        )
        circuit_data1 = {
            "cid": "CID0001",
            "provider": provider1.id,
            "type": circuit_type.id,
            "status": "active",
        }
        circuit_data2 = {
            "cid": "CID0002",
            "provider": provider2.id,
            "type": circuit_type.id,
            "status": "active",
        }
        circuit1: PynautobotObject = nautobot.circuits.circuits.create(**circuit_data1)
        circuit2: PynautobotObject = nautobot.circuits.circuits.create(**circuit_data2)

        circuit_list: List = list(nautobot.circuits.circuits.all())

        assert circuit1 == nautobot.circuits.circuits.get(circuit1.id)
        assert circuit2 == nautobot.circuits.circuits.get(circuit2.id)
        assert len(circuit_list) == 2

    finally:
        circuit1.delete()
        circuit2.delete()
        provider1.delete()
        provider2.delete()
        circuit_type.delete()
