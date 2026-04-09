import { expect, Page } from "@playwright/test";

export class PortalPublicPageView {
  constructor(private readonly page: Page) {}

  async open(url: string): Promise<void> {
    await this.page.goto(url);
  }

  async assertPublicPageVisible(): Promise<void> {
    await expect(this.page.getByTestId("portal-public-page-root")).toBeVisible();
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
