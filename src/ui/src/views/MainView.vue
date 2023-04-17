<template>
  <div class="main-container">
    <PromptInput
      :value="inputValue"
      :submitDisabled="view === View.Loading"
      @update="onInputChange"
      @submit="onSubmit"
      placeholder="How does the air in my city compare to Dhaka?"
      maxlength="150"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import PromptInput from '@/components/PromptInput.vue';

enum View {
  Greeting = 'GREETING',
  Loading = 'LOADING'
}

export default defineComponent({
  components: { PromptInput },
  setup() {
    const inputValue = ref('');
    const view = ref(View.Greeting);

    const onInputChange = (value: string) => {
      inputValue.value = value;
    };

    const onSubmit = async () => {};

    return { inputValue, onInputChange, onSubmit, view, View };
  }
});
</script>

<style scoped lang="scss">
.main-container {
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  width: 100%;
}
</style>
