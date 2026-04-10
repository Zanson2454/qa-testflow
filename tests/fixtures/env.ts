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
  /** 登录成功页特征文案 */
  consoleLoginSuccessText: string;
  /** 头像菜单中展示的平台版本号（完整断言） */
  consolePlatformVersion: string;
  /** 侧栏/菜单：门户管理 */
  consolePortalMenuText: string;
  /** 门户列表中的门户名称 */
  consolePortalEntryName: string;
  /** 配置区：门户配置 */
  consolePortalConfigText: string;
  /** 子菜单：公开页面 */
  consolePublicPageMenuText: string;
  /** 进入公开页面配置后，下拉选择的场景页名称（可选覆盖，默认 AT_公开页面） */
  consoleScenePageName: string;
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
    consoleCookie: process.env.CONSOLE_COOKIE || process.env.COOKIE || process.env.Cookie,
    consoleLoginSuccessText: process.env.CONSOLE_LOGIN_SUCCESS_TEXT || "欢迎登入系统~",
    consolePlatformVersion: process.env.CONSOLE_PLATFORM_VERSION || "3.0.2603-beta.0315",
    consolePortalMenuText: process.env.CONSOLE_PORTAL_MENU_TEXT || "门户管理",
    consolePortalEntryName: process.env.CONSOLE_PORTAL_ENTRY_NAME || "TERP 运营端",
    consolePortalConfigText: process.env.CONSOLE_PORTAL_CONFIG_TEXT || "门户配置",
    consolePublicPageMenuText: process.env.CONSOLE_PUBLIC_PAGE_MENU_TEXT || "公开页面",
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
