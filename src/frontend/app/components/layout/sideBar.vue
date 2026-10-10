<script setup lang="ts">
const route = useRoute()

const links = [
    { label: 'Modèles', to: '/' },
    { label: 'Agents', to: '/agents' },
    { label: 'Tools', to: '/tools' }
]

function isActive(to: string) {
    return to === '/' ? route.path === '/' : route.path.startsWith(to)
}
</script>

<template>
    <aside class="flex flex-col w-52 shrink-0 border-r border-neutral-900">
        <!-- Logo (même hauteur que la navbar) -->
        <div class="h-14 flex items-center px-4 border-b border-neutral-900">
            <Logo />
        </div>

        <!-- Navigation -->
        <nav class="flex-1 p-3 space-y-1.5">
            <NuxtLink
                v-for="link in links"
                :key="link.to"
                :to="link.to"
                class="group flex items-center justify-between px-3 py-2 font-mono text-xs border-2
                       transition-all duration-200 ease-out"
                :class="isActive(link.to)
                    ? 'bg-secondary-500 border-neutral-900 shadow-[3px_3px_0_#171717] -translate-x-px -translate-y-px'
                    : 'border-transparent hover:bg-secondary-500/30 hover:translate-x-1'"
            >
                <span>{{ link.label }}</span>
                <span
                    class="transition-all duration-200"
                    :class="isActive(link.to)
                        ? 'opacity-100 translate-x-0'
                        : 'opacity-0 -translate-x-2 group-hover:opacity-60 group-hover:translate-x-0'"
                >→</span>
            </NuxtLink>
        </nav>

        <!-- Réglages en bas -->
        <div class="p-3">
            <NuxtLink
                to="/settings"
                class="block px-3 py-2 font-mono text-xs border-2 border-transparent
                       transition-all duration-200 hover:translate-x-1 hover:bg-secondary-500/30"
            >
                Réglages
            </NuxtLink>
        </div>
    </aside>
</template>