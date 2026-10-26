// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  modules: ['@nuxt/ui'],
  css: [
    '@/assets/css/main.css'
  ], 
  app: {
    pageTransition: { name: 'page', mode: 'out-in'},
  },
  routeRules: {
    '/login': { appLayout: false },
    '/register': { appLayout: false }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000' 
    }
  }
})
