export type AskChatModelRequest = {
    message: string
    session_id: string
}

export type ChatModelResponse = {
    response: any
    usage_metadata: any
    session_id: string
    tool_usage?: any
}