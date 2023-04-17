import { log } from './log';
import { AirAiResult, type LatLng } from './schema';

export class AirAiApi {
  private static baseUrl: string = import.meta.env.VITE_AIR_AI_API_URL || '';

  static async prompt(prompt: string, latLng?: LatLng | null): Promise<AirAiResult> {
    const url = new URL(AirAiApi.baseUrl);
    url.pathname = '/rest/v1/air';
    url.searchParams.append('prompt', prompt);
    if (latLng) {
      url.searchParams.append('lat', latLng.lat.toString());
      url.searchParams.append('lng', latLng.lng.toString());
    }
    log.info('Sending prompt request', { prompt, latLng });
    const response = await fetch(url);

    if (response.status !== 200) throw response;

    const data = await response.json();
    const parsedData = new AirAiResult(data.answer, data.facts, data.auxiliary_data);
    log.info('Received prompt response', { data });
    return parsedData;
  }
}
