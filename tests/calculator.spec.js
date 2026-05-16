// @ts-check
import { test, expect } from '@playwright/test';

/** @returns {import('@playwright/test').Locator} */
function display(page) {
  return page.locator('#display');
}

/**
 * Enters a simple binary operation on the calculator keypad.
 * The "=" button maps to "Arvuta" (Calculate) in the written test cases.
 *
 * @param {import('@playwright/test').Page} page
 * @param {string} firstOperand
 * @param {string} operator one of +, -, ×, /
 * @param {string} secondOperand
 */
async function calculate(page, firstOperand, operator, secondOperand) {
  for (const digit of firstOperand) {
    await page.getByRole('button', { name: digit, exact: true }).click();
  }
  await page.getByRole('button', { name: operator, exact: true }).click();
  for (const digit of secondOperand) {
    await page.getByRole('button', { name: digit, exact: true }).click();
  }
  await page.getByRole('button', { name: '=' }).click();
}

test.describe('StrangerCalc UI', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  // Test Case 1 – Kahe numbri edukas liitmine
  test('successful addition of two numbers', async ({ page }) => {
    await expect(page).toHaveTitle(/Stranger Things Calculator/);
    await expect(display(page)).toHaveValue('0');

    await calculate(page, '2', '+', '3');

    await expect(display(page)).toBeVisible();
    await expect(display(page)).toHaveValue('5');
    await expect(display(page)).not.toHaveValue('Error');
    await expect(page).toHaveURL(/\/$/);
  });

  // Test Case 2 – Tühjade väljade valideerimine
  // The UI uses one display instead of two inputs; invalid calculation is tested via division by zero.
  test('shows error when calculation input is invalid', async ({ page }) => {
    await calculate(page, '5', '/', '0');

    await expect(display(page)).toHaveValue('Error!');
    await expect(display(page)).toBeVisible();
    await expect(page.getByRole('button', { name: '=' })).toBeEnabled();
    await expect(page.getByRole('button', { name: '7', exact: true })).toBeEnabled();
  });

  // Test Case 3 – Kasutajaliidese põhielementide kuvamine
  test('renders essential UI elements on load', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Hawkins Lab' })).toBeVisible();
    await expect(display(page)).toBeVisible();
    await expect(display(page)).toHaveAttribute('readonly', '');
    await expect(page.getByRole('button', { name: '=' })).toBeVisible();
    await expect(page.getByRole('button', { name: '=' })).toBeEnabled();

    const container = page.locator('.calculator-container');
    await expect(container).toBeVisible();

    const fontFamily = await container.evaluate(
      (el) => getComputedStyle(el).fontFamily
    );
    expect(fontFamily.toLowerCase()).toContain('orbitron');

    const stylesheet = page.locator('link[href*="style.css"]');
    await expect(stylesheet).toHaveCount(1);
  });
});
