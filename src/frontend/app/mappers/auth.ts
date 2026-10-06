import type { LoginRequest, LoginResponse, RegisterRequest } from "~/types/api/auth";
import type { FormLogin, FormRegister, UserToken } from "~/types/ui/auth";

export function toRegisterRequest(form: FormRegister): RegisterRequest {
    return {
        ...form,
        user_name: form.username,
        external_id: form.external_id ?? ''
    }
}

export function toLoginRequest(form: FormLogin): LoginRequest {
    return {
        ...form,
        email_or_user_name: form.emailOrUsername
    }
}

export function toLoginRequestFormData(form: FormLogin): Record<string, string> {
    return {
        'email_or_user_name': form.emailOrUsername,
        'password': form.password
    }
}

export function toUserToken(data: LoginResponse): UserToken {
    return {
        token: data.access_token,
        type: data.token_type
    }
}