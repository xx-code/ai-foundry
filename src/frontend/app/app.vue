<script lang="ts" setup>
import { toWelcome } from './mappers';
import { API_ROUTES } from './shared/routes';
import type { WelcomeResponse } from './types/api';

const { data } = useAsyncData('welcome', async () => {
  const res = await ApiLinkBuilder.route<WelcomeResponse>(API_ROUTES.ROOT.WELCOME)
    .mapper(toWelcome)
    .execute()

  return res
})
</script>

<template>
  <div>
    <p>{{ data?.message }}</p>
  </div>
</template>
