from __future__ import annotations

from typing import Union, Literal, List

from pydantic import Field

from scale_egp.sdk.enums import QuestionType, EvaluationType
from scale_egp.utils.model_utils import BaseModel, RootModel


class CategoricalChoice(BaseModel):
    """
    A choice for a categorical question.

    This is only used in a StudioEvaluationConfig to specify a choice for a  question that will be
    asked to users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        label: The text displayed to annotators for this choice.
        value: The value reported in the TestCaseResult for this question if this choice is
            selected.

            If users would like to track the improvement of a model over time, it is
            recommended to use a numeric value for this field.

            A string value can be used if no ordering is desired.
    """

    label: str
    value: Union[str, int, bool]


class CategoricalQuestion(BaseModel):
    """
    A categorical question.

    This is only used in a StudioEvaluationConfig to specify a question that will be asked to
    users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        question_id: A unique id for this question. Each question_id will be represented as a
            key in the `result` field in the TestCaseResult after an annotation is completed.
            When examining how an application has performed on a specific question, users should
            look at the `result` field in the TestCaseResult for the key with the
            corresponding id.
        question_type: The type of the question.
        title: The text displayed to annotators for this question.
        choices: The choices for the question.
    """

    question_id: str
    question_type: Literal[QuestionType.CATEGORICAL] = QuestionType.CATEGORICAL.value
    title: str
    choices: List[CategoricalChoice]


class DropdownQuestion(BaseModel):
    """
    A dropdown question.

    This is only used in a StudioEvaluationConfig to specify a question that will be asked to
    users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        question_id: A unique id for this question. Each question_id will be represented as a
            key in the `result` field in the TestCaseResult after an annotation is completed.
            When examining how an application has performed on a specific question, users should
            look at the `result` field in the TestCaseResult for the key with the
            corresponding id.
        question_type: The type of the question.
        title: The text displayed to annotators for this question.
        choices: The choices for the question.
    """

    question_id: str
    question_type: Literal[QuestionType.DROPDOWN] = QuestionType.DROPDOWN.value
    title: str
    choices: List[CategoricalChoice]


class FreeTextQuestion(BaseModel):
    """
    A free text question.

    This is only used in a StudioEvaluationConfig to specify a question that will be asked to
    users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        question_id: A unique id for this question. Each question_id will be represented as a
            key in the `result` field in the TestCaseResult after an annotation is completed.
            When examining how an application has performed on a specific question, users should
            look at the `result` field in the TestCaseResult for the key with the
            corresponding id.
        question_type: The type of the question.
        title: The text displayed to annotators for this question.
    """

    question_id: str
    question_type: Literal[QuestionType.FREE_TEXT] = QuestionType.FREE_TEXT.value
    title: str


class Question(RootModel):
    __root__: Union[CategoricalQuestion, DropdownQuestion, FreeTextQuestion] = Field(
        ...,
        discriminator="question_type",
    )


class StudioEvaluationConfig(BaseModel):
    """
    This specifies the configuration for a studio evaluation job.

    Users should use this evaluation config if they intend to do human evaluation through
    [Studio](https://scale.com/studio).

    Attributes:
        evaluation_type: The type of the evaluation.
        studio_project_id: The ID of the Studio project to use for the evaluation.
        questions: The questions to ask users when they are evaluating generated outputs in the
            EGP annotation UI.
    """

    evaluation_type: EvaluationType = EvaluationType.STUDIO
    studio_project_id: str
    questions: List[Question]


EvaluationConfig = StudioEvaluationConfig
