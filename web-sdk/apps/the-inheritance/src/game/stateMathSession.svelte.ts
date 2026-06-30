export type MathSessionStatus = 'pending' | 'ready' | 'blocked';

export type LocalMathSessionConfig = {
	gameId: string;
	gameName: string;
	profile: string;
	rtp: number;
	manifestSha256: string;
	releasePackagePath: string;
	developmentOnly: boolean;
};

export const stateMathSession = $state({
	status: 'pending' as MathSessionStatus,
	config: null as LocalMathSessionConfig | null,
	expectedRtp: null as number | null,
	error: null as unknown,
	replayRoundID: '',
});
