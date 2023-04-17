const isDev = import.meta.env.VITE_ENV_NAME === 'dev';
const devLogDisabled = import.meta.env.VITE_ENV_NAME === 'true';
const shouldLogInConsole = () =>
  // @ts-ignore
  (isDev && !devLogDisabled) || window.enableDevLogs;

class Logger {
  info(message: string, info?: object | null): void {
    if (shouldLogInConsole()) {
      console.log(`\x1b[46m \x1b[0m  INFO: ${message}`, info ? '\n' : '', info ? { info } : '');
    }
  }

  warn(message: string, info?: object | null): void {
    if (shouldLogInConsole()) {
      console.log(`\x1b[43m \x1b[0m  WARN: ${message}`, info ? '\n' : '', info ? { info } : '');
    }
  }

  error(message: string, info?: object | null): void {
    if (shouldLogInConsole()) {
      console.log(`\x1b[41m \x1b[107m ERROR: ${message}`, info ? '\n' : '', info ? { info } : '');
    }
  }
}

export const log = new Logger();
