from sensenova import error
from sensenova.api_resources.abstract import EngineAPIResource


class Completion(EngineAPIResource):
    OBJECT_NAME = "llm.completions"

    @classmethod
    def create(cls, *args, **kwargs):
        prompt = kwargs.get("prompt", None)
        if not prompt:
            raise error.InvalidRequestError(
                "The parameter prompt is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        prompt = kwargs.get("prompt", None)
        if not prompt:
            raise error.InvalidRequestError(
                "The parameter prompt is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )

        return await super().acreate(*args, **kwargs)
