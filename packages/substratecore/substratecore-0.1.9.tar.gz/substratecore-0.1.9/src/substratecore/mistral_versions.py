from .pydantic_models import MistralIn, MistralOut, ErrorOut, MistralResult
from .versions import ToIn, FromOut
from typing import Dict, Any, Optional, Union, List
from pydantic import ValidationError


def mistral_in_2023_12_26(json: Dict[str, Any]) -> Dict[str, Any]:
    """
    class TextGenerationArgs(BaseModel):
        prompt: Optional[str] = None
        n: Optional[int] = 1
        prompts: Optional[List[str]] = None
        system: Optional[str] = ""
        temperature: Optional[float] = 0.8
        presence_penalty: Optional[float] = 1.0
        frequency_penalty: Optional[float] = 0.3
        repetition_penalty: Optional[float] = 1.0
        top_p: Optional[float] = 1.0
        max_tokens: Optional[int] = None
    """
    # prompt, prompts -> nested
    result = {}
    maybePrompt = json.get("prompt")
    if maybePrompt:
        result["prompts"] = [{"prompt": maybePrompt}]
    maybePrompts = json.get("prompts")
    if maybePrompts:
        result["prompts"] = list(map(lambda p: {"prompt": p}, maybePrompts))
    maybeInputPrompts = json.get("input_prompts")
    if maybeInputPrompts:
        result["prompts"] = list(map(lambda p: {"prompt": p}, maybeInputPrompts))

    result = {
        **result,
        **{
            k: v
            for k, v in json.items()
            if not k in ["prompt", "prompts", "input_prompts"]
        },
    }
    return result


class ToMistralIn(ToIn[MistralIn]):
    def from_version(self, version: Optional[str]) -> Union[MistralIn, ErrorOut]:
        versions = {
            "2023-12-26": (lambda x: mistral_in_2023_12_26(x)),
        }
        res = self.json
        for date, fn in sorted(versions.items(), key=lambda x: x[0]):
            if version and version < date:
                res = fn(res)

        # Schema-level validation
        model = None
        try:
            model = MistralIn(**res)
        except ValidationError as e:
            import json

            e_json_str = e.json()
            e_json = json.loads(e_json_str)[0]
            message = f"{e_json.get('msg')}: {e_json.get('loc')}"
            return ErrorOut(type="invalid_request_error", message=message)

        return model


def mistral_out_2023_12_26(res: Any) -> Any:
    if isinstance(res, List):
        old_completions = []
        for item in res:
            completions = item.get("completions", [])
            old_completions.extend([{"text": c, "token_count": 0} for c in completions])
        return {
            "completions": old_completions,
            "token_count": 0,
            "input_token_count": 0,
        }
    else:
        return res  # unexpected, no-op


class FromMistralOut(FromOut[Any]):
    def to_version(self, version: Optional[str]) -> Any:
        versions = {
            "2023-12-26": (lambda x: mistral_out_2023_12_26(x)),
        }
        res = self.data
        for date, fn in sorted(versions.items(), key=lambda x: x[0], reverse=True):
            if version and version < date:
                res = fn(res)
        return res
