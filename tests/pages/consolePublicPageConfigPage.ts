import { expect, Page } from "@playwright/test";

export class ConsolePublicPageConfigPage {
  constructor(private readonly page: Page) {}

  async open(baseUrl: string, path: string): Promise<void> {
    await this.page.goto(`${baseUrl}${path}`);
  }

  async choosePublicPageByName(pageName: string): Promise<void> {
    // 优先使用 data-testid，若后续页面无该标识可在此统一调整定位策略。
    await this.page.getByTestId("public-page-select").click();
    await this.page.getByRole("option", { name: pageName }).click();
  }

  async save(): Promise<void> {
    await this.page.getByTestId("public-page-save").click();
  }

  async assertSaveSuccess(): Promise<void> {
    await expect(this.page.getByTestId("public-page-save-success")).toBeVisible();
  }

  async readPublicLink(): Promise<string> {
    const link = this.page.getByTestId("public-page-link");
    await expect(link).toBeVisible();
    const value = await link.inputValue();
    if (!value) {
      throw new Error("公开链接为空，无法继续 portal 验证。");
    }
    return value;
  }
}
