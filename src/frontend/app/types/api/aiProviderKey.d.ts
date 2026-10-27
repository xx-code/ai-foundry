export type AddAiProviderKeyRequest = {
    name: string
    api_key: string
    provider: string
}

export type AiProviderKeyResponse  = {
    id: string
    name: string
    provider: string
    api_key: string
}