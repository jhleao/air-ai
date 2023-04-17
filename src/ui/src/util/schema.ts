export class AirAiResult {
  answer: string = '';
  facts?: string[] | null;
  auxiliary_data?: LocationAirData[] | null;

  constructor(answer: string, facts?: string[] | null, auxiliary_data?: LocationAirData[] | null) {
    this.answer = answer;
    this.facts = facts;
    this.auxiliary_data = auxiliary_data;
  }
};

type LocationAirData = {
  location_name: string;
  data: AirDataPoint[];
};

type AirDataPoint = {
  date_unix: number;
  aqi: number;
  pm2_5: number;
  o3: number;
  co: number;
};
