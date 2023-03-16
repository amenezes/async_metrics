import re
from functools import partial

from async_metrics import logger

private_ipv4_pattern = re.compile(
    r"(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"
)
private_ipv6_pattern = re.compile(
    r"^((fc|fe|fd|FC|FE|FD)[0-9a-f]{2}|::1)(?::[0-9a-f]{1,4}){0,7}$"
)


def _is_private_ip(validator: re.Pattern, ip_address: str) -> bool:
    if validator.match(ip_address):
        return True
    return False


private_ipv4_validator = partial(_is_private_ip, private_ipv4_pattern)
private_ipv6_validator = partial(_is_private_ip, private_ipv6_pattern)


def private_ip_validator(ip_address: str) -> None:
    if not private_ipv4_validator(ip_address) and not private_ipv6_validator(
        ip_address
    ):
        logger.warning(f"Access denied for client: {ip_address}")
        raise Forbidden


class Forbidden(Exception):
    def __init__(
        self,
        message: str = "Access denied, only private addresses are allowed to access the metrics",
    ):
        super().__init__(message)
