const LOCAL_RGS_URL = 'http://127.0.0.1:3008';

const requestLocalRgs = async <T>({
	method = 'POST',
	path,
	body,
}: {
	method?: 'GET' | 'POST';
	path: string;
	body?: object;
}): Promise<T> => {
	const response = await fetch(`${LOCAL_RGS_URL}${path}`, {
		method,
		headers: body ? { 'Content-Type': 'application/json' } : undefined,
		body: body ? JSON.stringify(body) : undefined,
	});

	if (!response.ok) {
		throw new Error(`Local Math SDK bridge failed (${response.status}) at ${path}.`);
	}

	return (await response.json()) as T;
};

export const localRgsClient = {
	authenticate: (options: { sessionID: string; language: string }) =>
		requestLocalRgs<any>({ path: '/wallet/authenticate', body: options }),
	endRound: (options: { sessionID: string }) =>
		requestLocalRgs<any>({ path: '/wallet/end-round', body: options }),
	endEvent: (options: { sessionID: string; eventIndex: number }) =>
		requestLocalRgs<any>({ path: '/bet/event', body: options }),
	play: (options: { sessionID: string; currency: string; amount: number; mode: string }) =>
		requestLocalRgs<any>({ path: '/wallet/play', body: options }),
	sessionConfig: () =>
		requestLocalRgs<any>({
			method: 'GET',
			path: '/game/session-config',
		}),
	replay: (options: { game: string; version: string; mode: string; event: string }) =>
		requestLocalRgs<any>({
			method: 'GET',
			path: `/bet/replay/${encodeURIComponent(options.game)}/${encodeURIComponent(options.version)}/${encodeURIComponent(options.mode)}/${encodeURIComponent(options.event)}`,
		}),
	replayRound: (options: { roundID: string }) =>
		requestLocalRgs<any>({
			method: 'GET',
			path: `/bet/replay?roundID=${encodeURIComponent(options.roundID)}`,
		}),
};
