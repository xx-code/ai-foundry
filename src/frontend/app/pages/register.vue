<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui'
import { API_ROUTES } from '~/shared/routes'
import type { FormRegister } from '~/types/ui/auth'

const loginForm = reactive<FormRegister>({
    email: '',
    username: '',
    password: '',
})
const confirmPassword = ref('')
const loading = ref(false)

const toast = useToast()

const fieldUi = {
    label: 'text-[10px] font-bold uppercase tracking-wider text-neutral-900',
    error: 'mt-1 text-[11px] font-medium text-red-600'
}

function validate(state: Partial<FormRegister>): FormError[] {
    const errors: FormError[] = []

    if (!state.email?.trim())
        errors.push({ name: 'emailOrUsername', message: 'Email ou nom d\'utilisateur requis' })

    if (!state.password?.trim())
        errors.push({ name: 'password', message: 'Mot de passe requis' })

    if (!state.username?.trim())
        errors.push({ name: 'username', message: 'Username requis'})

    if (confirmPassword.value !== state.password)
        errors.push({ name: 'confirmPasssword', message: 'Username requis'})

    return errors
}

async function onSubmit(event: FormSubmitEvent<FormRegister>) {
    loading.value = true
    const data = event.data
    try {
        await ApiLinkBuilder
            .route(API_ROUTES.AUTH.REGISTER)
            .body(data)
            .execute()

        navigateTo('/login')
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
        <UiAuthLeadLayout />

        <div class="h-full flex justify-center items-center">
            <UForm class="w-80" :state="loginForm" :validate="validate" @submit="onSubmit">
                <div class="anim-slide-up" style="--delay: 200ms">
                    <h2 class="text-2xl font-bold text-neutral-900 font-display">Creer un compte</h2>
                    <p class="text-xs text-neutral-500 mt-0.5">Accède à ton atelier de modèles.</p>
                </div>

                <div class="mt-8 space-y-4">
                    <UFormField
                        name="email"
                        label="Email"
                        :ui="fieldUi"
                        class="anim-slide-up"
                        style="--delay: 320ms"
                    >
                        <UiAuthInput
                            v-model="loginForm.email"
                            type="text"
                            autocomplete="email"
                            placeholder="leaf@foundry.local"
                        />
                    </UFormField>

                    <UFormField
                        name="username"
                        label="Username"
                        :ui="fieldUi"
                        class="anim-slide-up"
                        style="--delay: 320ms"
                    >
                        <UiAuthInput
                            v-model="loginForm.username"
                            type="text"
                            autocomplete="username"
                            placeholder="username"
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

                    <UFormField
                        name="confirmPassword"
                        label="Confirmer le mot de passe"
                        :ui="fieldUi"
                        class="anim-slide-up"
                        style="--delay: 420ms"
                    >
                        <UiAuthInput
                            v-model="confirmPassword"
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
                        {{ loading ? 'Enregistrer' : 'S\' enregister' }}
                        <span
                            v-if="!loading"
                            class="inline-block transition-transform duration-200 group-hover:translate-x-1"
                        >→</span>
                        <span v-else class="size-3 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                    </span>
                </button>
            </UForm>
        </div>
    </div>
</template>