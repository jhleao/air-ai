import { log } from './log';
import type { LatLng } from './schema';

export class LocationUtil {
  static async hasLocationEnabled(): Promise<boolean> {
    if (!navigator.geolocation) return false;
    if (!navigator.permissions) return false;
    return navigator.permissions
      .query({ name: 'geolocation' })
      .then((result) => result.state === 'granted');
  }

  static async getLocation(): Promise<LatLng | null> {
    return new Promise((resolve) => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            resolve({
              lat: latitude,
              lng: longitude
            });
          },
          (error) => {
            log.error('Error getting location', { error });
            resolve(null);
          }
        );
      } else {
        log.error('Geolocation is not supported by this browser.');
        resolve(null);
      }
    });
  }
}
