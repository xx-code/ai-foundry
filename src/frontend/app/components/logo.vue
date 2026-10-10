<script setup lang="ts">
const props = withDefaults(
    defineProps<{
        size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
    }>(), { size: "2xl"}
) 
</script>

<template>
    <div>
        <h1 :class="`font-display font-bold text-${size} text-neutral-900`">FOUNDRY</h1>
    </div>
</template>