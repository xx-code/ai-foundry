import type { ApiRouteDefinition } from '~/types/shared/routes';

export const API_ROUTES = {
    ROOT: {
        WELCOME: {
            serverPath: '/api',
            apiPath: '/',
            method: 'GET'
        },
    },
    AUTH: {
        LOGIN: {
            serverPath: '/api/auth/login',
            apiPath: '/auth/login',
            method: 'POST',
            session: 'create',
            public: true
        },
        LOGOUT: { 
            serverPath: '/api/auth/logout', 
            apiPath: '/auth/logout', 
            method: 'POST', 
            session: 'destroy', 
        },
        CURRENT_USER: {
            serverPath: '/api/auth/me',
            apiPath: '/auth/me',
            method: 'GET'
        },
        REGISTER: {
            serverPath: '/api/auth/register',
            apiPath: '/auth/register',
            method: 'POST',
            public: true
        }
    },
    USER: {
        GET_USER: {
            serverPath: '/api/users',
            apiPath: '/users',
            method: 'GET'
        },
        ADD_API_KEY: {
            serverPath: '/api/ai-provider-keys/add-key',
            apiPath: '/ai-provider-keys/add-key',
            method: 'POST'
        },
        GET_API_KEY: {
            serverPath: '/api/ai-provider-keys/:id',
            apiPath: '/ai-provider-keys/:id',
            method: 'GET'
        }
    },
    MODEL: {
        PROVIDERS: {
            serverPath: '/api/models/providers',
            apiPath: '/models/providers',
            method: 'GET'
        },
        GET_ALL_MODELS: {
            serverPath: '/api/models',
            apiPath: '/models',
            method: 'GET'
        },
        GET_MODEL: {
            serverPath: '/api/models/:id',
            apiPath: '/models/:id',
            method: 'GET'
        },
        DEPLOY_MODEL: {
            serverPath: '/api/models',
            apiPath: '/models',
            method: 'POST'
        },
        UPDATE_MODEL: {
            serverPath: '/api/models/:id',
            apiPath: '/models/:id',
            method: 'PUT'
        },
        DELETE_MODEL: {
            serverPath: '/api/models/:id',
            apiPath: '/models/:id',
            method: 'DELETE'
        },
        ADD_MODEL_TOOL: {
            serverPath: '/api/models/:id/tool',
            apiPath: '/models/:id/tool',
            method: 'PUT'
        },
        REMOVE_MODEL_TOOL: {
            serverPath: '/api/models/:id/tool/:tool_id',
            apiPath: '/models/:id/tool/:tool_id',
            method: 'DELETE'
        }
    },
    MODEL_CHAT: {
        CHAT_ASK: {
            serverPath: '/api/models/chat',
            apiPath: '/models/chat',
            method: 'POST'
        },
        STREAM_CHAT_ASK: {
            serverPath: '/api/models/stream-chat',
            apiPath: '/models/stream-chat',
            method: 'POST'
        }
    },
    USER_MCP_SERVER: {
        LIST_MCP_TOOLS: {
            serverPath: '/api/user-mcp-servers/list-mcp-tools',
            apiPath: '/user-mcp-servers/list-mcp-tools',
            method: 'GET'
        },
        GET_MCP: {
            serverPath: '/api/user-mcp-servers/:id',
            apiPath: '/user-mcp-servers/:id',
            method: 'GET'
        },
        GET_MCPS: {
            serverPath: '/api/user-mcp-servers',
            apiPath: '/user-mcp-servers',
            method: 'GET'
        },
        ADD_MCP: {
            serverPath: '/api/user-mcp-servers',
            apiPath: '/user-mcp-servers',
            method: 'POST'
        },
        PUT_MCP: {
            serverPath: '/api/user-mcp-servers/:id',
            apiPath: '/user-mcp-servers/:id',
            method: 'PUT'
        },
        DELETE_MCP: {
            serverPath: '/api/user-mcp-servers/:id',
            apiPath: '/user-mcp-servers/:id',
            method: 'DELETE'
        }
    }
} satisfies Record<string, Record<string, ApiRouteDefinition>>