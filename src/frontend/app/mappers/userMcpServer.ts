import type { UserMcpServerResponse } from "~/types/api/userMcpServer";
import type { UserMcpServer } from "~/types/ui/userMcpServer";

export function toUserMcpServer(data: UserMcpServerResponse): UserMcpServer {
    return {
        id: data.id,
        app: data.app,
        cred: {
            apiKey: data.cred.api_key
        }
    }
}
