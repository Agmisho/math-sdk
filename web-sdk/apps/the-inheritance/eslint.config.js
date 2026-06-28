import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import svelte from 'eslint-plugin-svelte';
import prettier from 'eslint-config-prettier';

export default [
	{
		ignores: ['build/**', '.svelte-kit/**', 'node_modules/**', 'src/stories/data/**'],
	},
	js.configs.recommended,
	{
		files: ['**/*.js', '**/*.ts', '**/*.svelte'],
		languageOptions: {
			ecmaVersion: 2020,
			sourceType: 'module',
			globals: {
				clearTimeout: 'readonly',
				console: 'readonly',
				document: 'readonly',
				fetch: 'readonly',
				Response: 'readonly',
				setTimeout: 'readonly',
				URL: 'readonly',
				window: 'readonly',
				$state: 'readonly',
			},
		},
	},
	{
		files: ['**/*.ts'],
		languageOptions: {
			parser: tsParser,
		},
		plugins: {
			'@typescript-eslint': tsPlugin,
		},
		rules: tsPlugin.configs.recommended.rules,
	},
	...svelte.configs['flat/recommended'],
	{
		files: ['**/*.svelte.js', '**/*.svelte.ts'],
		languageOptions: {
			parser: tsParser,
		},
	},
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parserOptions: {
				parser: tsParser,
			},
		},
		rules: {
			'svelte/no-useless-mustaches': 'off',
			'svelte/require-each-key': 'off',
		},
	},
	prettier,
];
