<script setup lang="ts">
import { API_ROUTES } from '~/shared/routes'
import type { AddAiProviderKeyRequest } from '~/types/api/aiProviderKey'
import { AiProviderType } from '~/shared/constants/aiProviderKey'

const props = defineProps<{
    onClose?: (doRefresh: boolean) => void
}>()

const form = ref<AddAiProviderKeyRequest>({
    name: '',
    api_key: '',
    provider: AiProviderType.OPEN_AI
})

const loading = ref(false)

const providers = [
    { label: 'OpenAI', value: AiProviderType.OPEN_AI },
    { label: 'Google', value: AiProviderType.GOOGLE }
]

async function onSubmit() {
    loading.value = true
    try {
        await ApiLinkBuilder.route(API_ROUTES.AI_PROVIDER_KEYS.ADD)
            .body(form.value)
            .execute()
        props.onClose?.(true)
    } catch (e) {
        // ignore
    } finally {
        loading.value = false
    }
}

function onCancel() {
    props.onClose?.(false)
}
</script>

<template>
    <UModal title="Ajouter une clé API fournisseur">
        <template #body>
            <UForm :state="form" @submit="onSubmit" class="space-y-4">
                <UFormField label="Nom" name="name">
                    <UInput v-model="form.name" />
                </UFormField>

                <UFormField label="Fournisseur" name="provider">
                    <USelect v-model="form.provider" :items="providers" value-key="value" label-key="label" />
                </UFormField>

                <UFormField label="Clé API" name="api_key">
                    <UInput v-model="form.api_key" type="password" />
                </UFormField>

                <div class="flex items-center justify-end gap-2">
                    <UButton label="Annuler" color="neutral" variant="ghost" @click="onCancel" />
                    <UButton label="Enregistrer" type="submit" color="primary" :loading="loading" />
                </div>
            </UForm>
        </template>
    </UModal>
</template>
