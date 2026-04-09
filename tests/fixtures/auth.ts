import { Browser, BrowserContext } from "@playwright/test";
import { loadEnv } from "./env";

export async function createConsoleContext(browser: Browser): Promise<BrowserContext> {
  const env = loadEnv();
  const context = await browser.newContext();

  if (env.consoleCookie) {
    const [name, ...rest] = env.consoleCookie.split("=");
    const value = rest.join("=");
    if (!name || !value) {
      throw new Error("Cookie 格式无效，期望格式为 name=value。");
    }
    await context.addCookies([
      {
        name: name.trim(),
        value: value.trim(),
        // 对顶级域注入 cookie，保证 console 与 iam 子域都能共享登录态。
        domain: ".terminus.io",
        path: "/",
        httpOnly: true,
        secure: false
      }
    ]);
    return context;
  }

  await context.close();
  return browser.newContext({
    storageState: env.consoleStorageState
  });
}

export async function createPortalAnonymousContext(browser: Browser): Promise<BrowserContext> {
  return browser.newContext();
}
