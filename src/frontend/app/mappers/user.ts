import type { UserReponse } from "~/types/api/user";
import type { User } from "~/types/ui/user";

export function toUser(data: UserReponse): User {
    return {
        ...data,
        username: data.user_name
    }
}