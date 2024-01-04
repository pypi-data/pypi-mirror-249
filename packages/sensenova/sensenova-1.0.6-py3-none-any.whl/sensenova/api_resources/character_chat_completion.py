from sensenova import error
from sensenova.api_resources.abstract import EngineAPIResource


class CharacterChatCompletion(EngineAPIResource):
    OBJECT_NAME = "llm.character.chat-completions"

    @classmethod
    def create(cls, *args, **kwargs):
        prompt = kwargs.get("messages", None)
        if not prompt:
            raise error.InvalidRequestError(
                "The parameter messages is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        prompt = kwargs.get("messages", None)
        if not prompt:
            raise error.InvalidRequestError(
                "The parameter messages is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )

        return await super().acreate(*args, **kwargs)
