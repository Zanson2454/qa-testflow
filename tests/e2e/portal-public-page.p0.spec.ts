import { test, expect } from "@playwright/test";
import { createConsoleContext, createPortalAnonymousContext } from "../fixtures/auth";
import { loadEnv } from "../fixtures/env";
import { ConsolePublicPageConfigPage } from "../pages/consolePublicPageConfigPage";
import { PortalPublicPageView } from "../pages/portalPublicPageView";

const env = loadEnv();

test.describe("PRD-001 portal public page @p0", () => {
  test("E2E-PRD001-P0-01 console配置公开页并拿到访问链接 @p0", async ({ browser }) => {
    const context = await createConsoleContext(browser);
    const page = await context.newPage();
    const consolePage = new ConsolePublicPageConfigPage(page);

    const publicLink = await consolePage.configureAndReadPublicLink(
      env.consoleBaseUrl,
      env.consolePublicPagePath,
      env.consoleScenePageName
    );

    expect(publicLink).toContain("http");
    await context.close();
  });

  test("E2E-PRD001-P0-02 未登录访问公开链接可正常访问 @p0", async ({ browser }) => {
    const consoleContext = await createConsoleContext(browser);
    const consoleTab = await consoleContext.newPage();
    const consolePage = new ConsolePublicPageConfigPage(consoleTab);
    const publicLink = await consolePage.configureAndReadPublicLink(
      env.consoleBaseUrl,
      env.consolePublicPagePath,
      env.consoleScenePageName
    );
    await consoleContext.close();

    const portalContext = await createPortalAnonymousContext(browser);
    const portalTab = await portalContext.newPage();
    const portalPage = new PortalPublicPageView(portalTab);
    await portalPage.open(publicLink);
    await portalPage.assertPublicPageVisible();
    await portalPage.assertSuccessTextIfConfigured(env.portalPublicSuccessText);
    await portalContext.close();
  });

  test("E2E-PRD001-P0-03 未公开页面访问被拦截 @p0", async ({ browser }) => {
    const portalContext = await createPortalAnonymousContext(browser);
    const portalTab = await portalContext.newPage();
    const portalPage = new PortalPublicPageView(portalTab);

    // portal 路径以环境提供的 BASE_URL 为准，不在脚本中追加固定路径。
    await portalPage.open(env.portalBaseUrl);
    await portalPage.assertNoPermissionIfConfigured(env.portalNoPermissionText);
    await portalContext.close();
  });
});
