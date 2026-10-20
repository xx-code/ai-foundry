import hashlib
import time

from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import ListDto
from backend.domain.enums.ai_provider import AiProvider
from backend.domain.exception import NotFoundException
from google import genai
from openai import OpenAI

CACHE_TTL_SECONDS = 300
_PROVIDER_MODEL_CACHE: dict[tuple[str, str], tuple[float, ListDto[AiProviderModelDto]]] = {}


class OpenAiModelAdapter:

    def list(self, api_key: str) -> ListDto[AiProviderModelDto]:
        client = OpenAI(api_key=api_key)
        page = client.models.list()
        models = getattr(page, "data", []) or []

        items = [
            AiProviderModelDto(
                model_id=getattr(model, "id", str(model)),
                type=getattr(model, "type", getattr(model, "object", "MODEL")),
                input_price="",
                output_price="",
            )
            for model in models
        ]
        return ListDto(items=items, total=len(items))

    def exist_model(self, api_key: str, model_id: str) -> bool:
        if not model_id or not model_id.strip():
            return False

        normalized_model_id = model_id.strip().lower()
        models = self.list(api_key=api_key).items
        return any(
            model.model_id is not None and model.model_id.strip().lower() == normalized_model_id
            for model in models
        )


class GoogleModelAdapter:
    def list(self, api_key: str) -> ListDto[AiProviderModelDto]:
        client = genai.Client(api_key=api_key)
        response = client.models.list()
        models = getattr(response, "models", None)
        if models is None:
            models = getattr(response, "data", None)
        if models is None:
            models = list(response)
        if isinstance(models, dict):
            models = models.get("models", [])

        items = []
        for model in models:
            model_id = (
                getattr(model, "name", None)
                or getattr(model, "model", None)
                or getattr(model, "id", None)
                or str(model)
            )
            model_type = getattr(model, "type", None) or getattr(model, "display_name", None) or "MODEL"
            items.append(
                AiProviderModelDto(
                    model_id=str(model_id),
                    type=str(model_type),
                    input_price="",
                    output_price="",
                )
            )

        return ListDto(items=items, total=len(items))

    def exist_model(self, api_key: str, model_id: str) -> bool:
        if not model_id or not model_id.strip():
            return False

        normalized_model_id = model_id.strip().lower()
        models = self.list(api_key=api_key).items
        return any(
            model.model_id is not None and model.model_id.strip().lower() == normalized_model_id
            for model in models
        )


class FactoryProviderAiModelRepository(ProviderAiModelRepository):
    def list_model(self, input: ListAiProviderModelDto) -> ListDto[AiProviderModelDto]:
        key = hashlib.sha256(input.api_key.encode("utf-8")).hexdigest()
        cache_key = (input.provider.value, key)
        now = time.monotonic()

        expired_keys = [
            key for key, (cached_at, _) in _PROVIDER_MODEL_CACHE.items()
            if now - cached_at > CACHE_TTL_SECONDS
        ]
        for key in expired_keys:
            _PROVIDER_MODEL_CACHE.pop(key, None)

        cached_result = _PROVIDER_MODEL_CACHE.get(cache_key)
        if cached_result is not None:
            return cached_result[1]

        if input.provider == AiProvider.GOOGLE:
            adapter = GoogleModelAdapter()
            result = adapter.list(api_key=input.api_key)
        elif input.provider == AiProvider.OPEN_AI:
            adapter = OpenAiModelAdapter()
            result = adapter.list(api_key=input.api_key)
        else:
            raise NotFoundException("AI_PROVIDER_NOT_IMPLEMENTED", "This provider is not implemented")

        _PROVIDER_MODEL_CACHE[cache_key] = (now, result)
        return result

    def exist_model(self, input: ListAiProviderModelDto, model_id: str) -> bool:
        if not model_id or not model_id.strip():
            return False

        normalized_model_id = model_id.strip().lower()
        models = self.list_model(input).items
        return any(
            model.model_id.strip().lower() == normalized_model_id
            for model in models
            if model.model_id
        )

    