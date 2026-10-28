import type { ModelReasoningType, ModelToolType } from "~/shared/constants/model"

export type ModelParamsResponse = {
    temperature: number    
    max_tokens: number
    reasoning: ModelReasoningType
}

export type ModelToolResponse = {
    id: string
    name: string
    tool_id: string
    tool_type: ModelToolType
}

export type ModelResponse = {
    id: string
    provider_key_id: string
    provider_model_id: string
    name: string
    default_instruction: string
    params: ModelParamsResponse
    tools: ModelToolResponse[]
}

export type AiProviderModelResponse = {
    model_id: string
    type: string
}

export type ModelParamsRequest = ModelParamsResponse

export type DepoloyModelRequest = {
    name: string
    provider_key_id: string
    provider_model_id: string
    default_instruction?: string
    params?: ModelParamsRequest
}

export type UpdateModelRequest = {
    name?: string
    default_instruction?: string
    params?: ModelParamsRequest
}

export type AddModelToolRequest = {
    tool_id: string
    tool_type: string
}