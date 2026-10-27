import type { McpClientApp, McpClientAuthType } from "~/shared/constants/mcpClient"

export interface UserMcpServerCred {
    apiKey?: string
}

export interface UserMcpServer {
    id: string
    app: string
    cred: UserMcpServerCred
}

export type McpClientToolResponse = {
    app: McpClientApp
    authType: McpClientAuthType
}