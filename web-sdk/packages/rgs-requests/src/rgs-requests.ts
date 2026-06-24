import { API_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { rgsFetcher } from 'rgs-fetcher';

import { localRgsClient } from './local-rgs-client';

export * from './types';

export const requestAuthenticate = async (options: {
	sessionID: string;
	rgsUrl: string;
	language: string;
}) => {
	if (!options.rgsUrl) {
		return localRgsClient.authenticate({
			sessionID: options.sessionID,
			language: options.language,
		});
	}

	return rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/authenticate',
		variables: {
			sessionID: options.sessionID,
			language: options.language,
		},
	});
};

export const requestEndRound = async (options: { sessionID: string; rgsUrl: string }) => {
	if (!options.rgsUrl) {
		return localRgsClient.endRound({ sessionID: options.sessionID });
	}

	return rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/end-round',
		variables: {
			sessionID: options.sessionID,
		},
	});
};

export const requestEndEvent = async (options: {
	sessionID: string;
	eventIndex: number;
	rgsUrl: string;
}) => {
	if (!options.rgsUrl) {
		return localRgsClient.endEvent({
			sessionID: options.sessionID,
			eventIndex: options.eventIndex,
		});
	}

	return rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/bet/event',
		variables: {
			sessionID: options.sessionID,
			event: `${options.eventIndex}`,
		},
	});
};

export const requestBet = async (options: {
	sessionID: string;
	currency: string;
	amount: number;
	mode: string;
	rgsUrl: string;
}) => {
	if (!options.rgsUrl) {
		return localRgsClient.play({
			sessionID: options.sessionID,
			currency: options.currency,
			amount: options.amount,
			mode: options.mode,
		});
	}

	return rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/play',
		variables: {
			mode: options.mode,
			currency: options.currency,
			sessionID: options.sessionID,
			amount: options.amount * API_AMOUNT_MULTIPLIER,
		},
	});
};

export const requestReplay = async (options: {
	game: string;
	version: string;
	mode: string;
	event: string;
	rgsUrl: string;
}) => {
	if (!options.rgsUrl) return localRgsClient.replay(options);

	return rgsFetcher.get({
		rgsUrl: options.rgsUrl,
		// @ts-ignore TODO: update the schema.ts
		url: `/bet/replay/${options.game}/${options.version}/${options.mode}/${options.event}`,
	});
};
