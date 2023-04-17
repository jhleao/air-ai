type DateSource = Date | string | number;
type FormatDateType = 'MMM dd, yyyy' | 'MMM dd'


export class DateUtil {
  static format(source: DateSource, format: FormatDateType): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const date = new Date(source);

    const month = months[date.getMonth()];
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();

    const monthDay = `${month} ${day}`;

    if(format === 'MMM dd, yyyy') return `${monthDay}, ${year}`;

    return monthDay;
  }
}