export class AirAiResult {
  answer: string = '';
  facts?: string[] | null;
  auxiliary_data?: LocationAirData[] | null;

  constructor(answer: string, facts?: string[] | null, auxiliary_data?: LocationAirData[] | null) {
    this.answer = answer;
    this.facts = facts;
    this.auxiliary_data = auxiliary_data;
  }
}

export class LocationAirData {
  location_name: string = '';
  data: AirDataPoint[] = [];
}

export type AirDataPoint = {
  date_unix: number;
  aqi: number;
  pm2_5: number;
  o3: number;
  co: number;
  no: number;
  no2: number;
  so2: number;
  pm10: number;
  nh3: number;
};

export type LatLng = {
  lat: number;
  lng: number;
}
