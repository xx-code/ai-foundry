export type AddUserMcpServerRequest = {
    app: string
    api_key: string
}

export type UpdateUserMcpServerRequest = {
    api_key: string
}

export type UserMcpServerCredResponse = {
    api_key?: string
}

export type UserMcpServerResponse = {
    id: string
    app: string
    cred: UserMcpServerCredResponse
}

export type McpClientToolResponse = {
    app: string
    auth_type: string
}