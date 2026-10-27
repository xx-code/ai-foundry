import type { AiProviderKeyResponse } from "~/types/api/aiProviderKey";
import type { AiProviderKey } from "~/types/ui/aiProviderKey";

export function toAiProviderKey(data: AiProviderKeyResponse): AiProviderKey {
    return {
        id: data.id,
        name: data.name,
        provider: data.provider,
        apiKey: data.api_key
    }
}
