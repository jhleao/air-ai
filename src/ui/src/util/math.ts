export class MathUtil {
  static linearInterpolation(
    domainValue: number,
    minValue: number,
    maxValue: number,
    rangeMin: number,
    rangeMax: number
  ): number {
    const domainRange = maxValue - minValue;
    const rangeRange = rangeMax - rangeMin;
    const rangeValue = ((domainValue - minValue) * rangeRange) / domainRange + rangeMin;
    return rangeValue;
  }
}
