export type RegisterRequest = {
    email: string
    user_name: string
    external_id: string
    password: string
}

export type LoginRequest = {
    email_or_user_name: string
    password: string
}

export type LoginResponse = {
    access_token: string
    token_type: string
}