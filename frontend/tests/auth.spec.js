// @ts-check
import {test, expect} from '@playwright/test';

const baseUrl = 'http://localhost:5173';

test.describe('Signup flow', () => {
    test('has create family account signup page', async ({page}) => {
        await page.goto(`${baseUrl}/signup`);

        await expect(page.getByRole('heading', {name: 'Create Family Account'})).toBeVisible();

        await expect(page.getByLabel(/email/i)).toBeVisible();
        await expect(page.getByLabel(/^Password$/i)).toBeVisible();
        await expect(page.getByLabel(/Confirm Password/i)).toBeVisible();
        await expect(page.getByRole('button', {name: 'Create Account'})).toBeVisible();


    });

    test('signup page - incomplete form should not be submitted', async ({page}) => {

        let requestMade = false

        await page.route('**/auth/register', async (route) => {
            requestMade = true
            await route.continue()
        })

        await page.goto(`${baseUrl}/signup`)
        await page.getByLabel(/email/i).fill('user2@example.com')
        await page.getByLabel(/^Password$/i).fill('password1234')
        await page.getByLabel(/Confirm Password/i).fill('password1234')
        await page.getByRole('button', {name: 'Create Account'}).click()

        await expect(page).toHaveURL(`${baseUrl}/signup`)
        expect(requestMade).toBe(false)
    })


    test('signup page submits with mock data', async ({page}) => {
        let requestMade = false

        await page.route('**/auth/register', async (route) => {
            await route.fulfill({
                status: 200, // TODO: should be 201
                contentType: 'application/json',
                body: JSON.stringify({
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user2@example.com",
                    "phone_number": "string",
                    "roles": "family"
                })
            })
            requestMade = true
        })

        await page.goto(`${baseUrl}/signup`)
        await page.getByLabel(/email/i).fill('user2@example.com')
        await page.getByLabel(/^Password$/i).fill('password1234')
        await page.getByLabel(/Confirm Password/i).fill('password1234')
        await page.getByLabel(/First Name/i).fill('Firstname')
        await page.getByLabel(/Last Name/i).fill('Lastname')
        await page.getByLabel(/Phone Number/i).fill('1234567890')
        await page.locator('#terms-check').click()
        await page.getByRole('button', {name: 'Create Account'}).click()

        // redirect to login page after signup
        await expect(page).toHaveURL(`${baseUrl}/login`)
        await expect(requestMade).toBe(true)
    })
})

test.describe('Login flow', () => {

})


