<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { toListModelCards, toListModels, toModel } from '~/mappers/model'
import { API_ROUTES } from '~/shared/routes'
import type { ModelResponse } from '~/types/api/model'
import type { List } from '~/types/ui'
import type { ModelTableItem } from '~/types/ui/model'


const loading = ref(false)
const { data:models } = useAsyncData('models+all', async () => {
    const res = await ApiLinkBuilder
            .route<List<ModelResponse>>(API_ROUTES.MODEL.GET_ALL_MODELS)
            .mapper(toListModels)
            .execute()
    
    return toListModelCards(res.items)
})

const columns: TableColumn<ModelTableItem>[] = [
    { accessorKey: 'name', header: 'Nom' },
    { accessorKey: 'model', header: 'Modèles' },
    { accessorKey: 'provider', header: 'Fournisseur' },
    { accessorKey: 'createdAt', header: 'Créé à' }
]

const dateFormatter = new Intl.DateTimeFormat('fr-FR', {
    dateStyle: 'short',
    timeStyle: 'medium'
})

function openModel(model: ModelTableItem) {
    navigateTo(`/models/${model.id}`)
}
</script>

<template>
    <div>
        <div class="mb-3 flex justify-end">
            <UButton class="rounded-xs" color="secondary" label="Ajouter un modele" />
        </div>
        <UiDataTable
            :data="models ?? []"
            :columns="columns"
            :loading="loading"
            @select="openModel"
        >
            <template #createdAt-cell="{ row }">
                {{ dateFormatter.format(new Date(row.original.createdAt)) }}
            </template>
        </UiDataTable>
    </div>
</template>