import { toLoginRequestFormData, toUserToken } from "~/mappers/auth";
import { toUser } from "~/mappers/user";
import { API_ROUTES } from "~/shared/routes";
import type { FormLogin, UserToken } from "~/types/ui/auth";
import type { User } from "~/types/ui/user";

export const useAuth = () => {
    const user = useState<User|null>('auth_user', () => null);

    async function fetchCurrentUser(): Promise<User | null> {
        try {
            user.value = await ApiLinkBuilder.route(API_ROUTES.AUTH.CURRENT_USER)
            .mapper(toUser)
            .execute()
        } catch(e: any) {
            const status = e?.statusCode ?? e?.status
            if (status === 401 || status === 403)
                user.value = null
            else
                throw e
        }
        return user.value
    }

    async function login(form: FormLogin): Promise<void> {
        await ApiLinkBuilder.route(API_ROUTES.AUTH.LOGIN)
            .mapper(toUserToken)
            .formData(toLoginRequestFormData(form))
            .execute()
        await fetchCurrentUser()
    }

    async function isAuthenticated(verify = false): Promise<boolean> {
        if (user.value && !verify) return true
        return (await fetchCurrentUser()) !== null
    }

    async function logout() {
        try {
            await ApiLinkBuilder.route(API_ROUTES.AUTH.LOGOUT).execute()
        } finally {
            user.value = null
            await navigateTo('/login')
        }
    }

    return { login, isAuthenticated, logout, fetchCurrentUser }
}