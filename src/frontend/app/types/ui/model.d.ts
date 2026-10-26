export interface ModelParams {
    temperature: number
    maxTokens: number
    reasoning: ModelReasoningType 
}

export interface ModelTool {
    id: string
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

export interface TableModel {
    id: string
    name: string
    provider: string
    createdAt: Date
}

