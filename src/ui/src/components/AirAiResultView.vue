<template>
  <div class="container">
    <div>
      <h5 class="title">Result</h5>
      <p class="text">
        {{ result.answer }}
      </p>
    </div>
    <div v-if="result.facts?.length">
      <h5 class="title">Facts</h5>
      <p class="text">
        <ul>
          <li class="fact" v-for="fact in result.facts" :key="fact">{{ fact }}</li>
        </ul>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { AirAiResult } from '@/util/schema';

export default defineComponent({
  props: {
    result: {
      type: AirAiResult,
      required: true
    }
  }
});
</script>

<style scoped lang="scss">
.container {
  margin: 0 auto;
  width: 100%;
  max-width: 500px;
  margin-top: 1rem;
}

.title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: $gray800;
}

.text {
  font-size: 1rem;
  line-height: 1.1rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  color: $gray600;
}

.fact {
  margin-bottom: 1rem;
}
</style>
