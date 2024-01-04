from sensenova import error
from sensenova.api_resources.abstract import EngineAPIResource


class Embedding(EngineAPIResource):
    OBJECT_NAME = "llm.embeddings"

    @classmethod
    def create(cls, *args, **kwargs):
        embeddings_input = kwargs.get("input", None)
        if not embeddings_input:
            raise error.InvalidRequestError(
                "The parameter input is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        embeddings_input = kwargs.get("input", None)
        if not embeddings_input:
            raise error.InvalidRequestError(
                "The parameter input is required"
            )
        model = kwargs.get("model", None)
        if not model:
            raise error.InvalidRequestError(
                "The parameter model is required"
            )

        return await super().acreate(*args, **kwargs)
