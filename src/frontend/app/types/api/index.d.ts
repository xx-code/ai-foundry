export type WelcomeResponse = {
    message: string
}

export type CreatedResponse = {
    id: string
}

export type ListResponse<T> = {
    items: T[]
    total: number
}