<template>
  <div class="container">
    <SpinnerIcon color="#CBD5E0" />
    <p class="text">{{ label }}</p>
  </div>
</template>

<script lang="ts">
import SpinnerIcon from '@/components/icons/SpinnerIcon.vue';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  components: { SpinnerIcon },
  setup() {
    const LABELS = [
      'Reading stations...',
      'Inspecting concentration levels...',
      'Calculating air quality indexes...',
      'Generating report...',
      'Researching facts...',
      'Almost there...'
    ];

    const randomLabel = () => {
      const randomIndex = Math.floor(Math.random() * LABELS.length);
      const newLabel = LABELS[randomIndex];
      return newLabel;
    };

    const label = ref(randomLabel());
    const intervalId = ref<number | null>(null);

    intervalId.value = window.setInterval(() => {
      label.value = randomLabel();
    }, 1200);

    return {
      label,
      intervalId
    };
  },
  beforeUnmount() {
    if (!this.intervalId) return;
    clearInterval(this.intervalId);
  }
});
</script>

<style scoped lang="scss">
.container {
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  max-width: 280px;
  text-align: center;
  gap: 0.8rem;
}

.text{
  font-size: 0.9rem;
  color: $gray500;
  line-height: 1.1rem;
}
</style>
