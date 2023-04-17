export enum Quality {
  Good = 'good',
  Moderate = 'moderate',
  Unhealthy = 'unhealthy'
}

export class Bar {
  height: number = 0;
  value: number = 0;
  dateStr: string = '';
  text: string = '';
  quality: Quality = Quality.Moderate;
};

export enum Pollutant {
  pm2_5 = 'pm2_5',
  o3 = 'o3',
  co = 'co',
  no = 'no',
  no2 = 'no2',
  so2 = 'so2',
  pm10 = 'pm10',
  nh3 = 'nh3'
}

export const POLLUTANT_DISPLAY_NAMES: Record<Pollutant, string> = {
  pm2_5: 'PM2.5',
  o3: 'ozone (o3)',
  co: 'carbon monoxide (co)',
  no: 'nitrogen dioxide (no)',
  no2: 'nitrogen dioxide (no2)',
  so2: 'sulfur dioxide (so2)',
  pm10: 'PM10',
  nh3: 'ammonia (nh3)'
};

export const getQuality = (aqi: number) => {
  if (aqi < 50) return Quality.Good;
  else if (aqi < 150) return Quality.Moderate;
  else return Quality.Unhealthy;
};

