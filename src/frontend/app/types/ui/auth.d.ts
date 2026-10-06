import type { LoginRequest, RegisterRequest } from "../api/auth";

export interface FormRegister extends Omit<RegisterRequest, 'user_name'> {
    username: string
    external_id?: string = ""
}

export interface FormLogin extends Omit<LoginRequest, 'email_or_user_name'> {
    emailOrUsername: string
}

export interface UserToken {
    token: string
    type: string
}
