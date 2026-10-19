from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import ListDto
from backend.domain.enums.ai_provider import OnlineAiProvider
from backend.domain.exception import NotFoundException

class OpenAiModelAdapter:
    def list(self) -> ListDto[AiProviderModelDto]:
        ...

class GoogleModelAdapter: 
    def list(self) -> ListDto[AiProviderModelDto]:
        ...


class ModelAdapterFactory(ProviderAiModelRepository):
    def list_model(self, input: ListAiProviderModelDto) -> ListDto[AiProviderModelDto]:
        if input.provider == OnlineAiProvider.GOOGLE:
            adapter = GoogleModelAdapter()
            return adapter.list()
        elif input.provider == OnlineAiProvider.OPEN_AI:
            adapter = OpenAiModelAdapter()
            return adapter.list()
        else:
            raise NotFoundException("AI_PROVIDER_NOT_IMPLEMENTED", "This provider is not implemented")

    def exist_model(self, model_id: str) -> bool:
        raise NotImplementedError

    