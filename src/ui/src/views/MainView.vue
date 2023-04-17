<template>
  <div class="main-container">
    <PromptInput
      :value="inputValue"
      :submitDisabled="view === View.Loading"
      @update="onInputChange"
      @submit="onSubmit"
      type="text"
      placeholder="How does the air in my city compare to Dhaka?"
      maxlength="150"
    />
    <LoadingState v-if="view === View.Loading" />
    <ErrorState v-if="view === View.Error" @tryAgain="onSubmit" />
    <UnavailableLocation v-if="view === View.UnavailableLocation" />
    <GreetingText v-if="view === View.Greeting" />
    <AirAiResultView v-if="view === View.Result && result" :result="result" />
    <ViewOnGithub />
  </div>
</template>

<script lang="ts">
import PromptInput from '@/components/PromptInput.vue';
import { defineComponent, ref } from 'vue';
import AirAiResultView from '../components/AirAiResultView.vue';
import ErrorState from '../components/ErrorState.vue';
import GreetingText from '../components/GreetingText.vue';
import LoadingState from '../components/LoadingState.vue';
import UnavailableLocation from '../components/UnavailableLocation.vue';
import ViewOnGithub from '../components/ViewOnGithub.vue';
import { AirAiApi } from '../util/api';
import { LocationUtil } from '../util/location';
import type { AirAiResult, LatLng } from '../util/schema';

enum View {
  Greeting = 'GREETING',
  Loading = 'LOADING',
  Error = 'ERROR',
  Result = 'RESULT',
  UnavailableLocation = 'UNAVAILABLE_LOCATION'
}

export default defineComponent({
  components: {
    PromptInput,
    LoadingState,
    GreetingText,
    AirAiResultView,
    ErrorState,
    ViewOnGithub,
    UnavailableLocation
  },
  setup() {
    const inputValue = ref('');
    const location = ref<LatLng | null>(null);
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
        const apiResponse = await AirAiApi.prompt(prompt, location.value);
        result.value = apiResponse;
        view.value = View.Result;
      } catch (e) {
        if ((e as Response)?.status !== 422) {
          view.value = View.Error;
          return;
        }

        const errorCode = (await (e as Response).json()).code;
        if (errorCode !== 'ERR_NO_USER_LOCATION') throw new Error();
        const hasLocation = await LocationUtil.hasLocationEnabled();
        if(!hasLocation) view.value = View.UnavailableLocation;
        location.value = await LocationUtil.getLocation();
        // Retry with location
        if(location.value) onSubmit();
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
  flex: 1;
}
</style>
