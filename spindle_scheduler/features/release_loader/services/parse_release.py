import hashlib
import json
import uuid

from spindle_scheduler.domains import ContextLoad, Release

from ..domains import RawRelease


def calculate_release_hash(release_id: uuid.UUID, load_id: uuid.UUID) -> str:
    return hashlib.md5(
        json.dumps(
            {"release_id": release_id.hex, "load_id": load_id.hex}
        ).encode()
    ).hexdigest()


def parse_release(
    raw_release: RawRelease, context_load: ContextLoad
) -> Release:
    release_hash = calculate_release_hash(
        raw_release.id, load_id=context_load.id
    )
    return Release.parse_obj(
        {
            **raw_release.dict(),
            **{"hash": release_hash, "context_load": context_load},
        }
    )
