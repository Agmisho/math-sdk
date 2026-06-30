import { expect, test, type Page } from '@playwright/test';

const LOCAL_RGS_URL = 'http://127.0.0.1:3008';

const countVisibleScreenshotPixels = async (page: Page) => {
	const screenshot = await page.screenshot();
	return page.evaluate(async (base64Image) => {
		const image = new Image();
		image.src = `data:image/png;base64,${base64Image}`;
		await image.decode();
		const canvas = document.createElement('canvas');
		const width = Math.min(image.width, 320);
		const height = Math.min(image.height, 220);
		canvas.width = width;
		canvas.height = height;
		const context = canvas.getContext('2d');
		if (!context) return 0;
		context.drawImage(image, 0, 0, width, height);
		const data = context.getImageData(0, 0, width, height).data;
		let visiblePixels = 0;
		for (let index = 0; index < data.length; index += 16) {
			if (data[index] > 8 || data[index + 1] > 8 || data[index + 2] > 8 || data[index + 3] > 8) {
				visiblePixels += 1;
			}
		}
		return visiblePixels;
	}, screenshot.toString('base64'));
};

test('local RGS exposes the selected release RTP package', async ({ request }) => {
	const response = await request.get(`${LOCAL_RGS_URL}/game/session-config`);
	expect(response.ok()).toBe(true);
	const sessionConfig = await response.json();
	expect(sessionConfig).toMatchObject({
		gameId: '2_0_The_Inheritance',
		gameName: 'The Inheritance',
		developmentOnly: true,
	});
	expect([92, 93, 94, 95, 96, 97]).toContain(sessionConfig.rtp);
	expect(sessionConfig.profile).toBe(`rtp_${sessionConfig.rtp}`);
	expect(sessionConfig.manifestSha256).toMatch(/^[a-f0-9]{64}$/);
});

test('game renders without blank canvas or browser console errors', async ({ page }) => {
	const consoleErrors: string[] = [];
	page.on('console', (message) => {
		if (message.type() === 'error') consoleErrors.push(message.text());
	});

	await page.goto('/');
	await expect(page.getByTestId('the-inheritance-app')).toBeVisible();
	await expect(page.locator('canvas').first()).toBeVisible();
	await expect.poll(() => countVisibleScreenshotPixels(page)).toBeGreaterThan(300);
	expect(consoleErrors).toEqual([]);
});

test('audio and loader assets resolve for release QA', async ({ request }) => {
	for (const path of [
		'/assets/the-inheritance/audio/main-theme.mp3',
		'/assets/the-inheritance/audio/spin.mp3',
		'/assets/the-inheritance/audio/scatter-landing.mp3',
		'/assets/the-inheritance/ui/loader.png',
	]) {
		const response = await request.get(path);
		expect(response.ok(), `${path} should resolve`).toBe(true);
		const bytes = await response.body();
		expect(bytes.length, `${path} should not be empty`).toBeGreaterThan(0);
	}
});
