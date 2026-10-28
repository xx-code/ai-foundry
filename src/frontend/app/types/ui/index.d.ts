import type { CreatedResponse, ListResponse, WelcomeResponse } from "../api";

export interface Welcome extends WelcomeResponse {};

export interface Created extends CreatedResponse {}

export interface List<T> extends ListResponse<T> {}