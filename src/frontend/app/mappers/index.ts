import type { WelcomeResponse } from "~/types/api";
import type { Welcome } from "~/types/ui";

export function toWelcome(response: WelcomeResponse): Welcome {
    return response
}