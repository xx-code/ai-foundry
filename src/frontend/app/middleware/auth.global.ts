import { useAuth } from "~/composables/auth"

export default defineNuxtRouteMiddleware(async (to) => {
    const { isAuthenticated } = useAuth()
    const isAuth = await isAuthenticated() 

    if (isAuth && (to.path == '/login' || to.path == '/register')) return navigateTo('/', { replace: true })
    if (!isAuth && (to.path !== `/login` && to.path  !== `/register`)) return navigateTo(`/login`, { replace: true })
    
})