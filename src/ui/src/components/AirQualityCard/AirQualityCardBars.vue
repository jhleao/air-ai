<template>
  <div class="bars-container">
    <div
      class="bar-container"
      v-for="(bar, idx) in bars"
      :key="bar.dateStr"
      @mouseover="() => showTooltipFor(idx)"
      @mouseout="hideTooltip"
      :style="{ opacity: tooltipVisibleForIdx !== null && tooltipVisibleForIdx !== idx ? 0.7 : 1}"
    >
      <div class="bar" :class="bar.quality" :style="{ height: bar.height + '%' }">
        <div class="bar-value">{{ bar.value }}</div>
        <div v-if="tooltipVisibleForIdx === idx" class="tooltip">{{ bar.text }}</div>
      </div>
      <div class="bar-label">{{ bar.dateStr }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { AirDataPoint } from '@/util/schema';
import { DateUtil } from '@/util/date';
import type { Bar } from './AirQualityCard.util';
import { getQuality } from './AirQualityCard.util';
import { MathUtil } from '@/util/math';
import { computed } from 'vue';

export default defineComponent({
  props: {
    data: {
      type: Array<AirDataPoint>,
      required: true
    }
  },
  setup(props) {
    const bars = computed<Bar[]>(() => {
      const minAqi = Math.min(...props.data.map((dataPoint) => dataPoint.aqi ?? 0));
      const maxAqi = Math.max(...props.data.map((dataPoint) => dataPoint.aqi ?? 0));
      const MIN_BAR_HEIGHT = 25;
      return props.data.map((dataPoint) => {
        const height = MathUtil.linearInterpolation(
          dataPoint.aqi ?? 0,
          minAqi,
          maxAqi,
          MIN_BAR_HEIGHT,
          100
        );
        const quality = getQuality(dataPoint.aqi);
        const value = parseInt(`${dataPoint.aqi}`) ?? 0;
        const dateStr = DateUtil.format(dataPoint.date_unix * 1000, 'MMM dd');
        const text = `${dataPoint.pm2_5 ? `PM2.5: ${dataPoint.pm2_5.toFixed(1)} µg/m³` : ''}
PM10: ${dataPoint.pm10.toFixed(1)} µg/m³
NO2: ${dataPoint.no2.toFixed(1)} µg/m³
O3: ${dataPoint.o3.toFixed(1)} µg/m³
SO2: ${dataPoint.so2.toFixed(1)} µg/m³
CO: ${dataPoint.co.toFixed(1)} µg/m³`;

        return { height, quality, value, dateStr, text };
      });
    });

    const tooltipVisibleForIdx = ref<number | null>(null);

    const showTooltipFor = (idx: number) => {
      tooltipVisibleForIdx.value = idx;
    };
    const hideTooltip = () => {
      tooltipVisibleForIdx.value = null;
    };

    return { bars, showTooltipFor, hideTooltip, tooltipVisibleForIdx };
  }
});
</script>

<style scoped lang="scss">
.good {
  background-color: $good-bg;
  color: $good-fg;
}

.moderate {
  background-color: $moderate-bg;
  color: $moderate-fg;
}

.unhealthy {
  background-color: $unhealthy-bg;
  color: $unhealthy-fg;
}

.bars-container {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: flex-end;
  gap: 0.4em;
  height: 120px;
}

.bar {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  position: relative;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.15);
  width: 100%;
  border-radius: 2px;

  &-container {
    height: 100%;
    width: 40px;
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-end;
    gap: 0.2em;
    transition: opacity 0.1s ease-out;
    cursor: default;
  }

  &-label {
    color: $gray600;
    font-size: 0.7em;
    text-align: center;
  }

  &-value {
    text-align: center;
    font-size: 0.8em;
  }

  .tooltip {
    position: absolute;
    bottom: 110%;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.5rem;
    background-color: white;
    box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
    color: $gray600;
    font-size: 0.8rem;
    white-space: nowrap;
    white-space: pre-wrap;
    width: 150px;
    text-align: center;
    z-index: 10;
  }
}
</style>
