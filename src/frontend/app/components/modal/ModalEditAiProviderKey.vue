<script setup lang="ts">
import { API_ROUTES } from '~/shared/routes'
import type { AiProviderKey } from '~/types/ui/aiProviderKey'

const props = defineProps<{
    aiKey?: AiProviderKey
    onClose?: (doRefresh: boolean) => void
}>()

const form = ref({
    name: props.aiKey?.name ?? '',
    api_key: props.aiKey?.apiKey ?? ''
})

const loading = ref(false)

async function onSubmit() {
    if (!props.aiKey?.id) return
    loading.value = true
    try {
        await ApiLinkBuilder.route(API_ROUTES.AI_PROVIDER_KEYS.UPDATE)
            .params({ id: props.aiKey.id })
            .body({ name: form.value.name, api_key: form.value.api_key })
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
    <UModal title="Modifier la clé API fournisseur">
        <template #body>
            <UForm :state="form" @submit="onSubmit" class="space-y-4">
                <UFormField label="Nom" name="name">
                    <UInput v-model="form.name" />
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
