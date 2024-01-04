from typing import Optional, Literal, Iterable

from scale_egp.sdk.types.completions import CompletionRequest, Completion, ModelParameters
from scale_egp.utils.api_utils import APIEngine


class CompletionCollection(APIEngine):

    _sub_path = "v2/completions"

    def create(
        self,
        model: Literal[
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613",
            "text-davinci-003",
            "text-davinci-002",
            "text-curie-001",
            "text-babbage-001",
            "text-ada-001",
        ],
        prompt: str,
        model_parameters: Optional[ModelParameters] = None,
    ) -> Completion:
        """
        Create a new LLM Completion.

        Args:
            model: The model to use for the completion.
            prompt: The prompt to use for the completion.
            model_parameters: The parameters to use for the model.

        Returns:
            The newly created Completion.
        """
        response = self._post(
            sub_path=self._sub_path,
            request=CompletionRequest(
                model=model,
                prompt=prompt,
                model_parameters=model_parameters,
            ),
        )
        return Completion.from_dict(response.json())

    def stream(
        self,
        model: Literal[
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613",
            "text-davinci-003",
            "text-davinci-002",
            "text-curie-001",
            "text-babbage-001",
            "text-ada-001",
        ],
        prompt: str,
        model_parameters: Optional[ModelParameters] = None,
    ) -> Iterable[Completion]:
        """
        Stream LLM Completions.

        Returns:
            The newly created Completion.
        """
        iterable_payloads = self._post_stream(
            sub_path=self._sub_path,
            request=CompletionRequest(
                model=model,
                prompt=prompt,
                model_parameters=model_parameters,
                stream=True,
            ),
        )
        if iterable_payloads:
            for response_dict in iterable_payloads:
                yield Completion.from_dict(response_dict)
        else:
            return []
