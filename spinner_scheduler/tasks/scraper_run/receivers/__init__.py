from ..domains import ReleaseReceiverBase
from .economy import jp

RECEIVERS = {
    "economy.jp.ews.main": jp.EWSReciever,
}


def get_receiver(name: str) -> ReleaseReceiverBase:
    receiver_class = RECEIVERS[name]
    return receiver_class()
