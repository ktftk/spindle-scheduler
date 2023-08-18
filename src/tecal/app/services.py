from uuid import UUID

import uuid6


def generate_scrape_id() -> UUID:
    return uuid6.uuid7()
