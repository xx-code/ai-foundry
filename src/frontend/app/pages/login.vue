<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui'
import type { FormLogin } from '~/types/ui/auth'

const loginForm = reactive<FormLogin>({
    emailOrUsername: '',
    password: ''
})
const loading = ref(false)

const toast = useToast()
const { login } = useAuth()

const fieldUi = {
    label: 'text-[10px] font-bold uppercase tracking-wider text-neutral-900',
    error: 'mt-1 text-[11px] font-medium text-red-600'
}

function validate(state: Partial<FormLogin>): FormError[] {
    const errors: FormError[] = []

    if (!state.emailOrUsername?.trim())
        errors.push({ name: 'emailOrUsername', message: 'Email ou nom d\'utilisateur requis' })

    if (!state.password?.trim())
        errors.push({ name: 'password', message: 'Mot de passe requis' })

    return errors
}

async function onSubmit(event: FormSubmitEvent<FormLogin>) {
    loading.value = true
    const data = event.data
    try {
        await login(data)
        navigateTo('/')
    } catch(e: any) {
        toast.add({
            title: 'Connexion Impossible',
            description: 'Identifiants incorrects, réessaie',
            color: 'error'
        })
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="grid grid-cols-2 w-full h-screen bg-[#fff9ec]">
        <!-- Panneau gauche -->
        <UiAuthLeadLayout />

        <!-- Panneau droit -->
        <div class="h-full flex justify-center items-center">
            <UForm class="w-80" :state="loginForm" :validate="validate" @submit="onSubmit">
                <div class="anim-slide-up" style="--delay: 200ms">
                    <h2 class="text-2xl font-bold text-neutral-900 font-display">Connexion</h2>
                    <p class="text-xs text-neutral-500 mt-0.5">Accède à ton atelier de modèles.</p>
                </div>

                <div class="mt-8 space-y-4">
                    <UFormField
                        name="emailOrUsername"
                        label="Email"
                        :ui="fieldUi"
                        class="anim-slide-up"
                        style="--delay: 320ms"
                    >
                        <UiAuthInput
                            v-model="loginForm.emailOrUsername"
                            type="text"
                            autocomplete="username"
                            placeholder="leaf@foundry.local"
                        />
                    </UFormField>

                    <UFormField
                        name="password"
                        label="Mot de passe"
                        :ui="fieldUi"
                        class="anim-slide-up"
                        style="--delay: 420ms"
                    >
                        <UiAuthInput
                            v-model="loginForm.password"
                            type="password"
                            autocomplete="current-password"
                            placeholder="••••••••"
                        />
                    </UFormField> 
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="anim-slide-up group mt-6 w-full py-3 bg-neutral-900 text-white text-xs font-bold tracking-widest uppercase
                           shadow-[4px_4px_0_var(--color-primary-500)]
                           transition-all duration-200 ease-out
                           hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-[6px_6px_0_var(--color-primary-500)]
                           active:translate-x-1 active:translate-y-1 active:shadow-none
                           disabled:opacity-70 disabled:cursor-not-allowed"
                    style="--delay: 540ms"
                >
                    <span class="inline-flex items-center justify-center gap-2">
                        {{ loading ? 'Connexion…' : 'Se connecter' }}
                        <span
                            v-if="!loading"
                            class="inline-block transition-transform duration-200 group-hover:translate-x-1"
                        >→</span>
                        <span v-else class="size-3 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                    </span>
                </button>

                <div class="anim-slide-up mt-3 text-[11px] text-neutral-400" style="--delay: 640ms">
                    <span>Pas de compte ? </span>
                    <NuxtLink
                        to="/register"
                        class="text-primary-500 relative after:absolute after:left-0 after:-bottom-0.5 after:h-px after:w-full
                               after:origin-left after:scale-x-0 after:bg-primary-500 after:transition-transform after:duration-300
                               hover:after:scale-x-100"
                    >
                        Créer un compte
                    </NuxtLink>
                </div>
            </UForm>
        </div>
    </div>
</template>

<style scoped>
/* Animations d'entrée (délai piloté par --delay) */
.anim-slide-up {
    opacity: 0;
    animation: slide-up 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    animation-delay: var(--delay, 0ms);
}
.anim-fade-down {
    opacity: 0;
    animation: fade-down 0.6s ease-out forwards;
}
.anim-pop {
    opacity: 0;
    animation: pop 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    animation-delay: var(--delay, 0ms);
}
.anim-check {
    animation: check 0.5s ease-out 1.3s both;
}

/* La carte flotte doucement en continu */
.float-card {
    animation: float 4s ease-in-out 1.5s infinite;
}

@keyframes slide-up {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fade-down {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pop {
    from { opacity: 0; transform: translateY(30px) scale(0.9); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes check {
    0%   { opacity: 0; transform: scale(0) rotate(-45deg); }
    70%  { transform: scale(1.4) rotate(0); }
    100% { opacity: 1; transform: scale(1) rotate(0); }
}
@keyframes float {
    0%, 100% { translate: 0 0; }
    50%      { translate: 0 -6px; }
}

/* Respect des préférences d'accessibilité */
@media (prefers-reduced-motion: reduce) {
    .anim-slide-up, .anim-fade-down, .anim-pop, .anim-check, .float-card {
        animation: none;
        opacity: 1;
    }
}
</style>