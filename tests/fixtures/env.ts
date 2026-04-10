import path from "node:path";
import dotenv from "dotenv";

dotenv.config();

function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`缺少环境变量: ${name}`);
  }
  return value;
}

export type E2EEnv = {
  consoleBaseUrl: string;
  portalBaseUrl: string;
  consoleStorageState: string;
  consoleCookie?: string;
  consolePublicPagePath: string;
  /** 下拉中要选择的场景页名称，与用例中传入一致时可由环境覆盖 */
  consoleScenePageName: string;
  /** 可选：覆盖默认的 data-testid，便于未加 testid 前联调 */
  e2ePublicPageSelectTestId?: string;
  e2ePublicPageSaveTestId?: string;
  e2ePublicPageLinkTestId?: string;
  e2ePublicPageSaveSuccessTestId?: string;
  e2ePortalRootTestId?: string;
  portalPublicSuccessText?: string;
  portalNoPermissionText?: string;
};

export function loadEnv(): E2EEnv {
  return {
    consoleBaseUrl: required("CONSOLE_BASE_URL"),
    portalBaseUrl: required("PORTAL_BASE_URL"),
    consoleStorageState: process.env.CONSOLE_STORAGE_STATE || path.join(".auth", "console.storageState.json"),
    // 兼容 Cookie/COOKIE 两种写法，避免环境变量大小写差异导致登录失败。
    consoleCookie: process.env.CONSOLE_COOKIE || process.env.COOKIE || process.env.Cookie,
    // 不再提供默认路径，强制从 .env 显式配置，避免误跑到错误页面。
    consolePublicPagePath: required("CONSOLE_PUBLIC_PAGE_PATH"),
    consoleScenePageName: process.env.CONSOLE_SCENE_PAGE_NAME || "AT_公开页面",
    e2ePublicPageSelectTestId: process.env.E2E_PUBLIC_PAGE_SELECT_TESTID,
    e2ePublicPageSaveTestId: process.env.E2E_PUBLIC_PAGE_SAVE_TESTID,
    e2ePublicPageLinkTestId: process.env.E2E_PUBLIC_PAGE_LINK_TESTID,
    e2ePublicPageSaveSuccessTestId: process.env.E2E_PUBLIC_PAGE_SAVE_SUCCESS_TESTID,
    e2ePortalRootTestId: process.env.E2E_PORTAL_ROOT_TESTID,
    portalPublicSuccessText: process.env.PORTAL_PUBLIC_SUCCESS_TEXT,
    portalNoPermissionText: process.env.PORTAL_NO_PERMISSION_TEXT
  };
}
