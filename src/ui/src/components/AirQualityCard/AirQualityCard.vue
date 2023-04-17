<template>
  <div class="air-quality-card-container">
    <div class="header">
      <p class="title">{{ name }}</p>
      <p class="date">{{ dateStr }}</p>
    </div>
    <div class="aqi-card" :class="quality">
      <p class="aqi-card-box" :class="quality">
        <span>AQI</span>
        <span class="aqi-card-box-value">{{ aqi }}</span>
      </p>
      <div class="aqi-card-details">
        <p class="aqi-card-quality-name">{{ qualityName }}</p>
        <p class="aqi-card-main-pollutant">Main pollutant: {{ mainPollutant }}</p>
      </div>
    </div>
    <p class="bars-title">Over the last 7 days</p>
    <AirQualityCardBars :data="data.data" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { LocationAirData } from '@/util/schema';
import { DateUtil } from '@/util/date';
import { TextUtil } from '@/util/text';
import { computed } from 'vue';
import { POLLUTANT_DISPLAY_NAMES, Pollutant, getQuality } from './AirQualityCard.util';
import AirQualityCardBars from './AirQualityCardBars.vue';

export default defineComponent({
  components: { AirQualityCardBars },
  props: {
    data: {
      type: LocationAirData,
      required: true
    }
  },
  setup(props) {
    const aqi = computed(() => {
      const latestPoint = props.data.data[props.data.data.length - 1];
      if (!latestPoint) return 0;
      return latestPoint.aqi ?? 0;
    });

    const mainPollutant = computed(() => {
      const latest = props.data.data[props.data.data.length - 1];
      if (!latest) return 'Unknown';
      let mainPollutantKey = Pollutant.pm2_5;
      if (latest.o3 > latest[mainPollutantKey]) mainPollutantKey = Pollutant.o3;
      if (latest.co > latest[mainPollutantKey]) mainPollutantKey = Pollutant.co;
      if (latest.no > latest[mainPollutantKey]) mainPollutantKey = Pollutant.no;
      if (latest.no2 > latest[mainPollutantKey]) mainPollutantKey = Pollutant.no2;
      if (latest.so2 > latest[mainPollutantKey]) mainPollutantKey = Pollutant.so2;
      if (latest.pm10 > latest[mainPollutantKey]) mainPollutantKey = Pollutant.pm10;
      if (latest.nh3 > latest[mainPollutantKey]) mainPollutantKey = Pollutant.nh3;
      return POLLUTANT_DISPLAY_NAMES[mainPollutantKey];
    });
    const quality = computed(() => getQuality(aqi.value));

    const qualityName = computed(() => TextUtil.capitalizeFirstLetter(quality.value));

    const dateStr = computed(() => {
      if (props.data.data.length < 1) return '';
      const date = new Date(props.data.data[props.data.data.length - 1].date_unix * 1000);
      return DateUtil.format(date, 'MMM dd, yyyy');
    });
    return {
      quality,
      qualityName,
      mainPollutant,
      aqi,
      dateStr,
      name: props.data.location_name
    };
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

.air-quality-card-container {
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  padding: 1rem;
  font-size: 0.9rem;
  width: 350px;
}

.header {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;

  .title {
    font-size: 1.2em;
    color: $gray700;
    font-weight: 600;
  }

  .date {
    font-size: 0.8em;
    color: $gray500;
  }
}

.aqi-card {
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  margin-bottom: 0.7em;
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: 1em;
  height: 5em;
  padding: 0.8em;

  &-details {
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-end;
    align-self: flex-end;
  }

  &-quality-name {
    font-size: 1.6em;
    margin-bottom: 0.2em;
  }

  &-main-pollutant {
    font-size: 0.8em;
    line-height: 1em;
  }

  &-box {
    border-radius: 4px;
    padding: 0.3em;
    padding-left: 0.6em;
    font-size: 0.8em;
    width: 5em;

    &-value {
      display: block;
      margin-top: 0.1em;
      font-size: 1.8em;
    }

    &.good {
      background-color: #87c13c;
      color: white;
    }

    &.moderate {
      background-color: #efbe1d;
      color: white;
    }

    &.unhealthy {
      background-color: #e84b50;
      color: white;
    }
  }
}

.bars-title {
  font-size: 0.9em;
  color: $gray600;
  margin-bottom: 0.9em;
}
</style>
