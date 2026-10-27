import { toAskChatModelRequest, toChatModel } from "~/mappers/chat"
import type { ChatModelResponse } from "~/types/api/chat"
import type { AskChatModel, ChatModel } from "~/types/ui/chat"

// toAskChatModelRequest et toChatModel sont supposés auto-importés (utils/).
export function useModelChat(modelId: MaybeRefOrGetter<string>) {
    async function ask(data: AskChatModel): Promise<ChatModel> {
        // TODO: remplace par ton client API (baseURL, token, etc.)
        const res = await $fetch<ChatModelResponse>(`/models/${toValue(modelId)}/chat`, {
            method: 'POST',
            body: toAskChatModelRequest(data)
        })
        return toChatModel(res)
    }

    return { ask }
}