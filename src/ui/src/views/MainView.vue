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
    <LoadingState v-if="view === View.Loading" />
    <ErrorState v-if="view === View.Error" @tryAgain="onSubmit" />
    <GreetingText v-if="view === View.Greeting" />
    <AirAiResultView v-if="view === View.Result && result" :result="result" />
  </div>
</template>

<script lang="ts">
import PromptInput from '@/components/PromptInput.vue';
import { defineComponent, ref } from 'vue';
import AirAiResultView from '../components/AirAiResultView.vue';
import ErrorState from '../components/ErrorState.vue';
import GreetingText from '../components/GreetingText.vue';
import LoadingState from '../components/LoadingState.vue';
import { AirAiApi } from '../util/api';
import type { AirAiResult } from '../util/schema';

enum View {
  Greeting = 'GREETING',
  Loading = 'LOADING',
  Error = 'ERROR',
  Result = 'RESULT'
}

export default defineComponent({
  components: { PromptInput, LoadingState, GreetingText, AirAiResultView, ErrorState },
  setup() {
    const inputValue = ref('');
    const view = ref(View.Greeting);
    const result = ref<AirAiResult | null>(null);

    const onInputChange = (value: string) => {
      inputValue.value = value;
    };

    const onSubmit = async () => {
      if (!inputValue.value) return;
      view.value = View.Loading;
      const prompt = inputValue.value;
      try {
        const apiResponse = await AirAiApi.prompt(prompt);
        result.value = apiResponse;
        view.value = View.Result;
      } catch {
        view.value = View.Error;
      }
    };

    return { inputValue, onInputChange, onSubmit, view, View, result };
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
