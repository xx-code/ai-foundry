export interface AskChatModel {
    message: string
    sessionId: string
}

export interface ChatModel {
    response: any
    usageMetadata: object
    sessionId: string
    toolUsage?: object
}