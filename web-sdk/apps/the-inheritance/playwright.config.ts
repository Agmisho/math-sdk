import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
	testDir: './e2e',
	timeout: 60_000,
	expect: {
		timeout: 20_000,
	},
	fullyParallel: false,
	reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
	use: {
		baseURL: 'http://127.0.0.1:3007',
		trace: 'retain-on-failure',
		screenshot: 'only-on-failure',
		video: 'retain-on-failure',
	},
	webServer: [
		{
			command: 'python ../../../tools/the-inheritance-local-rgs/server.py',
			url: 'http://127.0.0.1:3008/health',
			timeout: 120_000,
			reuseExistingServer: false,
		},
		{
			command: 'corepack pnpm exec vite dev --host 127.0.0.1 --port 3007',
			url: 'http://127.0.0.1:3007',
			timeout: 120_000,
			reuseExistingServer: false,
		},
	],
	projects: [
		{
			name: 'chromium-desktop',
			use: {
				...devices['Desktop Chrome'],
				viewport: { width: 1440, height: 900 },
			},
		},
		{
			name: 'chromium-mobile',
			use: {
				...devices['Pixel 7'],
				viewport: { width: 412, height: 915 },
			},
		},
	],
});
