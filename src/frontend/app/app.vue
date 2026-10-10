<template>
  <body class="bg-neutral-50 text-neutral-900" > 
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </body> 
</template>

<style scoped>
.page-enter-active,
.page-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-enter-from {
    opacity: 0;
    transform: translateY(8px);
}
.page-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}
</style>