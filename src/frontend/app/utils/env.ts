export function getApiBase(): string {
    const runtimeConfig = useRuntimeConfig()
    return runtimeConfig.public.apiBase
}