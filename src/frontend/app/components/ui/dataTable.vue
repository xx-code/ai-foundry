<script setup lang="ts" generic="T extends Record<string, any>">
import type { TableColumn } from '@nuxt/ui'

const props = withDefaults(defineProps<{
    data: T[]
    columns: TableColumn<T>[]
    pageSize?: number
    loading?: boolean
}>(), {
    pageSize: 10
})

const page = ref(1)

const total = computed(() => props.data.length)
const pageCount = computed(() => Math.max(1, Math.ceil(total.value / props.pageSize)))
const start = computed(() => (total.value === 0 ? 0 : (page.value - 1) * props.pageSize + 1))
const end = computed(() => Math.min(page.value * props.pageSize, total.value))

const rows = computed(() =>
    props.data.slice((page.value - 1) * props.pageSize, page.value * props.pageSize)
)

// Reste sur une page valide si les données changent
watch(pageCount, (count) => {
    if (page.value > count) page.value = count
})

const tableUi = {
    root: 'flex-1 overflow-auto',
    base: 'w-full border-separate border-spacing-0',
    thead: 'bg-neutral-900 sticky top-0 z-10',
    th: 'px-4 py-2.5 text-left text-[11px] font-medium text-[#fff9ec] font-display',
    tr: 'transition-colors duration-150 hover:bg-secondary-500/20 font-mono',
    td: 'px-4 py-3 text-xs font-mono text-neutral-900 whitespace-nowrap',
    empty: 'py-16 text-center text-xs font-mono text-neutral-500'
}
</script>

<template>
    <div class="flex flex-col min-h-105 border border-neutral-900 bg-[#fff9ec]">
        <UTable
            :data="rows"
            :columns="columns"
            :loading="loading"
            :ui="tableUi"
        >
            <!-- Laisse passer les slots (#xxx-cell, #empty, ...) -->
            <template v-for="(_, name) in $slots" #[name]="slotProps">
                <slot :name="name" v-bind="slotProps ?? {}" />
            </template>

            <template v-if="!$slots.empty" #empty>
                Aucune donnée
            </template>
        </UTable>

        <!-- Pied : compteur + pagination -->
        <div class="flex items-center justify-between px-3 py-2 border-t border-neutral-900 font-mono text-[10px]">
            <span>{{ start }} - {{ end }} sur {{ total }}</span>

            <div class="flex items-center gap-4">
                <button
                    class="transition-all duration-150 hover:-translate-x-0.5 disabled:opacity-30 disabled:pointer-events-none"
                    :disabled="page <= 1"
                    @click="page--"
                >
                    ‹ préc.
                </button>
                <button
                    class="transition-all duration-150 hover:translate-x-0.5 disabled:opacity-30 disabled:pointer-events-none"
                    :disabled="page >= pageCount"
                    @click="page++"
                >
                    suiv. ›
                </button>
            </div>
        </div>
    </div>
</template>