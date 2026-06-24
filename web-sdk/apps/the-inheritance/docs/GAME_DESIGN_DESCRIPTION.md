# The Inheritance Game Design Description

This document preserves the product design supplied for The Inheritance and
reconciles it with the current validated Math SDK implementation.

## 1. Product Concept

The Inheritance is a premium 5x5 mansion-themed video slot about family wealth,
hidden heirlooms, Vault Scatters, Free Spins, Legacy Keys, and a progressive
vault-support mechanic.

The visual identity is dark green, black, antique gold, and emerald. The game
should feel expensive, historic, secretive, and mysterious. It must not become
cartoonish, futuristic, comedic, or visually generic.

The player has two connected progression paths:

- Vault Scatter path: triggers and retriggers Free Spins.
- Legacy Key path: collects settled Legacy Keys toward a 10-Key support credit.

## 2. Protected Layout

- 5 reels.
- 5 visible rows.
- Approved `Frame1` reel frame.
- Legacy Key panel to the left of the reels.
- Main controls below the reels.
- Separate Balance, Win, Bet, Spin, Speed, Auto Spin, Buy, Info, and Volume
  displays or controls.

The frame, reels, symbols, Legacy Key panel, and bottom UI must remain aligned
as the current approved composition. This document does not authorize moving
or redesigning those elements.

## 3. Visual Direction

Approved visual language:

- grand family estate interior;
- dark green walls and curtains;
- gold ornamental framing;
- emerald gemstone details;
- chandeliers and candlelight;
- antique furniture and family portraits;
- legal documents, letters, watches, magnifying glasses, brooches, chests,
  Legacy Keys, and hidden-vault imagery.

Suspense, Free Spin, multiplier, win, and transition effects must use this
inheritance-estate language and must not reuse unrelated western, mining,
cartoon, or futuristic presentation.

## 4. Current Resolved Math Contract

The supplied product brief left several values for final math confirmation.
They are now resolved by the current Math SDK and generated RTP libraries.

| Rule | Current resolved value |
| --- | --- |
| Grid | 5 reels x 5 visible rows |
| Evaluation | 15 fixed paylines, left to right |
| Minimum regular match | 3 symbols |
| RTP editions | 92%, 93%, 94%, 95%, 96%, 97% |
| Default development edition | 97% |
| Volatility direction | High target |
| Maximum win | 5000x |
| Base cost | 1x selected bet |
| Scatter Boost cost | 3x selected bet |
| Bonus Buy cost | 100x selected bet |
| Bonus Buy award | Exactly 10 Free Spins |
| Base Vault trigger | 3 = 8, 4 = 12, 5 = 15 Free Spins |
| Free Spin retrigger | 2 = +3, 3 = +5, 4 = +8, 5 = +12 |
| Legacy Key target | 10 |
| Legacy reward | One virtual Vault support credit on an eligible paid spin |
| Diamond Seals | x2, x5, x10, x20, x100 |
| Multiplier rule | Highest visible Diamond Seal applies globally to that spin |

RTP is a deployment/submission edition. It is not a player-selectable control
and must not change during a session.

## 5. Spin Modes

### Boot

The frontend `INITIAL_BOARD` initializes the visible reels.

- no debit;
- no win credit;
- no Legacy Key collection;
- no Free Spin trigger;
- no Bonus Buy state change.

Boot is a display state, not a Math SDK paid spin.

### Base

1. Debit the selected bet exactly once.
2. Generate the deterministic Math SDK result.
3. Spin and settle the final 5x5 board.
4. Evaluate paylines and the current-spin multiplier.
5. Check the effective Vault count.
6. Count settled Legacy Keys.
7. Present and credit the resolved result.

### Scatter Boost

Scatter Boost is a paid base-style spin using Math SDK mode
`scatter_boost`. It costs 3x the selected bet and uses the configured increased
Free Spin distribution. The frontend must not manufacture extra Vault symbols
or random feature results.

### Bought

1. Show the configured 100x price.
2. Block confirmation when balance is insufficient.
3. Debit the buy amount exactly once.
4. Do not also debit a normal Base bet.
5. Enter Bought mode.
6. Award exactly 10 Free Spins.
7. Run those spins without additional bet debits.
8. Show the accumulated feature total.
9. Return to Base mode.

### Free

- no normal bet debit;
- use the Free Spin reel configuration;
- show spins remaining and accumulated feature win;
- use natural Vault retrigger rules from math;
- apply the highest visible current-spin Diamond Seal;
- return safely to Base when the feature ends.

The current approved math does not collect Legacy Keys during Free Spins or
Bonus Buy. H4 remains a paying symbol when present. Changing collection
eligibility requires a new math decision, regenerated books, RTP validation,
and matching frontend event handling.

## 6. Vault Scatter

