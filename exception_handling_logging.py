import functools
import logging
import os
import time

os.system("")  # enable ANSI colours in Windows terminal

LOG_FORMAT = "%(asctime)s,%(msecs)03d | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%H:%M:%S"


class ColorFormatter(logging.Formatter):
    COLORS = {"ERROR": "\033[91m", "WARNING": "\033[93m"}
    RESET = "\033[0m"

    def format(self, record):
        text = super().format(record)
        color = self.COLORS.get(record.levelname)
        return f"{color}{text}{self.RESET}" if color else text


console = logging.StreamHandler()
console.setFormatter(ColorFormatter(LOG_FORMAT, DATE_FORMAT))
file_handler = logging.FileHandler("automation.log", mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
logging.basicConfig(level=logging.DEBUG, handlers=[console, file_handler])

logger = logging.getLogger("main")
retry_logger = logging.getLogger("with_retry")


# Custom exceptions
class BusinessError(Exception):
    """Raised when a business rule is violated."""


class SystemFailure(Exception):
    """Raised for temporary system / network failures."""


def with_retry(max_attempts=3, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(tx_id, *args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(tx_id, *args, **kwargs)
                except SystemFailure as e:
                    retry_logger.warning(f"{tx_id} attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


FLAKY = {"T005", "T006"}
calls = {}


@with_retry(max_attempts=3, delay=0.5)
def fetch_gst_rate(tx_id):
    calls[tx_id] = calls.get(tx_id, 0) + 1
    if tx_id in FLAKY and calls[tx_id] == 1:
        raise SystemFailure("Simulated network timeout")
    return 0.18


def process_transaction(tx_id, amount):
    if amount is None:
        raise BusinessError(f"Amount missing for {tx_id}")
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Amount must be numeric, got {type(amount).__name__}")
    if amount <= 0:
        raise BusinessError(f"Invalid amount {amount} for {tx_id}")
    rate = fetch_gst_rate(tx_id)
    return round(amount * (1 + rate), 2)


transactions = [
    ("T001", 1000),
    ("T002", -50),
    ("T003", None),
    ("T004", "abc"),
    ("T005", 2500),
    ("T006", 750),
]

summary = {"success": 0, "business": 0, "system": 0, "other": 0}
logger.info("=== Process started ===")

for tx_id, amount in transactions:
    try:
        result = process_transaction(tx_id, amount)
    except BusinessError as e:
        summary["business"] += 1
        logger.error(f"Business rule: {e}")
    except SystemFailure as e:
        summary["system"] += 1
        logger.error(f"System failure in {tx_id}: {e}")
    except Exception as e:
        summary["other"] += 1
        logger.error(f"Unexpected error in {tx_id}: {e}")
    else:
        summary["success"] += 1
        logger.info(f"{tx_id} processed. Amount with GST = {result}")
    finally:
        logger.debug(f"Finished handling {tx_id}")

try:
    _ = 10 / 0
except ZeroDivisionError:
    logger.error("Division by zero caught safely")

logger.info(f"=== Process ended === Summary: {summary}")
