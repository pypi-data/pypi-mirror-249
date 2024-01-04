import logging

from spaceone.core.manager import BaseManager
from spaceone.core.connector.space_connector import SpaceConnector

_LOGGER = logging.getLogger(__name__)


class SecretManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_type = self.transaction.get_meta("authorization.token_type")
        self.secret_connector: SpaceConnector = self.locator.get_connector(
            "SpaceConnector", service="secret"
        )

    def get_secret(self, secret_id: str, domain_id: str) -> dict:
        if self.token_type == "SYSTEM_TOKEN":
            return self.secret_connector.dispatch(
                "Secret.get",
                {"secret_id": secret_id},
                x_domain_id=domain_id,
            )
        else:
            return self.secret_connector.dispatch(
                "Secret.get", {"secret_id": secret_id}
            )

    def list_secrets(self, query: dict, domain_id: str) -> dict:
        _LOGGER.debug(f"[list_secrets] token_type: {self.token_type}")
        if self.token_type == "SYSTEM_TOKEN":
            return self.secret_connector.dispatch(
                "Secret.list",
                {"query": query},
                x_domain_id=domain_id,
            )
        else:
            return self.secret_connector.dispatch("Secret.list", {"query": query})

    def get_secret_data(self, secret_id: str, domain_id: str) -> dict:
        return self.secret_connector.dispatch(
            "Secret.get_data",
            {"secret_id": secret_id, "domain_id": domain_id},
        )
