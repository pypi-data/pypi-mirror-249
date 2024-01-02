import asyncio
import json
from dataclasses import dataclass
from typing import Dict, Generator, Literal, Optional

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource
from botfleet.resources._base import Resource
from botfleet.resources.execution import Execution


@dataclass
class BotExecutorCronJob(Resource):
    id: str
    bot_id: str
    name: str
    status: Literal["suspended", "running"]
    expression: str
    execution_stream_address: str
    created: str
    modified: str

    @classmethod
    def api_source(cls):
        return "bot-executor-cron-jobs"

    @classmethod
    def list(
        cls, bot_id: Optional[str] = None, page: int = 1, page_size: int = 10
    ) -> PagePaginatedResource["BotExecutorCronJob"]:
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
    def retrieve(cls, id: str) -> "BotExecutorCronJob":
        r = Client.request_action("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())

    @classmethod
    def create(cls, bot_id: str, name: str, expression: str) -> "BotExecutorCronJob":
        r = Client.request_action(
            "POST",
            f"{cls.api_source()}/create/",
            data={"bot_id": bot_id, "name": name, "expression": expression},
        )
        return cls(**r.json())

    @classmethod
    def update(cls, id: str, **kwargs) -> "BotExecutorCronJob":
        """
        The following fields can be updated: `name`, `status`.
        """

        r = Client.request_action(
            "PATCH", f"{cls.api_source()}/{id}/update/", data=kwargs
        )
        return cls(**r.json())

    @classmethod
    def delete(cls, id: str) -> None:
        Client.request_action("DELETE", f"{cls.api_source()}/{id}/delete/")

    def stream(self) -> Generator[Execution, None, None]:
        """
        Allows you to stream the executions of a cron job. Example:

        ```
        cron_job = BotExecutorCronJob.retrieve("8f66911b-ed13-4dc4-beaa-38a1e5732bdd")
        for execution in cron_job.stream():
             print(execution)
        ```
        """

        async def async_stream_executions():
            async for message in Client.listen_to_execution_stream(
                self.execution_stream_address
            ):
                yield Execution(**json.loads(message))

        def run():
            async_gen = async_stream_executions()
            try:
                while True:
                    yield asyncio.get_event_loop().run_until_complete(
                        async_gen.__anext__()
                    )
            except KeyboardInterrupt:
                ...

        return run()