- Exact symbol ID: `S`.
- Display name: Vault Scatter.
- Frontend asset: `symbols-cleaned/Vault Scatter.png`.
- It has no independent paytable award.
- It can appear on every active base/free reel.
- It is checked from the final settled result only.
- Base trigger: 3+ effective Vaults.
- Free Spin retrigger: 2+ natural Vaults.

When the Legacy meter is active, one virtual Vault can support an eligible
paid base/scatter-boost result:

- 2 natural + 1 virtual = 3 effective Vaults = 8 Free Spins.
- 3 natural + 1 virtual = 4 effective Vaults = 12 Free Spins.
- 4+ natural + 1 virtual uses the configured 5-Vault award cap.

The Key meter resets only when this virtual Vault credit is actually consumed
to trigger the feature.

## 7. Legacy Key

- Exact symbol ID: `H4`.
- Display name: Legacy Key.
- Frontend asset: `symbols-cleaned/Legacy Key.png`.
- It is both a normal paying high symbol and the collection symbol.
- Target: 10.

Collection rules:

- start at `0 / 10`;
- count every visible H4 on the final settled 5x5 result;
- count after reel motion completes;
- never count the opening board;
- never count a result twice;
- collect only on paid Base and Scatter Boost spins in the current math;
- keep one visible progress value inside the panel;
- cap display and stored progress at 10;
- preserve 10 until the virtual Vault credit is consumed;
- reset to 0 after credit use.

## 8. Symbols

### Low

| ID | Display |
| --- | --- |
| `L1` | A |
| `L2` | K |
| `L3` | Q |
| `L4` | J |
| `L5` | 10 |
| `L6` | Family Crest |

### High

| ID | Display |
| --- | --- |
| `H1` | Heiress |
| `H2` | Covered Portrait |
| `H3` | Treasure Chest |
| `H4` | Legacy Key |
| `H5` | Diamond Brooch |
| `H6` | Antique Pocket Watch |
| `H7` | Magnifying Glass |
| `H8` | Will |
| `H9` | Old Letter |

### Special

| ID | Role |
| --- | --- |
| `W` | Wild substitute; direct pay configured for five Wilds |
| `S` | Vault Scatter / Free Spin trigger |
| `M2` | Current-spin x2 Diamond Seal |
| `M5` | Current-spin x5 Diamond Seal |
| `M10` | Current-spin x10 Diamond Seal |
| `M20` | Current-spin x20 Diamond Seal |
| `M100` | Current-spin x100 Diamond Seal |

The Wild substitutes for regular paying symbols. It does not replace Vault
Scatters, Legacy Keys, or Diamond Seal multiplier symbols.

## 9. Pay and Multiplier Rules

- Wins run left to right from reel 1 across one of 15 configured paylines.
- Multiple paylines can pay in one result.
- The line evaluator chooses the better valid Wild/substituted payout.
- Vault Scatters do not pay independently.
- Diamond Seals do not have direct line payouts.
- If multiple Diamond Seals are visible, the highest value applies.
- The selected value multiplies settled line wins for the current spin only.
- The next spin begins at x1 unless another Diamond Seal lands.
- No multiplier stacking, carry-over, or persistence is currently enabled.

The exact symbol paytable is maintained in:

- `games/2_0_The_Inheritance/game_config.py`
- `web-sdk/apps/the-inheritance/src/game/config.ts`

## 10. State Separation

The frontend must keep these concepts distinct:

- `boot`
- `base`
- `bought`
- `free`
- spinning
- stopping
- settled
- win presentation
- bonus intro
- bonus outro

Results, balance changes, and feature awards are owned by the RGS/Math SDK.
The frontend animates the already-resolved deterministic result and must not
calculate random payouts, random symbols, or random feature outcomes.

## 11. Submission Boundary

Math and frontend remain separate Stake Engine deliverables.

- Math SDK owns reels, distributions, evaluation, feature resolution, RTP,
  max-win enforcement, books, lookup tables, and deterministic events.
- Web SDK owns rendering, controls, modals, sound, animation, and typed event
  playback.
- `tools/the-inheritance-local-rgs/server.py` is development infrastructure that
  connects them locally. It is not a replacement math engine.

## 12. Disabled Future Scaffolds

The repository contains disabled scaffolds for Vault Reel transformation,
sticky-Wild Vault Free Spins, high-volatility Free Spins, Sealed Will
collection/showdown, and Covered Portrait mystery reveals.

These are not active game rules while their configuration has `enabled: False`.
They must not be advertised as playable until deterministic books, RTP
validation, frontend event playback, and approval documentation are complete.

## 13. Source Of Truth

Use these sources in this order:

1. Generated and validated Math SDK configuration/books for numeric outcomes.
2. This document for product identity, protected layout, and player experience.
3. `GAME_RULES_AND_SPIN_MODES.md` for the detailed implementation map.
4. Frontend configuration only as a mirror of Math SDK rules.

When product intent and implemented math differ, do not guess. Record the gap,
make an explicit business/math decision, regenerate and validate the math, and
then update the frontend contract.
