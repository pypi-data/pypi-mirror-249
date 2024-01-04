import json
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, create_model
from scale_egp.cli.formatter import Markdownable
from scale_egp.sdk.enums import ModelVendor, ModelType
from scale_egp.sdk.types.model_templates import ModelTemplate
from scale_egp.sdk.types.models import (
    Model, ParameterSchema, ParameterSchemaModelConfig,
    parameter_schema_to_model, BaseModelRequest,
)
from scale_egp.sdk.constants.model_schemas import MODEL_SCHEMAS


class ModelDescription(BaseModel, Markdownable):
    model_instance: Model
    model_template: ModelTemplate

    def _get_request_schema(self) -> Dict[str, Any]:
        return get_full_request_schema(
            self.model_template.model_type,
            self.model_template.model_request_parameters_schema,
        ).schema()

    def _get_description_dict(self) -> Dict[str, Any]:
        return {
            "model_instance": json.loads(self.model_instance.json()),
            "model_template": json.loads(self.model_template.json()),
        }

    def to_markdown(self) -> str:
        return (
            f"# {self.model_instance.name} (id: {self.model_instance.id})\n"
            f"\n"
            f"*type*: {self.model_template.model_type.value}\n"
            f"*status*: {self.model_instance.status}\n"
            f"*vendor*: {(self.model_instance.model_vendor or ModelVendor.LAUNCH).value}\n"
            f"\n"
            f"{self.model_instance.description or ''}\n"
            f"## Model request schema\n"
            f"```\n"
            f"{json.dumps(self.model_instance.request_schema, indent=2)}\n"
            f"```\n"
            f"## Model response schema\n"
            f"```\n"
            f"{json.dumps(self.model_instance.response_schema, indent=2)}\n"
            f"```\n"
        )

    def json(self, **dumps_kwargs: Any) -> str:
        return json.dumps(self._get_description_dict(), **dumps_kwargs)


def get_full_request_schema(
    model_type: ModelType,
    model_request_parameter_schema: Optional[ParameterSchema] = None,
) -> Type[BaseModelRequest]:
    # dynamically construct Pydantic model which fully describes the model request schema
    # including the model_request_parameters field if it is used by the model.
    request_schema = create_model(
        MODEL_SCHEMAS[model_type][0].__name__,
        __config__=ParameterSchemaModelConfig,
    )
    # copy over all fields except model_request_parameters
    fields = {
        field_name: field_info
        for field_name, field_info in MODEL_SCHEMAS[model_type][0].__fields__.items()
        if field_name != "model_request_parameters"
    }
    if model_request_parameter_schema and len(model_request_parameter_schema.parameters) > 0:
        request_parameter_schema_cls = parameter_schema_to_model(
            "model_request_parameter_schema",
            model_request_parameter_schema,
        )
        fields["model_request_parameters"] = (request_parameter_schema_cls, ...)
    else:
        # permit an empty model_request_parameters to be sent since pydantic will send it automatically
        fields["model_request_parameters"] = BaseModelRequest.__fields__["model_request_parameters"]

    request_schema.__fields__ = fields
    return request_schema
