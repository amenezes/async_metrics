import pytest

from async_metrics.ext.utils import (
    Forbidden,
    private_ip_validator,
    private_ipv4_validator,
    private_ipv6_validator,
)


@pytest.mark.parametrize(
    "ip_address",
    [
        "10.40.101.123",
        "192.168.0.44",
        "172.19.104.32",
        "10.20.30.40",
        "192.168.1.100",
        "172.30.45.20",
        "10.200.12.34",
        "192.168.2.55",
        "172.16.50.12",
        "10.15.20.30",
    ],
)
def test_private_ipv4(ip_address):
    assert private_ipv4_validator(ip_address) is True


@pytest.mark.parametrize(
    "ip_address",
    [
        "216.58.194.174",
        "104.16.249.249",
        "151.101.1.69",
        "72.21.215.90",
        "23.21.103.70",
        "8.8.8.8",
        "35.185.44.232",
        "52.216.21.51",
        "54.174.175.25",
        "128.14.130.240",
    ],
)
def test_not_private_ipv4(ip_address):
    assert private_ipv4_validator(ip_address) is False


@pytest.mark.parametrize(
    "ip_address",
    [
        "fd93:da9f:6c81:99a8:f2a2:cea2:cf22:3541",
        "fc3d:3b9c:e977:44f3:8a81:3a34:cb5f:8127",
        "fd53:2eb9:9e4b:cfcc:db4d:4d4d:72b5:ec32",
        "fe96:1cb9:9294:2d4f:d4ad:ba4d:4c26:583e",
        "fdc6:19b9:ef5b:de5c:8d3a:5d5a:ea7e:7025",
        "febb:9a9f:57c8:8f48:2d2d:d1a1:b1c6:8d28",
        "fd10:fc6e:fc80:8f6d:fc6e:fc6e:fc6e:fc6e",
        "fec9:a7f6:8a99:b2e2:f1b6:a1a6:8c22:3f3d",
        "fd00:6f8c:fe0e:23d1:17c2:8e84:b129:9d9d",
        "fdfa:86db:bad7:adad:efce:7f18:8dbf:7bb9",
    ],
)
def test_private_ipv6(ip_address):
    assert private_ipv6_validator(ip_address) is True


@pytest.mark.parametrize(
    "ip_address",
    [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2606:4700:3030:0000:0000:0000:681c:c246",
        "2a03:2880:f21a:83:face:b00c:0:25de",
        "2001:4860:4860::8888",
        "2a00:1450:4001:818::2003",
        "2607:f8b0:4004:080a:0000:0000:0000:2004",
        "2a01:4f8:221:6104::1",
        "2001:678:4c0:bc5c::1",
        "2001:470:1f15:7a0:beee:7eff:fe5c:c82f",
        "2a02:1205:c68b:2530:58e8:8c32:f001:96e9",
    ],
)
def test_not_private_ipv6(ip_address):
    assert private_ipv6_validator(ip_address) is False


@pytest.mark.parametrize(
    "ip_address",
    [
        "10.40.101.123",
        "192.168.0.44",
        "172.19.104.32",
        "10.20.30.40",
        "192.168.1.100",
        "febb:9a9f:57c8:8f48:2d2d:d1a1:b1c6:8d28",
        "fd10:fc6e:fc80:8f6d:fc6e:fc6e:fc6e:fc6e",
        "fec9:a7f6:8a99:b2e2:f1b6:a1a6:8c22:3f3d",
        "fd00:6f8c:fe0e:23d1:17c2:8e84:b129:9d9d",
        "fdfa:86db:bad7:adad:efce:7f18:8dbf:7bb9",
    ],
)
def test_private_ip(ip_address):
    assert private_ip_validator(ip_address) is None


@pytest.mark.parametrize(
    "ip_address",
    [
        "216.58.194.174",
        "104.16.249.249",
        "151.101.1.69",
        "72.21.215.90",
        "23.21.103.70",
        "2001:4860:4860::8888",
        "2a00:1450:4001:818::2003",
        "2607:f8b0:4004:080a:0000:0000:0000:2004",
        "2a01:4f8:221:6104::1",
        "2001:678:4c0:bc5c::1",
    ],
)
def test_not_private_ip(ip_address):
    with pytest.raises(Forbidden):
        private_ip_validator(ip_address)
