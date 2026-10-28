import type { ListResponse } from "~/types/api";
import type { ModelResponse } from "~/types/api/model";
import type { List } from "~/types/ui";
import type { Model, ModelTableItem } from "~/types/ui/model";

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
            name: tool.name,
            toolId: tool.tool_id,
            toolType: tool.tool_type
        }))
    }
}

export function toListModels(data: ListResponse<ModelResponse>): List<Model> {
    return {
        items: data.items.map(i => toModel(i)),
        total: data.total
    }
}

export function toListModelCards(data: Model[]): ModelTableItem[] {
    return data.map(i => ({
        id: i.id,
        name: i.name,
        model: i.providerModel,
        provider: i.providerKeyId,
        createdAt: new Date()
    } satisfies ModelTableItem))
}