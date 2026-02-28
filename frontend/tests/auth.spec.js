// @ts-check
import { test, expect } from '@playwright/test';

const baseUrl = 'http://localhost:5173';

test.describe('Signup flow', () => {
  test('page exists - create family account signup page', async ({ page }) => {
    const response = await page.goto(`${baseUrl}/signup`);

    await expect(response?.status()).toBe(200);
    await expect(
      page.getByRole('heading', { name: 'Create Family Account' }),
    ).toBeVisible();
  });

  test('page components exist', async ({ page }) => {
    await page.goto(`${baseUrl}/signup`);

    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/^Password$/i)).toBeVisible();
    await expect(page.getByLabel(/Confirm Password/i)).toBeVisible();
    await expect(page.getByLabel(/First Name/i)).toBeVisible();
    await expect(page.getByLabel(/Last Name/i)).toBeVisible();
    await expect(page.getByLabel(/Phone Number/i)).toBeVisible();
    await expect(page.locator('#terms-check')).toBeVisible();

    await expect(
      page.getByRole('button', { name: 'Create Account' }),
    ).toBeVisible();
  });

  test('incomplete form should not be submitted', async ({ page }) => {
    let requestMade = false;

    await page.route('**/auth/register', async (route) => {
      requestMade = true;
      await route.continue();
    });

    await page.goto(`${baseUrl}/signup`);
    await page.getByLabel(/email/i).fill('user2@example.com');
    await page.getByLabel(/^Password$/i).fill('password1234');
    await page.getByLabel(/Confirm Password/i).fill('password1234');
    await page.getByRole('button', { name: 'Create Account' }).click();

    await expect(page).toHaveURL(`${baseUrl}/signup`);
    expect(requestMade).toBe(false);
  });

  test('submits with mock data', async ({ page }) => {
    let requestMade = false;

    await page.route('**/auth/register', async (route) => {
      await route.fulfill({
        status: 200, // TODO: should be 201
        contentType: 'application/json',
        body: JSON.stringify({
          first_name: 'string',
          last_name: 'string',
          email: 'user2@example.com',
          phone_number: 'string',
          roles: 'family',
        }),
      });
      requestMade = true;
    });

    await page.goto(`${baseUrl}/signup`);
    await page.getByLabel(/email/i).fill('user2@example.com');
    await page.getByLabel(/^Password$/i).fill('password1234');
    await page.getByLabel(/Confirm Password/i).fill('password1234');
    await page.getByLabel(/First Name/i).fill('Firstname');
    await page.getByLabel(/Last Name/i).fill('Lastname');
    await page.getByLabel(/Phone Number/i).fill('1234567890');
    await page.locator('#terms-check').click();
    await page.getByRole('button', { name: 'Create Account' }).click();

    // redirect to login page after signup
    await expect(page).toHaveURL(`${baseUrl}/login`);
    await expect(requestMade).toBe(true);
  });
});

test.describe('Login flow', () => {
  test('page exists', async ({ page }) => {
    const response = await page.goto(`${baseUrl}/login`);
    await expect(response?.status()).toBe(200);
    await expect(
      page.getByRole('heading', { name: /welcome back/i }),
    ).toBeVisible();
  });

  test('page components exist', async ({ page }) => {
    await page.goto(`${baseUrl}/login`);

    await expect(page.getByLabel(/username/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /log in/i })).toBeVisible();
  });

  // TODO: Maybe we should prevent empty form being submitted, currently it's allowed

  test('successful login redirects to home page', async ({ page }) => {
    let requestMade = false;

    await page.route('**/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user_info: {
            id: 1,
            email: 'user@example.com',
            phone_number: 'string',
            first_name: 'string',
            access_token:
              'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTc3MTI5OTM2OCwiaWF0IjoxNzcxMjk3NTY4fQ.OH_DGvWr1aTJg8_DcLi4ZGHhtTR_2PKuGH0igPNBhqk',
          },
        }),
      });
      requestMade = true;
    });

    await page.goto(`${baseUrl}/login`);
    await page.getByLabel(/username/i).fill('user@example.com');
    await page.getByLabel(/password/i).fill('password1234');
    await page.getByRole('button', { name: /log in/i }).click();

    await expect(page).toHaveURL(`${baseUrl}/`);
    await expect(requestMade).toBe(true);
  });

  // TODO: invalid credentials shouldn't be redirected
  test('unsuccessful login should not be redirected', async ({ page }) => {
    let requestMade = false;

    await page.route('**/auth/login', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({
          detail: '401: Invalid credentials',
        }),
      });
      requestMade = true;
    });

    await page.goto(`${baseUrl}/login`);
    await page.getByLabel(/username/i).fill('user@example.com');
    await page.getByLabel(/password/i).fill('password12345');
    await page.getByRole('button', { name: /log in/i }).click();

    await expect(page).toHaveURL(`${baseUrl}/login`);
    await expect(requestMade).toBe(true);
  });
});

test.describe('Protected routes', () => {
  const protectedRoutes = ['dashboard'];

  test('redirects to login page if not logged in', async ({ page }) => {
    await Promise.all(
      protectedRoutes.map(async (route) => {
        await page.goto(`${baseUrl}/${route}`);
        await expect(page).toHaveURL(`${baseUrl}/login`);
      }),
    );
  });

  test('redirects to original page after logged in', async ({ page }) => {
    const originalProtectedRoute = `${baseUrl}/${protectedRoutes[0]}`;
    let requestMade = false;

    await page.route('**/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user_info: {
            id: 1,
            email: 'user@example.com',
            phone_number: 'string',
            first_name: 'string',
            access_token:
              'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTc3MTI5OTM2OCwiaWF0IjoxNzcxMjk3NTY4fQ.OH_DGvWr1aTJg8_DcLi4ZGHhtTR_2PKuGH0igPNBhqk',
          },
        }),
      });
      requestMade = true;
    });

    await page.goto(originalProtectedRoute);
    // 1. redirects to login page
    await expect(page).toHaveURL(`${baseUrl}/login`);

    await page.getByLabel(/username/i).fill('user@example.com');
    await page.getByLabel(/password/i).fill('password1234');
    await page.getByRole('button', { name: /log in/i }).click();

    // 2. redirects back to original page after login, without another redirection to the login page
    await expect(page).toHaveURL(originalProtectedRoute);
    await expect(requestMade).toBe(true);
  });
});
