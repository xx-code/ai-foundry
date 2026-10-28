<script setup lang="ts">
import type { Model } from '~/types/ui/model'
import { ModelToolType } from '~/shared/constants/model'

type ModelDraft = Pick<Model, 'name' | 'defaultInstruction' | 'params'>

const props = defineProps<{
    model: Model
    saving?: boolean
}>()

const emit = defineEmits<{
    save: [draft: ModelDraft]
    addTool: [toolType: ModelToolType]
    removeTool: [toolId: string]
    toggleWebSearch: [checked: boolean]
    toggleCodeInterpreter: [checked: boolean]
}>()

function toDraft(model: Model): ModelDraft {
    return {
        name: model.name,
        defaultInstruction: model.defaultInstruction ?? '',
        params: { ...model.params }
    }
}

const draft = ref<ModelDraft>(toDraft(props.model))

// Resynchronise le brouillon quand le modèle est rechargé / sauvegardé
watch(() => props.model, (model) => { draft.value = toDraft(model) }, { deep: true })

const isDirty = computed(() =>
    JSON.stringify(draft.value) !== JSON.stringify(toDraft(props.model))
)

// TODO: aligne avec ModelReasoningType (~/shared/constants/model)
const reasoningItems = ['low', 'medium', 'high']

function reset() {
    draft.value = toDraft(props.model)
}

const hasWebSearch = computed(() => props.model.tools.some(t => t.toolType === ModelToolType.WEB_SEARCH))
const hasCodeInterpreter = computed(() => props.model.tools.some(t => t.toolType === ModelToolType.CODE_INTERPRETOR))

function onToggleWebSearch(val: boolean) {
    emit('toggleWebSearch', val)
}

function onToggleCodeInterpreter(val: boolean) {
    emit('toggleCodeInterpreter', val)
}
</script>

<template>
    <section class="flex flex-col min-h-0 overflow-y-auto">
        <!-- Nom -->
        <div class="p-5 border-b border-neutral-900 space-y-2">
            <label for="model-name" class="block font-display text-xs font-medium">Nom</label>
            <UInput id="model-name" v-model="draft.name" class="w-full" />
        </div>

        <!-- Instructions -->
        <div class="p-5 border-b border-neutral-900 space-y-2">
            <label for="model-instructions" class="block font-display text-xs font-medium">Instructions</label>
            <UTextarea
                id="model-instructions"
                v-model="draft.defaultInstruction"
                :rows="8"
                autoresize
                class="w-full"
                placeholder="Décris le rôle et le comportement attendus du modèle."
            />
        </div>

        <!-- Paramètres -->
        <div class="p-5 border-b border-neutral-900 space-y-5">
            <h2 class="font-display text-xs font-medium">Paramètres</h2>

            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <label for="model-temperature" class="font-mono text-xs">Température</label>
                    <span class="font-mono text-xs">{{ draft.params.temperature.toFixed(1) }}</span>
                </div>
                <USlider
                    id="model-temperature"
                    v-model="draft.params.temperature"
                    :min="0"
                    :max="2"
                    :step="0.1"
                />
            </div>

            <div class="space-y-2">
                <label for="model-max-tokens" class="block font-mono text-xs">Tokens max</label>
                <UInput
                    id="model-max-tokens"
                    v-model.number="draft.params.maxTokens"
                    type="number"
                    :min="1"
                    class="w-full"
                />
            </div>

            <div class="space-y-2">
                <label class="block font-mono text-xs">Raisonnement</label>
                <USelect v-model="draft.params.reasoning" :items="reasoningItems" class="w-full" />
            </div>
        </div>

        <!-- Tools -->
        <div class="p-5 border-b border-neutral-900 space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="font-display text-xs font-medium">Tools</h2>
                <span class="font-mono text-[10px]">{{ model.tools.length }}</span>
            </div>

            <div class="space-y-2">
                <div class="flex items-center justify-between border border-neutral-900 bg-white px-3 py-2">
                    <span class="font-mono text-xs">Web Search</span>
                    <USwitch :model-value="hasWebSearch" @update:model-value="onToggleWebSearch" />
                </div>
                <div class="flex items-center justify-between border border-neutral-900 bg-white px-3 py-2">
                    <span class="font-mono text-xs">Code Interpreter</span>
                    <USwitch :model-value="hasCodeInterpreter" @update:model-value="onToggleCodeInterpreter" />
                </div>
            </div>

            <div class="space-y-1.5">
                <div class="font-mono text-[10px] text-neutral-600">MCP</div>
                <ul v-if="model.tools.some(t => t.toolType === ModelToolType.MCP_SERVER)" class="space-y-1.5">
                    <li
                        v-for="tool in model.tools.filter(t => t.toolType === ModelToolType.MCP_SERVER)"
                        :key="tool.id"
                        class="flex items-center justify-between border border-neutral-900 bg-white px-3 py-2 font-mono text-xs"
                    >
                        <span class="truncate">{{ tool.name }}</span>
                        <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash-2" @click="emit('removeTool', tool.id)" />
                    </li>
                </ul>
                <p v-else class="font-mono text-xs text-neutral-500">Aucun MCP connecté.</p>
            </div>
        </div>

        <!-- Actions (collées en bas) -->
        <div class="sticky bottom-0 mt-auto flex items-center justify-end gap-2 p-4 border-t border-neutral-900 bg-[#fff9ec]">
            <UButton
                class="rounded-xs"
                color="neutral"
                variant="ghost"
                label="Annuler"
                :disabled="!isDirty || saving"
                @click="reset"
            />
            <UButton
                class="rounded-xs"
                color="secondary"
                label="Enregistrer"
                :loading="saving"
                :disabled="!isDirty"
                @click="emit('save', draft)"
            />
        </div>
    </section>
</template>