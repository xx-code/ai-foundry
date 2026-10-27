import type { AskChatModelRequest, ChatModelResponse } from "~/types/api/chat";
import type { AskChatModel, ChatModel } from "~/types/ui/chat";

export function toAskChatModelRequest(data: AskChatModel): AskChatModelRequest {
    return {
        message: data.message,
        session_id: data.sessionId
    }
}

export function toChatModel(data: ChatModelResponse): ChatModel {
    return {
        response: data.response,
        usageMetadata: data.usage_metadata,
        sessionId: data.session_id,
        toolUsage: data.tool_usage
    }
}
