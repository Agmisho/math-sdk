const paytable = (three: number, four: number, five: number) => [
	{ '5': five },
	{ '4': four },
	{ '3': three },
];
const wildPaytable = [{ '5': 20 }];
const configuredRtp = Number(import.meta.env.PUBLIC_THE_INHERITANCE_RTP ?? '0.97');
const supportedRtpValues = new Set([0.92, 0.93, 0.94, 0.95, 0.96, 0.97]);
const rtp = supportedRtpValues.has(configuredRtp) ? configuredRtp : 0.97;

const symbols = {
	S: { special_properties: ['scatter'] },
	W: { paytable: wildPaytable, special_properties: ['wild'] },
	M2: { special_properties: ['multiplier'] },
	M5: { special_properties: ['multiplier'] },
	M10: { special_properties: ['multiplier'] },
	M20: { special_properties: ['multiplier'] },
	M100: { special_properties: ['multiplier'] },
	H1: { paytable: paytable(0.5, 2.5, 5) },
	H2: { paytable: paytable(0.5, 2.5, 5) },
	H3: { paytable: paytable(1, 5, 10) },
	H4: { paytable: paytable(1, 5, 10), special_properties: ['collection'] },
	H5: { paytable: paytable(2, 1, 20) },
	H6: { paytable: paytable(2, 1, 20) },
	H7: { paytable: paytable(3, 6, 15) },
	H8: { paytable: paytable(2, 5, 12) },
	H9: { paytable: paytable(1.5, 4, 10) },
	L1: { paytable: paytable(0.1, 0.5, 1) },
	L2: { paytable: paytable(0.1, 0.5, 1) },
	L3: { paytable: paytable(0.1, 0.5, 1) },
	L4: { paytable: paytable(0.1, 0.5, 1) },
	L5: { paytable: paytable(0.1, 0.5, 1) },
	L6: { paytable: paytable(0.1, 0.4, 1.5) },
};

type SymbolKey = keyof typeof symbols;

const reel = (names: SymbolKey[]) => names.map((name) => ({ name }));

const basePaddingReels = [
	reel(['L1', 'H1', 'H3', 'L2', 'H3', 'S', 'L3', 'H5', 'L4', 'M2', 'H2', 'L5', 'W', 'H6', 'L6', 'H7', 'M5', 'H8', 'L1', 'H9']),
	reel(['H2', 'L2', 'H3', 'L3', 'H1', 'M2', 'L6', 'H5', 'S', 'L1', 'H6', 'L4', 'M10', 'H3', 'L5', 'W', 'H7', 'L2', 'H8', 'H9']),
	reel(['L3', 'H3', 'S', 'L1', 'M5', 'H3', 'L2', 'H1', 'L6', 'H5', 'W', 'M20', 'H2', 'L4', 'H6', 'L5', 'H7', 'M2', 'H8', 'H9']),
	reel(['L4', 'H3', 'L2', 'H2', 'S', 'H1', 'L5', 'M2', 'H3', 'L1', 'H6', 'W', 'M10', 'H5', 'L6', 'H7', 'L3', 'H8', 'M5', 'H9']),
	reel(['H5', 'L5', 'H1', 'L3', 'H3', 'M2', 'S', 'L6', 'H2', 'L1', 'W', 'H6', 'M20', 'L4', 'H3', 'H7', 'M5', 'H8', 'L2', 'H9']),
];

const freegamePaddingReels = [
	reel(['M2', 'H1', 'H3', 'M5', 'H3', 'S', 'L3', 'H5', 'M10', 'W', 'H2', 'L5', 'M20', 'H6', 'L6', 'H7', 'M2', 'H8', 'L1', 'H9', 'M100']),
	reel(['H2', 'M5', 'H3', 'L3', 'H1', 'M2', 'L6', 'H5', 'S', 'L1', 'H6', 'M10', 'W', 'H3', 'L5', 'M20', 'H7', 'L2', 'H8', 'H9']),
	reel(['L3', 'H3', 'S', 'M2', 'M5', 'H3', 'L2', 'H1', 'L6', 'H5', 'W', 'M20', 'H2', 'L4', 'H6', 'L5', 'H7', 'M10', 'H8', 'H9', 'M100']),
	reel(['L4', 'H3', 'M2', 'H2', 'S', 'H1', 'L5', 'M5', 'H3', 'L1', 'H6', 'W', 'M10', 'H5', 'L6', 'H7', 'L3', 'H8', 'M20', 'H9']),
	reel(['H5', 'L5', 'H1', 'M2', 'H3', 'M5', 'S', 'L6', 'H2', 'L1', 'W', 'H6', 'M20', 'L4', 'H3', 'H7', 'M10', 'H8', 'L2', 'H9']),
];

export default {
	providerName: 'sample_provider',
	gameName: 'the_inheritance',
	gameID: '2_0_The_Inheritance',
	rtp,
	numReels: 5,
	numRows: [5, 5, 5, 5, 5],
	betModes: {
		base: {
			cost: 1.0,
			feature: true,
			buyBonus: false,
			rtp,
			max_win: 5000.0,
		},
		scatter_boost: {
			cost: 3.0,
			feature: true,
			buyBonus: false,
			rtp,
			max_win: 5000.0,
		},
		bonus: {
			cost: 100.0,
			feature: false,
			buyBonus: true,
			rtp,
			max_win: 5000.0,
		},
	},
	paylines: {
		'1': [0, 0, 0, 0, 0],
		'2': [1, 1, 1, 1, 1],
		'3': [2, 2, 2, 2, 2],
		'4': [3, 3, 3, 3, 3],
		'5': [4, 4, 4, 4, 4],
		'6': [0, 1, 2, 3, 4],
		'7': [4, 3, 2, 1, 0],
		'8': [0, 1, 0, 1, 0],
		'9': [1, 0, 1, 0, 1],
		'10': [1, 2, 1, 2, 1],
		'11': [2, 1, 2, 1, 2],
		'12': [2, 3, 2, 3, 2],
		'13': [3, 2, 3, 2, 3],
		'14': [3, 4, 3, 4, 3],
		'15': [4, 3, 4, 3, 4],
	},
	symbols,
	paddingReels: {
		basegame: basePaddingReels,
		freegame: freegamePaddingReels,
	},
};
