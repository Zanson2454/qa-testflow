import { expect, Locator, Page } from "@playwright/test";
import { loadEnv } from "../fixtures/env";

/**
 * Console 侧：从首页经菜单进入「公开页面」配置，并完成选场景、保存、读取公开链接。
 * 导航步骤与业务约定一致：仅依赖 CONSOLE_BASE_URL + Cookie，不配置深层 path。
 */
export class ConsolePublicPageConfigPage {
  constructor(private readonly page: Page) {}

  private env() {
    return loadEnv();
  }

  private selectLocator(): Locator {
    const e = this.env();
    if (e.e2ePublicPageSelectTestId) {
      return this.page.getByTestId(e.e2ePublicPageSelectTestId);
    }
    return this.page
      .getByTestId("public-page-select")
      .or(this.page.getByRole("combobox").first())
      .or(this.page.locator("input[role='combobox']").first());
  }

  private saveLocator(): Locator {
    const e = this.env();
    if (e.e2ePublicPageSaveTestId) {
      return this.page.getByTestId(e.e2ePublicPageSaveTestId);
    }
    return this.page.getByTestId("public-page-save").or(this.page.getByRole("button", { name: /保存|确定|提交/ }));
  }

  private linkLocator(): Locator {
    const e = this.env();
    if (e.e2ePublicPageLinkTestId) {
      return this.page.getByTestId(e.e2ePublicPageLinkTestId);
    }
    return this.page
      .getByTestId("public-page-link")
      .or(this.page.getByPlaceholder(/http|链接|URL|地址/i));
  }

  private successLocator(): Locator {
    const e = this.env();
    if (e.e2ePublicPageSaveSuccessTestId) {
      return this.page.getByTestId(e.e2ePublicPageSaveSuccessTestId);
    }
    return this.page
      .getByTestId("public-page-save-success")
      .or(this.page.getByText(/保存成功|已保存|成功/));
  }

  /**
   * STEP1：打开 console 首页并断言登录成功特征文案。
   */
  async gotoConsoleHomeAndAssertLogin(): Promise<void> {
    const e = this.env();
    await this.page.goto(e.consoleBaseUrl, { waitUntil: "domcontentloaded" });
    await this.page.waitForLoadState("networkidle", { timeout: 30_000 }).catch(() => {});
    await expect(this.page.getByText(e.consoleLoginSuccessText)).toBeVisible({ timeout: 30_000 });
  }

  /**
   * STEP2：点击左下角头像，断言平台版本号展示。
   */
  async openAvatarAndAssertPlatformVersion(): Promise<void> {
    const e = this.env();
    const avatar = this.page.getByRole("img", { name: "avatar" }).or(this.page.locator('img[alt="avatar"]')).first();
    await expect(avatar).toBeVisible({ timeout: 15_000 });
    await avatar.click();
    // 版本号须完整出现在头像相关浮层/面板中（与产品展示一致即可，不要求整段文案完全相等）
    await expect(this.page.getByText(e.consolePlatformVersion)).toBeVisible({ timeout: 10_000 });
    await this.page.keyboard.press("Escape").catch(() => {});
  }

  /**
   * STEP3：进入门户管理，断言目标门户存在于列表。
   */
  async openPortalManagementAndAssertPortalListed(): Promise<void> {
    const e = this.env();
    await this.page.getByText(e.consolePortalMenuText, { exact: true }).first().click();
    await expect(this.page.getByText(e.consolePortalEntryName, { exact: true }).first()).toBeVisible({
      timeout: 20_000
    });
  }

  /**
   * STEP4：点击目标门户，断言出现「门户配置」。
   */
  async selectPortalAndAssertPortalConfigVisible(): Promise<void> {
    const e = this.env();
    await this.page.getByText(e.consolePortalEntryName, { exact: true }).first().click();
    await expect(this.page.getByText(e.consolePortalConfigText, { exact: true }).first()).toBeVisible({
      timeout: 20_000
    });
  }

  /**
   * STEP5：展开门户配置并进入「公开页面」子项。
   */
  async openPublicPageFromPortalConfig(): Promise<void> {
    const e = this.env();
    await this.page.getByText(e.consolePortalConfigText, { exact: true }).first().click();
    await expect(this.page.getByText(e.consolePublicPageMenuText, { exact: true }).first()).toBeVisible({
      timeout: 15_000
    });
    await this.page.getByText(e.consolePublicPageMenuText, { exact: true }).first().click();
    await this.page.waitForLoadState("networkidle", { timeout: 20_000 }).catch(() => {});
  }

  /** 完整菜单导航：STEP1 → STEP5 */
  async navigateConsoleToPublicPageModule(): Promise<void> {
    await this.gotoConsoleHomeAndAssertLogin();
    await this.openAvatarAndAssertPlatformVersion();
    await this.openPortalManagementAndAssertPortalListed();
    await this.selectPortalAndAssertPortalConfigVisible();
    await this.openPublicPageFromPortalConfig();
  }

  async choosePublicPageByName(pageName: string): Promise<void> {
    const select = this.selectLocator();
    await expect(select).toBeVisible({ timeout: 30_000 });
    await select.click();
    const escaped = pageName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    await this.page.getByRole("option", { name: new RegExp(escaped) }).click();
  }

  async save(): Promise<void> {
    const btn = this.saveLocator();
    await expect(btn).toBeVisible({ timeout: 15_000 });
    await btn.click();
  }

  async assertSaveSuccess(): Promise<void> {
    const el = this.successLocator();
    await expect(el).toBeVisible({ timeout: 15_000 });
  }

  async readPublicLink(): Promise<string> {
    const link = this.linkLocator();
    await expect(link).toBeVisible({ timeout: 20_000 });
    const value = await link.evaluate((el: HTMLElement) => {
      if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) {
        return el.value?.trim() ?? "";
      }
      if (el instanceof HTMLAnchorElement) {
        return el.href || el.textContent?.trim() || "";
      }
      return el.textContent?.trim() ?? "";
    });
    if (!value || !value.includes("http")) {
      throw new Error("公开链接为空或不是 http(s) URL，请检查页面上的链接展示控件或配置 E2E_PUBLIC_PAGE_LINK_TESTID。");
    }
    return value;
  }

  /** 菜单进入公开页 → 选场景 → 保存 → 读链接 */
  async configureAndReadPublicLink(): Promise<string> {
    await this.navigateConsoleToPublicPageModule();
    await this.choosePublicPageByName(this.env().consoleScenePageName);
    await this.save();
    await this.assertSaveSuccess();
    return this.readPublicLink();
  }
}
