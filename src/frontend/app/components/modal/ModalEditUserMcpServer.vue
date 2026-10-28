<script setup lang="ts">
import { API_ROUTES } from '~/shared/routes'
import type { UserMcpServer } from '~/types/ui/userMcpServer'

const props = defineProps<{
    mcp?: UserMcpServer
    onClose?: (doRefresh: boolean) => void
}>()

const form = ref({
    api_key: props.mcp?.cred.apiKey ?? ''
})

const loading = ref(false)

async function onSubmit() {
    if (!props.mcp?.id) return
    loading.value = true
    try {
        await ApiLinkBuilder.route(API_ROUTES.USER_MCP_SERVER.PUT_MCP)
            .params({ mcp_id: props.mcp.id })
            .body({ api_key: form.value.api_key })
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
    <UModal title="Modifier l'outil MCP">
        <template #body>
            <UForm :state="form" @submit="onSubmit" class="space-y-4">
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
