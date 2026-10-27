<script setup lang="ts">
import type { Model } from '~/types/ui/model'

const route = useRoute()
const modelId = computed(() => route.params.id as string)

// TODO: remplace par l'appel API (ex: toModel(await $fetch(`/models/${modelId.value}`)))
const model = ref<Model>({
    id: modelId.value,
    name: 'brain finance',
    providerKeyId: '1',
    providerModel: 'gpt-5.2',
    defaultInstruction: 'Tu es un assistant IA qui aide à trouver des informations.',
    params: { temperature: 1, maxTokens: 2048, reasoning: 'medium' as Model['params']['reasoning'] },
    tools: []
})

const saving = ref(false)

type ModelDraft = Pick<Model, 'name' | 'defaultInstruction' | 'params'>

async function onSave(draft: ModelDraft) {
    saving.value = true
    try {
        // TODO: PATCH /models/:id avec UpdateModelRequest
        model.value = { ...model.value, ...draft }
    } finally {
        saving.value = false
    }
}
</script>

<template>
    <div class="flex flex-col h-full min-h-0">
        <!-- En-tête -->
        <div class="h-14 flex-none flex items-center gap-3 px-6 border-b border-neutral-900">
            <NuxtLink
                to="/"
                class="grid place-items-center size-7 border border-neutral-900 bg-white
                       transition-all duration-150 hover:bg-secondary-500 hover:-translate-x-px hover:-translate-y-px
                       hover:shadow-[2px_2px_0_#171717]"
                aria-label="Retour aux modèles"
            >
                <UIcon name="i-lucide-arrow-left" class="size-4" />
            </NuxtLink>
            <h1 class="font-display text-sm font-medium">{{ model.name }}</h1>
            <span class="font-mono text-[10px] border border-neutral-900 px-1.5 py-0.5">
                {{ model.providerModel }}
            </span>
        </div>

        <!-- Édition | Chat -->
        <div class="grid flex-1 min-h-0 grid-cols-1 lg:grid-cols-[minmax(340px,2fr)_3fr]">
            <UiModelEditPart
                class="border-b lg:border-b-0 lg:border-r border-neutral-900"
                :model="model"
                :saving="saving"
                @save="onSave"
            />
            <UiModelChatPart :model-id="model.id" />
        </div>
    </div>
</template>