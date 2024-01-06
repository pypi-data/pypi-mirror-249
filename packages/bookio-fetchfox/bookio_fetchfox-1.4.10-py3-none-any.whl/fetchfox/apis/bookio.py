from typing import Iterable

from fetchfox import rest

BASE_URL = "https://api.book.io"


def get_campaigns() -> Iterable[dict]:
    response, status_code = rest.get(
        f"{BASE_URL}/treasury/v2/campaigns/all",
    )

    yield from response
