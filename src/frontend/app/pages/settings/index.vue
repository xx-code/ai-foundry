<script setup lang="ts">
import { useOverlay } from '@nuxt/ui/runtime/composables/useOverlay'
import type { TableColumn } from '@nuxt/ui'
import { toAiProviderKey } from '~/mappers/aiProviderKey'
import { toUserMcpServer } from '~/mappers/userMcpServer'
import { API_ROUTES } from '~/shared/routes'
import type { AiProviderKeyResponse } from '~/types/api/aiProviderKey'
import type { ListResponse } from '~/types/api'
import type { UserMcpServerResponse } from '~/types/api/userMcpServer'
import type { AiProviderKey } from '~/types/ui/aiProviderKey'
import type { UserMcpServer } from '~/types/ui/userMcpServer'
import ModalAddAiProviderKey from '~/components/modal/ModalAddAiProviderKey.vue'
import ModalEditAiProviderKey from '~/components/modal/ModalEditAiProviderKey.vue'
import ModalAddUserMcpServer from '~/components/modal/ModalAddUserMcpServer.vue'
import ModalEditUserMcpServer from '~/components/modal/ModalEditUserMcpServer.vue'

const overlay = useOverlay()

const aiProviderKeyModal = overlay.create(ModalAddAiProviderKey)
const aiProviderKeyEditModal = overlay.create(ModalEditAiProviderKey)
const mcpModal = overlay.create(ModalAddUserMcpServer)
const mcpEditModal = overlay.create(ModalEditUserMcpServer)

const { data, refresh, pending } = useAsyncData('settings-ai-keys-mcp', async () => {
    const [aiKeysRes, mcpRes] = await Promise.all([
        ApiLinkBuilder.route<ListResponse<AiProviderKeyResponse>>(API_ROUTES.AI_PROVIDER_KEYS.LIST)
            .mapper((res: ListResponse<AiProviderKeyResponse>) => res.items.map(toAiProviderKey))
            .execute()
            .catch(async () => [] as AiProviderKey[]),
        ApiLinkBuilder.route<ListResponse<UserMcpServerResponse>>(API_ROUTES.USER_MCP_SERVER.GET_MCPS)
            .mapper((res: ListResponse<UserMcpServerResponse>) => res.items.map(toUserMcpServer))
            .execute()
            .catch(async () => [] as UserMcpServer[])
    ])

    return {
        aiKeys: aiKeysRes as AiProviderKey[],
        mcps: mcpRes as UserMcpServer[]
    }
})

const aiColumns: TableColumn<AiProviderKey>[] = [
    { accessorKey: 'name', header: 'Nom' },
    { accessorKey: 'provider', header: 'Fournisseur' },
    { accessorKey: 'apiKey', header: 'Clé API' }
]

const mcpColumns: TableColumn<UserMcpServer>[] = [
    { accessorKey: 'app', header: 'Application' },
    { accessorKey: 'cred.apiKey', header: 'Clé API' }
]

function openAddAiKey() {
    aiProviderKeyModal.open({ onClose: (refreshNeeded: boolean) => { if (refreshNeeded) refresh() } })
}

function openEditAiKey(key: AiProviderKey) {
    aiProviderKeyEditModal.open({ aiKey: key, onClose: (refreshNeeded: boolean) => { if (refreshNeeded) refresh() } })
}

function openAddMcp() {
    mcpModal.open({ onClose: (refreshNeeded: boolean) => { if (refreshNeeded) refresh() } })
}

function openEditMcp(mcp: UserMcpServer) {
    mcpEditModal.open({ mcp, onClose: (refreshNeeded: boolean) => { if (refreshNeeded) refresh() } })
}

async function deleteAiKey(key: AiProviderKey) {
    try {
        await ApiLinkBuilder.route(API_ROUTES.AI_PROVIDER_KEYS.DELETE)
            .params({ id: key.id })
            .execute()
        refresh()
    } catch (e) {
        // ignore
    }
}

async function deleteMcp(mcp: UserMcpServer) {
    try {
        await ApiLinkBuilder.route(API_ROUTES.USER_MCP_SERVER.DELETE_MCP)
            .params({ mcp_id: mcp.id })
            .execute()
        refresh()
    } catch (e) {
        // ignore
    }
}
</script>

<template>
    <div class="space-y-8">
        <div class="flex items-center justify-between">
            <h1 class="font-display text-lg font-medium">Réglages</h1>
        </div>

        <section class="space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="font-display text-sm font-medium">Clés API des fournisseurs IA</h2>
                <UButton label="Ajouter une clé" icon="i-lucide-plus" size="sm" color="primary" @click="openAddAiKey" />
            </div>
            <UiDataTable :data="data?.aiKeys ?? []" :columns="aiColumns" :loading="pending">
                <template #name-cell="{ row }">
                    <div class="flex items-center justify-between">
                        <span>{{ row.original.name }}</span>
                        <div class="flex items-center gap-2">
                            <UButton size="xs" variant="ghost" icon="i-lucide-pencil" @click.stop="openEditAiKey(row.original)" />
                            <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash-2" @click.stop="deleteAiKey(row.original)" />
                        </div>
                    </div>
                </template>
                <template #apiKey-cell="{ row }">
                    <span class="truncate max-w-[200px] block">{{ row.original.apiKey }}</span>
                </template>
            </UiDataTable>
        </section>

        <section class="space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="font-display text-sm font-medium">Outils MCP utilisateur</h2>
                <UButton label="Ajouter un MCP" icon="i-lucide-plus" size="sm" color="primary" @click="openAddMcp" />
            </div>
            <UiDataTable :data="data?.mcps ?? []" :columns="mcpColumns" :loading="pending">
                <template #app-cell="{ row }">
                    <div class="flex items-center justify-between">
                        <span>{{ row.original.app }}</span>
                        <div class="flex items-center gap-2">
                            <UButton size="xs" variant="ghost" icon="i-lucide-pencil" @click.stop="openEditMcp(row.original)" />
                            <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash-2" @click.stop="deleteMcp(row.original)" />
                        </div>
                    </div>
                </template>
                <template #cred.apiKey-cell="{ row }">
                    <span class="truncate max-w-[200px] block">{{ row.original.cred.apiKey }}</span>
                </template>
            </UiDataTable>
        </section>
    </div>
</template>
