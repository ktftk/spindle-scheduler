import hashlib
import json
import uuid

from spindle_scheduler import Release

from ..domains import ReleaseResource


def calculate_release_hash(release_id: uuid.UUID, load_id: uuid.UUID) -> str:
    return hashlib.md5(
        json.dumps(
            {"release_id": release_id.hex, "load_id": load_id.hex}
        ).encode()
    ).hexdigest()


def create_release(
    release_resource: ReleaseResource, load_id: uuid.UUID
) -> Release:
    release_hash = calculate_release_hash(release_resource.id, load_id=load_id)
    return Release.parse_obj(
        {**release_resource.dict(), **{"hash": release_hash}}
    )
