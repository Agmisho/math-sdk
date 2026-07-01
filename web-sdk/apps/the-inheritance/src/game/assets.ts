const staticAsset = (path: string) => `./assets/${path.split('/').map(encodeURIComponent).join('/')}`;
const inheritanceAsset = (path: string) => staticAsset(`the-inheritance/${path}`);
const symbol = (filename: string) => ({ type: 'sprite', src: inheritanceAsset(`symbols-cleaned/${filename}`) });

export default {
	loader: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/loader/loader.atlas'),
			skeleton: staticAsset('spines/loader/loader.json'),
			scale: 2,
		},
		preload: true,
	},
	pressToContinueText: {
		type: 'sprites',
		src: staticAsset('sprites/pressToContinueText/MM_pressanywhere.json'),
		preload: true,
	},
	inheritanceBackground: {
		type: 'sprite',
		src: inheritanceAsset('backgrounds/background.png'),
		preload: true,
	},
	inheritanceLoader: {
		type: 'sprite',
		src: inheritanceAsset('ui/loader.png'),
		preload: true,
	},
	inheritanceFrame: {
		type: 'sprite',
		src: inheritanceAsset('ui/Frame1.png'),
		preload: true,
	},
	inheritanceUiPanel: {
		type: 'sprite',
		src: inheritanceAsset('ui/UI.png'),
		preload: true,
	},
	buttonSpin: { type: 'sprite', src: inheritanceAsset('buttons/Spin.png'), preload: true },
	buttonAuto: { type: 'sprite', src: inheritanceAsset('buttons/Auto.png'), preload: true },
	buttonBuy: { type: 'sprite', src: inheritanceAsset('buttons/Buy.png'), preload: true },
	buttonInfo: { type: 'sprite', src: inheritanceAsset('buttons/Info.png'), preload: true },
	buttonVolume: { type: 'sprite', src: inheritanceAsset('buttons/Volume.png'), preload: true },
	buttonSpeed: { type: 'sprite', src: inheritanceAsset('buttons/speed.png'), preload: true },
	buttonSpeedActive: { type: 'sprite', src: inheritanceAsset('buttons/speed1.png'), preload: true },
	S: symbol('Vault Scatter.png'),
	W: symbol('Wild.png'),
	M2: symbol('Diamond Seal Multiplier 2.png'),
	M5: symbol('Diamond Seal Multiplier 5.png'),
	M10: symbol('Diamond Seal Multiplier 10.png'),
	M20: symbol('Diamond Seal Multiplier 20.png'),
	M100: symbol('Diamond Seal Multiplier 100.png'),
	H1: symbol('Heiress.png'),
	H2: symbol('Covered Portrait Mystery.png'),
	H3: symbol('Treasure Chest.png'),
	H4: symbol('Legacy Key.png'),
	H5: symbol('Diamond Brooch.png'),
	H6: symbol('Antique Pocket Watch.png'),
	H7: symbol('Magnifying Glass.png'),
	H8: symbol('will.png'),
	H9: symbol('Old Letter.png'),
	L1: symbol('A.png'),
	L2: symbol('K.png'),
	L3: symbol('Q.png'),
	L4: symbol('J.png'),
	L5: symbol('10.png'),
	L6: symbol('Family Crest Wild.png'),
	explosion: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/symbols3/symbols3.atlas'),
			skeleton: staticAsset('spines/symbols3/explosion.json'),
			scale: 2,
		},
	},
	reelsFrame: {
		type: 'sprites',
		src: staticAsset('sprites/reelsFrame/reels_frame.json'),
	},
	payFrame: {
		type: 'sprite',
		src: staticAsset('sprites/payFrame/payFrame.png'),
	},
	anticipation: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/anticipation/anticipation.atlas'),
			skeleton: staticAsset('spines/anticipation/anticipation.json'),
			scale: 2,
		},
	},
	goldFont: {
		type: 'font',
		src: staticAsset('fonts/goldFont/mm_gold.xml'),
	},
	goldBlur: {
		type: 'font',
		src: staticAsset('fonts/goldBlur/miningfont_gold_blur.xml'),
	},
	silverFont: {
		type: 'font',
		src: staticAsset('fonts/silverFont/mm_silver.xml'),
	},
	purpleFont: {
		type: 'font',
		src: staticAsset('fonts/purpleFont/mm_purple.xml'),
	},
	bigwin: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/bigwin/big_wins.atlas'),
			skeleton: staticAsset('spines/bigwin/mm_bigwin.json'),
			scale: 2,
		},
	},
	globalMultiplier: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/globalMultiplier/multiframe.atlas'),
			skeleton: staticAsset('spines/globalMultiplier/multiframe.json'),
			scale: 2,
		},
	},
	fsIntro: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/fsIntro/fs_screen.atlas'),
			skeleton: staticAsset('spines/fsIntro/fs_screen.json'),
			scale: 2,
		},
	},
	fsIntroNumber: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/fsIntro/fs_screen.atlas'),
			skeleton: staticAsset('spines/fsIntro/fs_screen_number.json'),
			scale: 2,
		},
	},
	fsOutroNumber: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/fsIntro/fs_screen.atlas'),
			skeleton: staticAsset('spines/fsIntro/fs_total_number.json'),
			scale: 2,
		},
	},
	foregroundAnimation: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/foregroundAnimation/mm_bg.atlas'),
			skeleton: staticAsset('spines/foregroundAnimation/mm_bg.json'),
			scale: 2,
		},
		preload: true,
	},
	foregroundFeatureAnimation: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/foregroundFeatureAnimation/mm_bg_feature.atlas'),
			skeleton: staticAsset('spines/foregroundFeatureAnimation/mm_bg_feature.json'),
			scale: 2,
		},
		preload: true,
	},
	tumble_multiplier: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/tumbleWin/tumble_win.atlas'),
			skeleton: staticAsset('spines/tumbleWin/tumble_multiplier.json'),
			scale: 2,
		},
	},
	tumble_win: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/tumbleWin/tumble_win.atlas'),
			skeleton: staticAsset('spines/tumbleWin/tumble_win.json'),
			scale: 2,
		},
	},
	reelhouse: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/reelhouse/reelhouse_glow.atlas'),
			skeleton: staticAsset('spines/reelhouse/reelhouse_glow.json'),
			scale: 2,
		},
	},
	progressBar: {
		type: 'sprites',
		src: staticAsset('sprites/progressBar/progressBar.json'),
		preload: true,
	},
	freeSpins: {
		type: 'sprites',
		src: staticAsset('sprites/freeSpins/freeSpins.json'),
	},
	winSmall: {
		type: 'sprites',
		src: staticAsset('sprites/winSmall/MM_Localisation_winsmall.json'),
	},
	clusterWin: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/clusterWin/clusterpay.atlas'),
			skeleton: staticAsset('spines/clusterWin/clusterpay.json'),
			scale: 2,
		},
	},
	transition: {
		type: 'spine',
		src: {
			atlas: staticAsset('spines/transition/transition.atlas'),
			skeleton: staticAsset('spines/transition/transition.json'),
			scale: 2,
		},
	},
	symbolsStatic: {
		type: 'sprites',
		src: staticAsset('sprites/symbolsStatic/symbolsStatic.json'),
	},
	coins: {
		type: 'spriteSheet',
		src: staticAsset('sprites/coin/SD2_Coin.json'),
	},
	sound: {
		type: 'audio',
		src: staticAsset('audio/sounds.json'),
		preload: true,
	},
};
