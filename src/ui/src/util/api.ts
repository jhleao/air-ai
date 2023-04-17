import { log } from './log';
import { AirAiResult } from './schema';

export class AirAiApi {
  private static baseUrl: string = import.meta.env.VITE_AIR_AI_API_URL || '';

  static async prompt(prompt: string, lat?: string, lng?: string): Promise<AirAiResult> {
    const url = new URL(AirAiApi.baseUrl);
    url.pathname = '/rest/v1/air';
    url.searchParams.append('prompt', prompt);
    if (lat) url.searchParams.append('lat', lat);
    if (lng) url.searchParams.append('lng', lng);
    log.info('Sending prompt request', { prompt, lat, lng });
    const response = await fetch(url);
    const data = await response.json();
    const parsedData = new AirAiResult(data.answer, data.facts, data.auxiliary_data);
    log.info('Received prompt response', { data });
    return parsedData;
  }
}
