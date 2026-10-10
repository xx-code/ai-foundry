import type { UserReponse } from "../api/user";

export interface User extends Omit<UserReponse, 'user_name'> {
    username: string
}