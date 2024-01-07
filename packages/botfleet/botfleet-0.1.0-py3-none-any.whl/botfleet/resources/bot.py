import asyncio
import json
from dataclasses import dataclass
from typing import Literal, Optional, Union

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource
from botfleet.resources._base import Resource
from botfleet.resources.bot_executor_job import BotExecutorJob
from botfleet.resources.bot_template import BotTemplate
from botfleet.resources.execution import Execution
from botfleet.types import JSON


@dataclass
class Bot(Resource):
    id: str
    name: str
    script: str
    requirements: str
    env_vars: str
    python_version: Literal["3.9", "3.10", "3.11", "3.12"]
    store_id: str
    created: str
    modified: str

    @classmethod
    def api_source(cls):
        return "bots"

    @classmethod
    def list(cls, page: int = 1, page_size: int = 10) -> PagePaginatedResource["Bot"]:
        params = {"page": page, "page_size": page_size}
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
    def retrieve(cls, id: str) -> "Bot":
        r = Client.request_action("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())

    @classmethod
    def create(
        cls,
        name: str,
        script: str,
        python_version: Literal["3.9", "3.10", "3.11", "3.12"],
        store_id: str,
        requirements: str = "",
        env_vars: str = "",
    ) -> "Bot":
        r = Client.request_action(
            "POST",
            f"{cls.api_source()}/create/",
            data={
                "name": name,
                "script": script,
                "requirements": requirements,
                "env_vars": env_vars,
                "python_version": python_version,
                "store_id": store_id,
            },
        )
        return cls(**r.json())

    @classmethod
    def create_from_template(
        cls,
        template_id: str,
        store_id: str,
        name: Optional[str] = None,
        script: Optional[str] = None,
        python_version: Optional[Literal["3.9", "3.10", "3.11", "3.12"]] = None,
        requirements: Optional[str] = None,
        env_vars: Optional[str] = None,
    ) -> "Bot":
        """
        Allows overriding the following fields: `name`, `script`, `requirements`,
        `env_vars`, `python_version`.
        """
        bot_template = BotTemplate.retrieve(template_id)

        name = name if name is not None else bot_template.name
        script = script if script is not None else bot_template.script
        requirements = (
            requirements if requirements is not None else bot_template.requirements
        )
        env_vars = env_vars if env_vars is not None else bot_template.env_vars
        python_version = (
            python_version
            if python_version is not None
            else bot_template.python_version
        )

        r = Client.request_action(
            "POST",
            f"{cls.api_source()}/create/",
            data={
                "name": name,
                "script": script,
                "requirements": requirements,
                "env_vars": env_vars,
                "python_version": python_version,
                "store_id": store_id,
            },
        )
        return cls(**r.json())

    @classmethod
    def update(cls, id: str, **kwargs) -> "Bot":
        """
        The following fields can be updated: `name`, `script`, `requirements`,
        `env_vars`, `python_version`, `store_id`.
        """

        r = Client.request_action(
            "PATCH", f"{cls.api_source()}/{id}/update/", data=kwargs
        )
        return cls(**r.json())

    @classmethod
    def delete(cls, id: str) -> None:
        Client.request_action("DELETE", f"{cls.api_source()}/{id}/delete/")

    def execute(
        self, payload: JSON = None, wait: bool = True
    ) -> Union[Execution, BotExecutorJob]:
        """
        Returns an `Execution` object if `wait` is `True`, otherwise returns a
        `BotExecutorJob` object.
        """
        job = BotExecutorJob.create(bot_id=self.id, payload=payload)

        if not wait:
            return job

        ret = asyncio.get_event_loop().run_until_complete(
            Client.listen_to_execution(job.execution_address)
        )
        return Execution(**json.loads(ret))
