from dataclasses import dataclass
from typing import Dict, Optional

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource
from botfleet.resources._base import Resource


@dataclass
class BotBuilderJob(Resource):
    id: str
    bot_id: str
    created: str

    @classmethod
    def api_source(cls):
        return "bot-builder-jobs"

    @classmethod
    def list(
        cls, bot_id: Optional[str] = None, page: int = 1, page_size: int = 10
    ) -> PagePaginatedResource["BotBuilderJob"]:
        params: Dict = {"page": page, "page_size": page_size}
        if bot_id is not None:
            params["bot_id"] = bot_id
        r = Client.request_action("GET", f"{cls.api_source()}/", params=params)
        return PagePaginatedResource(
            _next_url=r.json()["next"],
            _previous_url=r.json()["previous"],
            _resource_class=cls,
            total_count=r.json()["total_count"],
            current_page=r.json()["current_page"],
            results=[cls(**result) for result in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "BotBuilderJob":
        r = Client.request_action("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())
