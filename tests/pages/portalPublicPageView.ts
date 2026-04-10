import { expect, Page } from "@playwright/test";
import { loadEnv } from "../fixtures/env";

export class PortalPublicPageView {
  constructor(private readonly page: Page) {}

  async open(url: string): Promise<void> {
    await this.page.goto(url, { waitUntil: "domcontentloaded" });
    await this.page.waitForLoadState("networkidle", { timeout: 30_000 }).catch(() => {});
  }

  async assertPublicPageVisible(): Promise<void> {
    const e = loadEnv();
    const root = e.e2ePortalRootTestId
      ? this.page.getByTestId(e.e2ePortalRootTestId)
      : this.page.getByTestId("portal-public-page-root").or(this.page.locator("main, [role='main'], #root").first());
    await expect(root).toBeVisible({ timeout: 20_000 });
  }

  async assertSuccessTextIfConfigured(text?: string): Promise<void> {
    if (!text) {
      return;
    }
    await expect(this.page.getByText(text)).toBeVisible();
  }

  async assertNoPermissionIfConfigured(text?: string): Promise<void> {
    if (!text) {
      return;
    }
    await expect(this.page.getByText(text)).toBeVisible();
  }
}
