<template>
  <div class="result-container">
    <div class="summary-container">
      <h5 class="title">Result</h5>
      <p class="text">
        {{ result.answer }}
      </p>
    </div>
    <div class='cards-container'  v-if="result.auxiliary_data?.length">
      <AirQualityCard class="fact" v-for="place in result.auxiliary_data" :key="place.location_name" :data="place"/>
    </div>
    <div class='facts-container' v-if="result.facts?.length">
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
import AirQualityCard from './AirQualityCard/AirQualityCard.vue';

export default defineComponent({
  components: { AirQualityCard },
    props: {
        result: {
            type: AirAiResult,
            required: true
        }
    },
});
</script>

<style scoped lang="scss">
.result-container {
  margin: 0 auto;
  margin-top: 1rem;
}

.summary-container {
  max-width: $max-content-width;
  min-width: $min-content-width;
  margin: 0 auto;
}

.title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: $gray800;
}

.text {
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 400;
  max-width: $max-content-width;
  min-width: $min-content-width;
  color: $gray600;
  margin: 0 auto;
}

.facts-container {
  max-width: $max-content-width;
  min-width: $min-content-width;
  margin: 0 auto;
}

.fact {
  line-height: 1.5rem;
  margin-bottom: 1rem;
}

.cards-container {
  max-width: 800px;
  margin: 0 auto;
  margin-top: 1rem;
  margin-bottom: 1.5rem;

  display: flex;
  flex-flow: row wrap;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
</style>
