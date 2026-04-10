import { expect, Locator, Page } from "@playwright/test";
import { loadEnv } from "../fixtures/env";

/**
 * Console 侧「公开页面」配置页面对象。
 * 定位器优先读环境变量中的 testid，便于与真实页面逐步对齐；未配置时尝试通用兜底。
 */
export class ConsolePublicPageConfigPage {
  constructor(private readonly page: Page) {}

  private env() {
    return loadEnv();
  }

  /** 若仍落在「选项目」引导页，说明 CONSOLE_PUBLIC_PAGE_PATH 未指向功能页 */
  async assertNotOnWelcomeScreen(): Promise<void> {
    const projectPicker = this.page.getByText(/Select project for resource management/i);
    const visible = await projectPicker.first().isVisible().catch(() => false);
    if (visible) {
      throw new Error(
        "当前仍在 console 项目选择引导页。请将 .env 中 CONSOLE_PUBLIC_PAGE_PATH 配成「公开页面」配置功能的完整路由（不要仅填 /team/xxx）。"
      );
    }
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

  async open(baseUrl: string, path: string): Promise<void> {
    await this.page.goto(`${baseUrl}${path}`, { waitUntil: "domcontentloaded" });
    await this.page.waitForLoadState("networkidle", { timeout: 30_000 }).catch(() => {});
    await this.assertNotOnWelcomeScreen();
  }

  async choosePublicPageByName(pageName: string): Promise<void> {
    const select = this.selectLocator();
    await expect(select).toBeVisible({ timeout: 30_000 });
    await select.click();
    await this.page.getByRole("option", { name: new RegExp(pageName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")) }).click();
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

  /** P0-02 与 P0-01 共用：打开页 → 选场景 → 保存 → 校验成功 → 读链接 */
  async configureAndReadPublicLink(baseUrl: string, path: string, pageName: string): Promise<string> {
    await this.open(baseUrl, path);
    await this.choosePublicPageByName(pageName);
    await this.save();
    await this.assertSaveSuccess();
    return this.readPublicLink();
  }
}
