import type { ModelResponse } from "~/types/api/model";
import type { Model } from "~/types/ui/model";

export function toModel(data: ModelResponse): Model {
    return {
        id: data.id,
        name: data.name,
        providerKeyId: data.provider_key_id,
        providerModel: data.provider_model_id,
        defaultInstruction: data.default_instruction,
        params: {
            temperature: data.params.temperature,
            maxTokens: data.params.max_tokens,
            reasoning: data.params.reasoning
        },
        tools: data.tools.map((tool) => ({
            id: tool.id,
            toolId: tool.tool_id,
            toolType: tool.tool_type
        }))
    }
}
