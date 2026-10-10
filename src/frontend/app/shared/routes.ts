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
        }
    }
} satisfies Record<string, Record<string, ApiRouteDefinition>>