import type { ModelReasoningType, ModelToolType } from "~/shared/constants/model"

export interface ModelParams {
    temperature: number
    maxTokens: number
    reasoning: ModelReasoningType 
}

export interface ModelTool {
    id: string
    name: string
    toolId: string
    toolType: ModelToolType
}

export interface Model {
    id: string
    name: string
    providerKeyId: string
    providerModel: string
    defaultInstruction?: string
    params: ModelParams
    tools: ModelTool[]
}

export interface ModelTableItem {
    id: string
    name: string
    model: string
    provider: string
    createdAt: Date
}

