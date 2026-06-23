import type { SymbolName } from './types';

export const SYMBOL_ROLE_KEY = 'key';
export const SYMBOL_ROLE_WILD = 'wild';
export const SYMBOL_ROLE_MULTIPLIER = 'multiplier';
export const SYMBOL_ROLE_MYSTERY = 'mystery';
export const SYMBOL_ROLE_VAULT_TRIGGER = 'vaultTrigger';
export const SYMBOL_ROLE_HIGH_PREMIUM = 'highPremium';
export const SYMBOL_ROLE_LOW_PAYING = 'lowPaying';

export type SymbolRole =
	| typeof SYMBOL_ROLE_KEY
	| typeof SYMBOL_ROLE_WILD
	| typeof SYMBOL_ROLE_MULTIPLIER
	| typeof SYMBOL_ROLE_MYSTERY
	| typeof SYMBOL_ROLE_VAULT_TRIGGER
	| typeof SYMBOL_ROLE_HIGH_PREMIUM
	| typeof SYMBOL_ROLE_LOW_PAYING;

export const SYMBOL_ROLE_SYMBOLS = {
	[SYMBOL_ROLE_KEY]: 'H4',
	[SYMBOL_ROLE_WILD]: 'W',
	[SYMBOL_ROLE_MYSTERY]: 'H2',
	[SYMBOL_ROLE_VAULT_TRIGGER]: 'S',
	[SYMBOL_ROLE_MULTIPLIER]: ['M2', 'M5', 'M10', 'M20', 'M100'],
	[SYMBOL_ROLE_HIGH_PREMIUM]: ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
	[SYMBOL_ROLE_LOW_PAYING]: ['L1', 'L2', 'L3', 'L4', 'L5', 'L6'],
} as const satisfies Record<SymbolRole, SymbolName | readonly SymbolName[]>;

export const SYMBOL_MULTIPLIER_VALUES = {
	M2: 2,
	M5: 5,
	M10: 10,
	M20: 20,
	M100: 100,
} as const satisfies Partial<Record<SymbolName, number>>;

export const SYMBOL_DISPLAY_NAMES = {
	S: 'Vault Scatter',
	W: 'Wild',
	M2: '2x Multiplier',
	M5: '5x Multiplier',
	M10: '10x Multiplier',
	M20: '20x Multiplier',
	M100: '100x Multiplier',
	H1: 'Heiress',
	H2: 'Covered Portrait',
	H3: 'Treasure Chest',
	H4: 'Legacy Key',
	H5: 'Diamond Brooch',
	H6: 'Pocket Watch',
	H7: 'Magnifying Glass',
	H8: 'Will',
	H9: 'Old Letter',
	L1: 'A',
	L2: 'K',
	L3: 'Q',
	L4: 'J',
	L5: '10',
	L6: 'Family Crest',
} as const satisfies Record<SymbolName, string>;

export const SYMBOL_ASSET_FILES = {
	S: 'Vault Scatter.png',
	W: 'Wild.png',
	M2: 'Diamond Seal Multiplier 2.png',
	M5: 'Diamond Seal Multiplier 5.png',
	M10: 'Diamond Seal Multiplier 10.png',
	M20: 'Diamond Seal Multiplier 20.png',
	M100: 'Diamond Seal Multiplier 100.png',
	H1: 'Heiress.png',
	H2: 'Covered Portrait Mystery.png',
	H3: 'Treasure Chest.png',
	H4: 'Legacy Key.png',
	H5: 'Diamond Brooch.png',
	H6: 'Antique Pocket Watch.png',
	H7: 'Magnifying Glass.png',
	H8: 'will.png',
	H9: 'Old Letter.png',
	L1: 'A.png',
	L2: 'K.png',
	L3: 'Q.png',
	L4: 'J.png',
	L5: '10.png',
	L6: 'Family Crest Wild.png',
} as const satisfies Record<SymbolName, string>;

export const symbolHasRole = (symbol: SymbolName, role: SymbolRole) => {
	const roleSymbols = SYMBOL_ROLE_SYMBOLS[role];
	return Array.isArray(roleSymbols) ? (roleSymbols as readonly SymbolName[]).includes(symbol) : roleSymbols === symbol;
};
