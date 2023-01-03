import hashlib
import json
import uuid

from spindle_scheduler.domains import Release

from ..domains import RawRelease


def calculate_release_hash(release_id: uuid.UUID, load_id: uuid.UUID) -> str:
    return hashlib.md5(
        json.dumps(
            {"release_id": release_id.hex, "load_id": load_id.hex}
        ).encode()
    ).hexdigest()


def parse_release(raw_release: RawRelease, load_id: uuid.UUID) -> Release:
    release_hash = calculate_release_hash(raw_release.id, load_id=load_id)
    return Release.parse_obj({**raw_release.dict(), **{"hash": release_hash}})
