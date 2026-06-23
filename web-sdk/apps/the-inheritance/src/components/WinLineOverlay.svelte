<script lang="ts">
	import { Graphics } from 'pixi-svelte';

	import { SYMBOL_SIZE } from '../game/constants';
	import type { Position } from '../game/types';
	import { getContext } from '../game/context';
	import { getSymbolX } from '../game/utils';

	type Point = { x: number; y: number };

	type Props = {
		positions: Position[];
		winningPositions: Position[];
		progress: number;
		alpha: number;
	};

	const props: Props = $props();
	const context = getContext();

	const clamp = (value: number) => Math.max(0, Math.min(1, value));
	const distance = (start: Point, end: Point) => Math.hypot(end.x - start.x, end.y - start.y);
	const getPositionPoint = (position: Position) => ({
		x: getSymbolX(position.reel),
		y:
			context.stateGame.board[position.reel]?.reelState.symbols[position.row]?.symbolY() ??
			SYMBOL_SIZE * (position.row - 0.5),
	});

	const points = $derived(
		[...props.positions]
			.sort((a, b) => a.reel - b.reel || a.row - b.row)
			.map(getPositionPoint),
	);
	const winningPoints = $derived(
		[...props.winningPositions]
			.sort((a, b) => a.reel - b.reel || a.row - b.row)
			.map((position) => ({
				reel: position.reel,
				...getPositionPoint(position),
			})),
	);

	const trimPolyline = (sourcePoints: Point[], progress: number) => {
		if (sourcePoints.length <= 1) return sourcePoints;

		const lengths = sourcePoints.slice(1).map((point, index) => distance(sourcePoints[index], point));
		const totalLength = lengths.reduce((total, length) => total + length, 0);
		const targetLength = totalLength * clamp(progress);
		const visiblePoints = [sourcePoints[0]];
		let traversed = 0;

		for (let index = 0; index < lengths.length; index += 1) {
			const segmentLength = lengths[index];
			const start = sourcePoints[index];
			const end = sourcePoints[index + 1];

			if (traversed + segmentLength <= targetLength) {
				visiblePoints.push(end);
				traversed += segmentLength;
				continue;
			}

			const segmentProgress = segmentLength === 0 ? 1 : (targetLength - traversed) / segmentLength;
			visiblePoints.push({
				x: start.x + (end.x - start.x) * clamp(segmentProgress),
				y: start.y + (end.y - start.y) * clamp(segmentProgress),
			});
			break;
		}

		return visiblePoints;
	};

	const drawLine = (graphics: any) => {
		const alpha = clamp(props.alpha);
		const visiblePoints = trimPolyline(points, props.progress);
		if (alpha <= 0 || visiblePoints.length < 2) return;

		const drawStroke = (width: number, color: number, strokeAlpha: number) => {
			graphics.moveTo(visiblePoints[0].x, visiblePoints[0].y);
			for (const point of visiblePoints.slice(1)) graphics.lineTo(point.x, point.y);
			graphics.stroke({ width, color, alpha: strokeAlpha * alpha, cap: 'round', join: 'round' });
		};

		drawStroke(18, 0x062a1a, 0.38);
		drawStroke(8, 0x1f7b4c, 0.58);
		drawStroke(4, 0xffe6a2, 0.92);

		const reachedReel = Math.floor((points.length - 1) * clamp(props.progress));
		for (const point of winningPoints.filter((point) => point.reel <= reachedReel)) {
			graphics.circle(point.x, point.y, SYMBOL_SIZE * 0.34);
			graphics.fill({ color: 0x062a1a, alpha: 0.2 * alpha });
			graphics.stroke({ width: 4, color: 0x2fa66c, alpha: 0.72 * alpha });
			graphics.circle(point.x, point.y, SYMBOL_SIZE * 0.24);
			graphics.stroke({ width: 2, color: 0xffe6a2, alpha: 0.86 * alpha });
		}
	};
</script>

<Graphics draw={drawLine} />
