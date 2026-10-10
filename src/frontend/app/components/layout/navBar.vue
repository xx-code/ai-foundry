<script setup lang="ts">
const { logout } = useAuth()

// TODO: remplace par l'utilisateur connecté (ex: const { user } = useAuth())
const { user } = useAuth()
const initial = computed(() => user.value?.username.charAt(0).toUpperCase())

const items = [
    [{ label: 'Déconnexion', icon: 'i-lucide-log-out', onSelect: () => logout() }]
]
</script>

<template>
    <header class="h-14 flex-none flex items-center justify-end px-6 border-b border-neutral-900">
        <UDropdownMenu :items="items" :content="{ align: 'end' }">
            <button
                class="flex items-center gap-3 text-xs font-medium cursor-pointer group"
            >
                <span>{{ user?.username }}</span>
                <span
                    class="grid place-items-center size-7 bg-white border border-neutral-900 font-mono
                           transition-all duration-200
                           group-hover:bg-secondary-500 group-hover:shadow-[2px_2px_0_#171717]
                           group-hover:-translate-x-px group-hover:-translate-y-px"
                >
                    {{ initial }}
                </span>
            </button>
        </UDropdownMenu>
    </header>
</template>