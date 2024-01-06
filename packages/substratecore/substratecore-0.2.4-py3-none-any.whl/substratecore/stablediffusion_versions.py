from .pydantic_models import (
    StableDiffusionIn,
    StableDiffusionOut,
    ErrorOut,
    StableDiffusionImage,
)
from .versions import ToIn, FromOut
from typing import Dict, Any, Optional, Union, List
from pydantic import ValidationError


def sd_in_2023_12_26(json: Dict[str, Any]) -> Dict[str, Any]:
    # use_hosted_url -> store
    # return_base64 -> store
    # n -> num_images
    result = {
        **{
            k: v
            for k, v in json.items()
            if not k in ["use_hosted_url", "return_base64", "n"]
        },
    }
    if json.get("use_hosted_url") != None:
        result["store"] = json.get("use_hosted_url")
    if json.get("return_base64") != None:
        result["store"] = not json.get("return_base64")
    if json.get("n") != None:
        result["num_images"] = json.get("n")
    # image urls -> nested
    if json.get("image_url"):
        result = {
            "image": {
                "image_url": json.get("image_url"),
                "mask_image_url": json.get("mask_image_url"),
                "prompt_strength": json.get("strength"),
            },
            **{
                k: v
                for k, v in result.items()
                if not k in ["image_url", "mask_image_url", "strength"]
            },
        }
    return result


class ToStableDiffusionIn(ToIn[StableDiffusionIn]):
    def from_version(
        self, version: Optional[str]
    ) -> Union[StableDiffusionIn, ErrorOut]:
        versions = {
            "2023-12-26": (lambda x: sd_in_2023_12_26(x)),
        }
        res = self.json
        for date, fn in sorted(versions.items(), key=lambda x: x[0]):
            if version and version < date:
                res = fn(res)

        # Schema-level validation
        model = None
        try:
            model = StableDiffusionIn(**res)
        except ValidationError as e:
            import json

            e_json_str = e.json()
            e_json = json.loads(e_json_str)[0]
            message = f"{e_json.get('msg')}: {e_json.get('loc')}"
            return ErrorOut(type="invalid_request_error", message=message)

        return model
