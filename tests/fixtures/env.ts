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
    portalPublicSuccessText: process.env.PORTAL_PUBLIC_SUCCESS_TEXT,
    portalNoPermissionText: process.env.PORTAL_NO_PERMISSION_TEXT
  };
}
