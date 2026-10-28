<script setup lang="ts">
import { toModel } from '~/mappers/model'
import { API_ROUTES } from '~/shared/routes'
import type { ModelResponse, UpdateModelRequest } from '~/types/api/model'
import type { Model } from '~/types/ui/model'
import { ModelToolType } from '~/shared/constants/model'

const route = useRoute()
const modelId = computed(() => route.params.id as string)

const { data:model, refresh } = useAsyncData(`model-${modelId}`, async () => {
    const res = await ApiLinkBuilder
            .route<ModelResponse>(API_ROUTES.MODEL.GET_MODEL)
            .params({ id: modelId.value })
            .mapper(toModel)
            .execute()
        
    console.log(res)
    
    return res
})

const saving = ref(false)

type ModelDraft = Pick<Model, 'name' | 'defaultInstruction' | 'params'>

async function onSave(draft: ModelDraft) {
    saving.value = true
    try {
        await ApiLinkBuilder
            .route<ModelResponse>(API_ROUTES.MODEL.UPDATE_MODEL)
            .params({ id: modelId.value })
            .body({
                name: draft.name, 
                default_instruction: draft.defaultInstruction,
                params: {
                    temperature: draft.params.temperature,
                    max_tokens: draft.params.maxTokens,
                    reasoning: draft.params.reasoning
                },

            } satisfies UpdateModelRequest)
            .execute()

        refresh()
    } finally {
        saving.value = false
    }
}

async function addTool(toolType: ModelToolType) {
    try {
        await ApiLinkBuilder.route(API_ROUTES.MODEL.ADD_MODEL_TOOL)
            .params({ id: modelId.value })
            .body({ tool_id: toolType, tool_type: toolType })
            .execute()
        refresh()
    } catch (e) {
        // ignore
    }
}

async function removeTool(toolId: string) {
    try {
        await ApiLinkBuilder.route(API_ROUTES.MODEL.REMOVE_MODEL_TOOL)
            .params({ id: modelId.value, tool_id: toolId })
            .execute()
        refresh()
    } catch (e) {
        // ignore
    }
}

function toggleWebSearch(checked: boolean) {
    if (!model.value) return
    const existing = model.value.tools.find(t => t.toolType === ModelToolType.WEB_SEARCH)
    if (checked && !existing) {
        addTool(ModelToolType.WEB_SEARCH)
    } else if (!checked && existing) {
        removeTool(existing.id)
    }
}

function toggleCodeInterpreter(checked: boolean) {
    if (!model.value) return
    const existing = model.value.tools.find(t => t.toolType === ModelToolType.CODE_INTERPRETOR)
    if (checked && !existing) {
        addTool(ModelToolType.CODE_INTERPRETOR)
    } else if (!checked && existing) {
        removeTool(existing.id)
    }
}
</script>

<template>
    <div v-if="model != undefined" class="flex flex-col h-full min-h-0">
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
                @add-tool="addTool"
                @remove-tool="removeTool"
                @toggle-web-search="toggleWebSearch"
                @toggle-code-interpreter="toggleCodeInterpreter"
            />
            <UiModelChatPart :model-id="model.id" />
        </div>
    </div>
</template>