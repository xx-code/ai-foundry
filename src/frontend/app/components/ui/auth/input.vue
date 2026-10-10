<script setup lang="ts">
const props = defineProps<{
    type?: string
    placeholder?: string
    autocomplete?: string
    // injectés par UFormField via useFormField
    id?: string
    name?: string
    color?: string
    highlight?: boolean
    disabled?: boolean
}>()

const model = defineModel<string>()

const {
    id, name, color, disabled, ariaAttrs,
    emitFormInput, emitFormBlur, emitFormChange, emitFormFocus
//@ts-ignore
} = useFormField(props)

const hasError = computed(() => color.value === 'error')
</script>

<template>
    <input
        :id="id"
        v-model="model"
        :name="name"
        :type="type ?? 'text'"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :disabled="disabled"
        v-bind="ariaAttrs"
        class="w-full px-3 py-2.5 text-sm bg-white text-neutral-900 border-2 outline-none
               transition-all duration-200 ease-out
               placeholder:text-neutral-400 hover:bg-neutral-50
               focus:-translate-x-0.5 focus:-translate-y-0.5
               disabled:opacity-60 disabled:cursor-not-allowed"
        :class="hasError
            ? 'border-red-600 focus:shadow-[3px_3px_0_#dc2626]'
            : 'border-neutral-900 focus:shadow-[3px_3px_0_var(--color-primary-500)]'"
        @input="emitFormInput"
        @change="emitFormChange"
        @focus="emitFormFocus"
        @blur="emitFormBlur"
    />
</template>