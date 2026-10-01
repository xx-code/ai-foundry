import type { ApiRouteDefinition } from '~/types/shared/routes';

export const API_ROUTES = {
    ROOT: {
        WELCOME: {
            serverPath: '/api',
            apiPath: '/',
            method: 'GET'
        }
    }
} satisfies Record<string, Record<string, ApiRouteDefinition>>