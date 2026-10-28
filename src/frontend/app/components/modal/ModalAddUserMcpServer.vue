<script setup lang="ts">
import { API_ROUTES } from '~/shared/routes'
import type { AddUserMcpServerRequest } from '~/types/api/userMcpServer'
import { McpClientApp, McpClientAuthType } from '~/shared/constants/mcpClient'

const props = defineProps<{
    onClose?: (doRefresh: boolean) => void
}>()

const form = ref<AddUserMcpServerRequest>({
    app: McpClientApp.DEMO_APP,
    api_key: ''
})

const loading = ref(false)

const apps = [
    { label: 'DEMO_APP', value: McpClientApp.DEMO_APP },
    { label: 'AGNI_APP', value: McpClientApp.AGNI_APP }
]

async function onSubmit() {
    loading.value = true
    try {
        await ApiLinkBuilder.route(API_ROUTES.USER_MCP_SERVER.ADD_MCP)
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
    <UModal title="Ajouter un outil MCP">
        <template #body>
            <UForm :state="form" @submit="onSubmit" class="space-y-4">
                <UFormField label="Application" name="app">
                    <USelect v-model="form.app" :items="apps" value-key="value" label-key="label" />
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
