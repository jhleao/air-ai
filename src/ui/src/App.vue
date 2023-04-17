<script setup lang="ts">
import LogoHeader from './components/LogoHeader.vue'
</script>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({})
</script>

<template>
  <header>
    <LogoHeader />
  </header>

  <RouterView />
</template>

<style scoped>
    
</style>
