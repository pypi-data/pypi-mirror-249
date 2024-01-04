import json
from typing import Any, Dict, Generator, Generic, Optional, Type, TypeVar
from scale_egp.cli.formatter import (
    FormattingOptions,
    get_formatting_options,
    set_formatting_options,
)
from scale_egp.cli.model_description import ModelDescription
from scale_egp.sdk.client import EGPClient
from scale_egp.sdk.collections.model_templates import ModelTemplateCollection
from scale_egp.sdk.collections.models import ModelCollection
from scale_egp.sdk.types.user_info import UserInfoResponse, get_user_info
from scale_egp.sdk.types.models import Model, ModelRequest
from scale_egp.sdk.types.model_templates import ModelTemplate, ModelTemplateRequest
from scale_egp.sdk.constants.model_schemas import MODEL_SCHEMAS
from scale_egp.utils.api_utils import APIEngine
from scale_egp.utils.model_utils import BaseModel
from argh import CommandError, arg
import fastjsonschema


EntityT = TypeVar("EntityT", bound=BaseModel)
RequestT = TypeVar("RequestT", bound=BaseModel)


def read_json_file(filename: str) -> Any:
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())


class EGPClientFactory:
    def __init__(
        self,
    ):
        self.client: Optional[EGPClient] = None
        self._client_kwargs = None

    def set_client_kwargs(self, **kwargs):
        self._client_kwargs = kwargs

    def get_client(self) -> EGPClient:
        if self.client is None:
            self.client = EGPClient(**self._client_kwargs)
        return self.client


class CollectionCRUDCommands(Generic[EntityT, RequestT]):
    command_group_name = "CRUD"

    def __init__(
        self,
        client_factory: EGPClientFactory,
        entity_type: Type[EntityT],
        request_type: Type[RequestT],
        collection_type: Type[APIEngine],
    ):
        self._client_factory = client_factory
        self._entity_type = entity_type
        self._request_type = request_type
        self._collection_type = collection_type

    def _get_collection_instance(self) -> APIEngine:
        return self._collection_type(self._client_factory.get_client())

    def _transform_entity_json(self, entity_dict: Dict[str, Any]) -> Dict[str, Any]:
        return entity_dict

    def _create(self, request_dict: Any) -> EntityT:
        assert isinstance(request_dict, dict)
        # add client account id if not set in file
        request_dict["account_id"] = request_dict.get(
            "account_id", self._client_factory.get_client().account_id
        )
        request_obj = self._request_type(**request_dict)
        collection = self._get_collection_instance()
        response = collection._post(getattr(collection, "_sub_path"), request_obj)
        assert response.status_code == 200
        response_dict = response.json()
        assert isinstance(response_dict, dict)
        return self._entity_type(**response_dict)

    @arg("filename", help="file to load")
    def create(self, filename: str) -> EntityT:
        request_dict = read_json_file(filename)
        return self._create(request_dict)

    def get(self, id: str) -> EntityT:
        collection = self._get_collection_instance()
        sub_path = f"{collection._sub_path}/{id}"
        response = collection._get(sub_path)
        assert response.status_code == 200
        response_dict = response.json()
        assert isinstance(response_dict, dict)
        return self._entity_type(**response_dict)

    def list(self) -> Generator[EntityT, None, None]:
        formatting_options = get_formatting_options()
        formatting_options.force_list = True
        set_formatting_options(formatting_options)
        collection = self._get_collection_instance()
        response = collection._get(collection._sub_path)
        assert response.status_code == 200
        response_list = response.json()
        assert isinstance(response_list, list)
        # TODO: pagination
        for entity_dict in response_list:
            yield self._entity_type(**entity_dict)


class ModelAliasCommands(CollectionCRUDCommands[Model, ModelRequest]):
    command_group_name = "model"

    def __init__(
        self,
        client_factory: EGPClientFactory,
    ):
        super().__init__(client_factory, Model, ModelRequest, ModelCollection)

    def list(self) -> Generator[EntityT, None, None]:
        set_formatting_options(
            FormattingOptions(
                table_columns=["id", "name", "model_template_id", "created_at", "description"]
            )
        )
        return super().list()

    def describe(self, model_id: str) -> ModelDescription:
        model_alias = self.get(model_id)
        model_template = ModelTemplateCommands(self._client_factory).get(
            model_alias.model_template_id
        )
        return ModelDescription(model_instance=model_alias, model_template=model_template)

    @arg("filename", help="file to load")
    @arg(
        "--model-template-id", help="id of the model template to use if not specified in JSON file"
    )
    def create(self, filename: str, model_template_id: Optional[str] = None) -> EntityT:
        request_dict = read_json_file(filename)
        assert isinstance(request_dict, dict)
        effective_model_template_id = request_dict.get("model_template_id", model_template_id)
        if effective_model_template_id is None:
            raise CommandError(
                "No model template id specified in JSON file or --model-template-id option. Please provide the model template id!"
            )
        request_dict["model_template_id"] = effective_model_template_id
        return self._create(request_dict)

    @arg("filename", help="Model request")
    def validate_request(self, model_id: str, filename: str) -> Optional[str]:
        model_alias = self.get(model_id)
        execute_request_dict = read_json_file(filename)
        validator = fastjsonschema.compile(model_alias.request_schema)
        try:
            validator(execute_request_dict)
        except fastjsonschema.JsonSchemaException as e:
            return f"Data failed validation: {e}"
        return None

    @arg("filename", help="Model request")
    def execute(self, model_id: str, filename: str) -> EntityT:
        model_alias = self.get(model_id)
        model_template = ModelTemplateCommands(self._client_factory).get(
            model_alias.model_template_id
        )
        model_type = model_template.model_type
        model_request_cls, model_response_cls = MODEL_SCHEMAS[model_type]
        request_dict = read_json_file(filename)
        assert isinstance(request_dict, dict)
        request_obj = model_request_cls(**request_dict)
        collection = self._get_collection_instance()
        sub_path = f"{collection._sub_path}/{model_id}/execute"
        response = collection._post(
            sub_path=sub_path,
            request=request_obj,
            timeout=10 * 60,  # 10 minutes
        )
        assert response.status_code == 200
        return model_response_cls(**response.json())


class ModelTemplateCommands(CollectionCRUDCommands[ModelTemplate, ModelTemplateRequest]):
    command_group_name = "model_template"

    def __init__(
        self,
        client_factory: EGPClientFactory,
    ):
        super().__init__(
            client_factory, ModelTemplate, ModelTemplateRequest, ModelTemplateCollection
        )

    def _transform_entity_json(self, entity_dict: Dict[str, Any]) -> Dict[str, Any]:
        if entity_dict.get("vendor_configuration") is not None:
            entity_dict["model_vendor"] = "LLMENGINE"
        return entity_dict

    def list(self) -> Generator[EntityT, None, None]:
        set_formatting_options(
            FormattingOptions(table_columns=["id", "name", "model_type", "created_at"])
        )
        return super().list()

    def show_model_schemas(self):
        return [
            {
                "model_type": model_type.value,
                "request_schema": schemas[0].schema(),
                "response_schema": schemas[1].schema(),
            }
            for (model_type, schemas) in MODEL_SCHEMAS.items()
        ]


class UserCommands:
    command_group_name = "user"

    def __init__(
        self,
        client_factory: EGPClientFactory,
    ):
        self.client_factory = client_factory

    def whoami(self) -> UserInfoResponse:
        client = self.client_factory.get_client()
        return get_user_info(client.httpx_client, client.endpoint_url, client.log_curl_commands)
