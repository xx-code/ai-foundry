<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import type { AiModel } from '~/types/ui/model'

const models = ref<AiModel[]>([
    {
        id: '1',
        name: 'brain finance',
        model: 'gpt-5.2',
        provider: 'OpenAi',
        createdAt: '2026-10-07T12:53:36'
    }
])
const loading = ref(false)

const columns: TableColumn<AiModel>[] = [
    { accessorKey: 'name', header: 'Nom' },
    { accessorKey: 'model', header: 'Modèles' },
    { accessorKey: 'provider', header: 'Fournisseur' },
    { accessorKey: 'createdAt', header: 'Créé à' }
]

const dateFormatter = new Intl.DateTimeFormat('fr-FR', {
    dateStyle: 'short',
    timeStyle: 'medium'
})
</script>

<template>
    <div>
        <div class="mb-3 flex justify-end">
            <UButton class="rounded-xs" color="secondary" label="Ajouter un modele" />
        </div>
        <UiDataTable :data="models" :columns="columns" :loading="loading">
            <template #createdAt-cell="{ row }">
                {{ dateFormatter.format(new Date(row.original.createdAt)) }}
            </template>
        </UiDataTable>
    </div>
</template>