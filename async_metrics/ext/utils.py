import re

from async_metrics import logger

private_ip_pattern = re.compile(
    r"(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"
)


def private_ip_validator(ip_address: str) -> None:
    if not private_ip_pattern.match(ip_address):
        logger.warning(f"Access denied for client: {ip_address}")
        raise Forbidden


class Forbidden(Exception):
    pass
