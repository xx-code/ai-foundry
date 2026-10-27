<script setup lang="ts">
const props = defineProps<{
    modelId: string
}>()

type ChatMessage = {
    id: string
    role: 'user' | 'assistant' | 'error'
    content: string
}

const { ask } = useModelChat(() => props.modelId)

const messages = ref<ChatMessage[]>([])
const input = ref('')
const loading = ref(false)
const sessionId = ref(crypto.randomUUID())
const scroller = ref<HTMLElement | null>(null)

function stringify(value: unknown): string {
    return typeof value === 'string' ? value : JSON.stringify(value, null, 2)
}

function push(role: ChatMessage['role'], content: string) {
    messages.value.push({ id: crypto.randomUUID(), role, content })
}

async function scrollToBottom() {
    await nextTick()
    scroller.value?.scrollTo({ top: scroller.value.scrollHeight, behavior: 'smooth' })
}

async function send() {
    const message = input.value.trim()
    if (!message || loading.value) return

    push('user', message)
    input.value = ''
    loading.value = true
    scrollToBottom()

    try {
        const res = await ask({ message, sessionId: sessionId.value })
        sessionId.value = res.sessionId
        push('assistant', stringify(res.response))
    } catch {
        push('error', 'Le modèle n’a pas répondu. Vérifie la clé du fournisseur et réessaie.')
    } finally {
        loading.value = false
        scrollToBottom()
    }
}

function newChat() {
    messages.value = []
    sessionId.value = crypto.randomUUID()
}

function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        send()
    }
}
</script>

<template>
    <section class="flex flex-col min-h-0">
        <!-- Barre du chat -->
        <div class="h-10 flex-none flex items-center justify-between px-4 border-b border-neutral-900">
            <span class="font-display text-xs font-medium">Test du modèle</span>
            <UButton
                class="rounded-xs"
                color="neutral"
                variant="ghost"
                size="xs"
                icon="i-lucide-message-square-plus"
                label="Nouvelle conversation"
                :disabled="!messages.length"
                @click="newChat"
            />
        </div>

        <!-- Messages -->
        <div ref="scroller" class="flex-1 min-h-0 overflow-y-auto p-5">
            <div v-if="!messages.length" class="h-full grid place-items-center">
                <p class="font-display text-lg font-medium text-center">
                    Que veux-tu tester ?
                </p>
            </div>

            <ul v-else class="space-y-4">
                <li
                    v-for="m in messages"
                    :key="m.id"
                    class="flex"
                    :class="m.role === 'user' ? 'justify-end' : 'justify-start'"
                >
                    <div
                        class="max-w-[85%] border border-neutral-900 px-3 py-2 font-mono text-xs whitespace-pre-wrap break-words"
                        :class="{
                            'bg-secondary-500 shadow-[2px_2px_0_#171717]': m.role === 'user',
                            'bg-white': m.role === 'assistant',
                            'bg-red-100 border-red-700 text-red-800': m.role === 'error'
                        }"
                    >
                        {{ m.content }}
                    </div>
                </li>

                <li v-if="loading" class="flex">
                    <div class="border border-neutral-900 bg-white px-3 py-2 font-mono text-xs" aria-live="polite">
                        Réflexion en cours…
                    </div>
                </li>
            </ul>
        </div>

        <!-- Saisie -->
        <div class="flex-none p-4 border-t border-neutral-900">
            <div class="flex items-end gap-2">
                <UTextarea
                    v-model="input"
                    class="flex-1"
                    :rows="2"
                    autoresize
                    :maxrows="6"
                    placeholder="Écris au modèle…"
                    @keydown="onKeydown"
                />
                <UButton
                    class="rounded-xs"
                    color="secondary"
                    icon="i-lucide-send"
                    aria-label="Envoyer"
                    :loading="loading"
                    :disabled="!input.trim()"
                    @click="send"
                />
            </div>
            <p class="mt-2 font-mono text-[10px] text-neutral-500">
                Entrée pour envoyer, Maj+Entrée pour un retour à la ligne.
            </p>
        </div>
    </section>
</template>