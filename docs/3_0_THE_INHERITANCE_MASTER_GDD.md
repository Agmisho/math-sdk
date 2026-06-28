# The Inheritance Master GDD

Version: Release 1 working design reference

This document is the working source of truth for The Inheritance Release 1
design. Active code and generated Math SDK books remain the final authority for
runtime behavior. If this document and active code disagree, stop and reconcile
the gap before changing math or frontend behavior.

This document replaces conflicting old notes as the working design reference.
Historical documents may remain in the repository for context, but they must not
be used to override this document, `games/2_0_The_Inheritance/game_config.py`,
or generated math outputs.

## 1. Release 1 Build Order

1. Keep the completed insufficient-balance fix.
2. Finish the Legacy Key authority fix.
3. Confirm RGS/Math owns permanent Key state.
4. Maintain this Master GDD before math or frontend feature work begins.
5. Design Decree Reels in detail.
6. Implement Decree Reels in the Math SDK.
7. Rebuild books, lookup tables, and validate all RTP editions.
8. Update the local RGS event contract.
9. Update frontend event playback and animation.
10. Test and commit in small stages.

Target commit stages:

- Legacy Key correction.
- Master GDD.
- Decree Reel math.
- RGS event contract.
- Frontend animation/UI.
- Runtime validation or test report.

## 2. Authority Hierarchy

Use this order when resolving disputes:

1. Generated and validated Math SDK configuration, books, and lookup tables.
2. `games/2_0_The_Inheritance/game_config.py`.
3. This Master GDD.
4. `web-sdk/apps/the-inheritance/docs/GAME_RULES_AND_SPIN_MODES.md`.
5. Frontend config mirrors and presentation files.
6. Historical audit/baseline notes.

The frontend must not invent symbols, payouts, probabilities, free spins, or
feature outcomes. It only animates deterministic events issued by Math/RGS.

## 3. Protected Layout

Do not move, resize, or redesign these for Release 1 unless a separate visual
approval task explicitly requires it:

- `Frame1.png` and current reel frame geometry.
- 5 reels by 5 visible rows.
- Current reel positions and symbol cell alignment.
- Legacy Key panel position.
- Bottom UI layout, including buttons and hit areas.
- Background art.

Decree Reels must fit inside the current reel/frame composition. No UI geometry
changes are authorized by this document.

## 4. Active Game Overview

The Inheritance is a premium mansion inheritance slot built around a 5x5 reel
set, fixed paylines, Vault Scatters, Free Spins, Legacy Keys, Diamond Seal
multipliers, and an upcoming Decree Reels feature.

Active resolved values:

| Rule | Value |
| --- | --- |
| Grid | 5 reels x 5 visible rows |
| Win type | 15 fixed paylines |
| Direction | Left to right |
| Default RTP edition | 97% |
| Supported RTP editions | 92%, 93%, 94%, 95%, 96%, 97% |
| Max round win | 5000x |
| Base cost | 1x bet |
| Scatter Boost cost | 3x bet |
| Bonus Buy cost | 100x bet |
| Bonus Buy award | 10 Free Spins |
| Legacy Key target | 10 |
| Diamond Seal values | x2, x5, x10, x20, x100 |

## 5. Active Spin Modes

| Mode | Trigger | Debit | Feature Rules | Next State |
| --- | --- | --- | --- | --- |
| Boot | Frontend opening board | None | No win, no Key collection, no feature trigger | Base-ready |
| Base | Normal Spin | 1x bet | Can collect Keys and trigger Free Spins | Base or Free |
| Scatter Boost | Boost toggle/active mode | 3x bet | Higher configured Free Spin trigger distribution; can collect Keys | Base or Free |
| Bought | Buy Bonus confirmation | 100x bet once | Awards exactly 10 Free Spins; no extra base debit | Free |
| Free | Base/Boost trigger or Buy Bonus | None | Retriggers by natural Vaults; no current Key collection | Base after end |

## 6. Active Symbols

### Low Symbols

| ID | Display |
| --- | --- |
| `L1` | A |
| `L2` | K |
| `L3` | Q |
| `L4` | J |
| `L5` | 10 |
| `L6` | Family Crest |

### High Symbols

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

### Special Symbols

| ID | Display | Current Role |
| --- | --- | --- |
| `W` | Wild | Substitutes regular paying symbols; direct pay only for 5 Wilds; does not substitute Legacy Keys, Vault Scatters, or Diamond Seals |
| `S` | Vault Scatter | Free Spin trigger/retrigger symbol |
| `M2` | Diamond Seal x2 | Current-spin global multiplier source |
| `M5` | Diamond Seal x5 | Current-spin global multiplier source |
| `M10` | Diamond Seal x10 | Current-spin global multiplier source |
| `M20` | Diamond Seal x20 | Current-spin global multiplier source |
| `M100` | Diamond Seal x100 | Current-spin global multiplier source |
| `E` | Executor's Seal | Proposed Decree Reels trigger symbol; not implemented yet |

`E` is reserved by this document for Release 1 Decree Reels. It is not an
active runtime symbol until Math SDK config, reel strips, generated books, RGS
contract, frontend assets, and RTP validations are complete.

## 7. Active Paytable

The current paytable is authoritative in:

- `games/2_0_The_Inheritance/game_config.py`
- `web-sdk/apps/the-inheritance/src/game/config.ts`

The frontend info modal must mirror those values. The stale historical baseline
paytable is superseded.

## 8. Vault Scatter Rules

- Exact ID: `S`.
- Display name: Vault Scatter.
- Asset: `Vault Scatter.png`.
- It does not pay independently.
- It is counted from the final settled result only.
- Base/Scatter Boost trigger:
  - 3 effective Vaults: 8 Free Spins.
  - 4 effective Vaults: 12 Free Spins.
  - 5 effective Vaults: 15 Free Spins.
- Free Spin retrigger:
  - 2 natural Vaults: +3 Free Spins.
  - 3 natural Vaults: +5 Free Spins.
  - 4 natural Vaults: +8 Free Spins.
  - 5 natural Vaults: +12 Free Spins.

Legacy Key virtual Vault credit can add 1 effective Vault only on eligible paid
base/scatter-boost spins when the Key meter was already full before the spin and
at least 2 natural Vaults land.

## 9. Legacy Key Authority

- Exact ID: `H4`.
- Display name: Legacy Key.
- Asset: `Legacy Key.png`.
- It is both a paying high symbol and the collection symbol.
- Target: 10.

Authoritative state model:

- Math/RGS owns permanent Key state.
- Frontend displays `collectionUpdate.collected`.
- Frontend must not independently own or recalculate the permanent Key total.
- Opening boards never collect Keys.
- Bonus Buy trigger boards do not collect Keys.
- Free Spins do not collect Keys in the current Release 1 math.
- Paid Base and Scatter Boost spins can collect Keys.
- Collection is capped at `10 / 10`.
- When the virtual Vault credit is consumed, Math/RGS sends the reset event and
  the frontend displays `0 / 10`.

Local RGS state:

- `tools/the-inheritance-local-rgs/server.py` owns local `key_count` for the
  development session.
- The local bridge rewrites the returned `collectionUpdate` event to the current
  session count.
- The local bridge resets `key_count` only when the virtual Vault credit is
  actually used.

Frontend state:

- `stateGame.keyCounter` is a display mirror of authoritative events.
- `BoardFrame.svelte` displays exactly one progress value inside the Key panel.
- No mounted frontend component should keep a separate permanent Key total.

## 10. Diamond Seal Multipliers

Diamond Seal IDs and values:

| ID | Value |
| --- | ---: |
| `M2` | 2 |
| `M5` | 5 |
| `M10` | 10 |
| `M20` | 20 |
| `M100` | 100 |

Current active rule:

- Highest visible Diamond Seal value applies globally to current-spin line
  wins.
- Diamond Seals do not pay directly.
- No persistence or carry-over is active.
- The multiplier resets to x1 on the next spin unless another source appears.

## 11. Decree Reels Feature Design

Status: designed here, not implemented.

Public feature name: Decree Reels.

Core fantasy: the Executor's Seal stamps a legal decree onto one reel, turning
that reel into an estate-decreed Wild reel only when doing so creates or
improves a real payable result.

The existing disabled Vault Reel scaffold can be used as implementation
inspiration, but the Release 1 player-facing feature name is Decree Reels.

### Executor's Seal Symbol

| Field | Release 1 Design |
| --- | --- |
| Symbol ID | `E` |
| Display name | Executor's Seal |
| Asset file | `Executor's Seal.png` under the The Inheritance symbol asset folder |
| Classification | Special feature trigger |
| Direct pay | None |
| Substitution | Does not substitute |
| Collection | Not collected |
| Scatter role | Not a Vault Scatter |
| Multiplier role | Can reveal a Decree multiplier source when feature qualifies |

`E` must be added to math symbol roles, frontend symbol types, assets, event
fixtures, and info/paytable copy only when the Math SDK implementation begins.

### Qualifying Conditions

A Decree Reel event qualifies only when all of these are true:

1. The final settled board contains at least one `E`.
2. The spin mode is eligible by config.
3. The candidate reel has not already been converted this spin.
4. Converting the target reel to Wilds creates or improves at least one payable
   line win.
5. The improved result still respects the 5000x round cap.
6. Math can emit deterministic event data before frontend animation starts.

Default eligible modes:

| Mode | Eligible? | Notes |
| --- | --- | --- |
| Boot | No | Opening display board is never evaluated. |
| Base | Yes | Tuned to be rare. |
| Scatter Boost | Yes | Uses separate weights only if RTP tuning requires it. |
| Bought trigger board | No | Buy Bonus should enter Free Spins without extra base-board feature noise. |
| Free Spin | Yes | Higher opportunity is allowed by config and RTP tuning. |

Maximum converted reels per result:

- Base/Scatter Boost: configurable, initial target `1`.
- Free Spins: configurable, initial target `2`.
- Any higher value requires separate RTP approval.

### Reel Conversion Logic

For each qualifying `E` position:

1. Set `targetReel` to the reel containing the `E`.
2. Capture the original visible 5-symbol reel.
3. Evaluate current payable line wins before conversion.
4. Replace all visible positions on `targetReel` with `W` for line evaluation.
5. Evaluate candidate line wins after conversion at x1.
6. Reject the event if no line improves.
7. Resolve the Decree multiplier.
8. Resolve the multiplier stack.
9. Re-evaluate final line wins with the applied multiplier.
10. Apply the round cap.
11. Emit deterministic event data for frontend playback.

The transformed board is used for line evaluation. Original special-symbol
counts are still preserved for their own systems as described below.

### Multiplier Range And Weighting

Decree Reels use the current Diamond Seal value range:

| Value | Base/Boost starting weight | Free Spin starting weight |
| ---: | ---: | ---: |
| 2 | 700 | 550 |
| 5 | 200 | 250 |
| 10 | 80 | 140 |
| 20 | 18 | 50 |
| 100 | 2 | 10 |

These are starting design weights for simulation, not certified probabilities.
Final weights must be config-driven, regenerated into books, and validated for
all RTP editions before approval.

### Stack Rule

Release 1 stacking rule: `highest`.

Applied multiplier:

```text
max(natural Diamond Seal values, Decree multiplier values, 1)
```

If multiple Decree Reels resolve in one spin, all Decree multiplier sources are
included in the same highest-value stack. Sum or product stacking is not
approved for Release 1 because it would materially change volatility and RTP.

### Cap Behavior

- The 5000x max round win remains mandatory.
- Cap is applied after all line wins and the selected multiplier stack.
- The Decree event must include `capStatus`.
- If the cap truncates a Decree result, frontend must display the capped final
  amount, not the uncapped candidate amount.

## 12. Decree Interaction Order

Order inside a paid result:

1. Generate the original settled board from the Math SDK.
2. Resolve symbol attributes.
3. Emit/prepare `reveal` for the original board.
4. Resolve Legacy Key collection from the original board.
5. Resolve natural Vault Scatter count from the original board.
6. Resolve Legacy virtual Vault credit eligibility from pre-spin Key state.
7. Resolve Decree Reel candidates.
8. Emit `decreeReelResolved` events before `winInfo`.
9. Resolve Diamond Seal plus Decree multiplier stack.
10. Emit `multiplierUpdate`.
11. Evaluate line wins on the transformed board.
12. Apply Free Spin trigger/retrigger rules using the preserved Vault counts.
13. Apply max-win cap.
14. Emit win and final total events.
15. Update balance and persistent state through RGS.

Important: Vault and Key systems read the original settled board. Decree
conversion must not erase a Vault Scatter trigger or prevent a Legacy Key from
being collected when that symbol existed on the original final board.

## 13. Decree Interactions

### Diamond Seals

- Natural Diamond Seals visible on the original settled board remain eligible
  multiplier sources.
- If a Diamond Seal is on a reel later converted to Wilds, its source data must
  be preserved in the event before visual conversion.
- Decree multiplier and natural Diamond Seals use the same highest-value stack.

### Vault Scatters

- Natural Vault count is captured before Decree conversion.
- Decree conversion does not create Vaults.
- Decree conversion does not remove already-counted Vaults.
- Free Spin trigger/retrigger decisions use preserved Vault counts plus any
  valid Legacy virtual Vault credit.

### Legacy Keys

- Key collection is captured before Decree conversion.
- If an `H4` is on a reel that later converts to Wilds, it still counts because
  it was visible on the original settled board.
- Key credit consumption follows the Vault trigger rules, not the Decree result.

### Wilds

- Converted reel positions become `W` for line evaluation.
- Existing Wilds on other reels keep normal behavior.
- Five Wilds can pay direct Wild pay where the line evaluator chooses it as the
  best result.

### Free Spins And Bonus Buy

- Decree Reels may occur in Free Spins when enabled by config.
- Bought trigger boards are not Decree eligible by default.
- Bonus Buy still awards exactly 10 Free Spins and does not double-debit.

## 14. Required Decree Event Contract

New BookEvent type:

```text
decreeReelResolved
```

Minimum fields:

```text
type
index
gameType
spinMode
sourceExecutorSealSymbol
sourceExecutorSealPosition
sourceExecutorSealDisplayPosition
targetReel
originalSymbols
transformedPositions
transformedDisplayPositions
wildSymbolId
decreeMultiplierValue
decreeMultiplierSourcePosition
multiplierStack
affectedPaylines
lineWinBeforeTransform
lineWinBeforeMultiplier
finalLineWin
totalSpinWinBefore
totalSpinWinAfter
capStatus
```

`affectedPaylines` must be detailed enough for frontend line highlighting and
symbol emphasis without recalculating wins.

## 15. Math SDK Implementation Requirements

Implement Decree Reels inside the current The Inheritance Math SDK architecture.

Use or extend:

- `GameConfig`
- `GameState`
- `GameStateOverride`
- `GameExecutables`
- `GameCalculations`
- `GameEvents`
- `WinManager`
- `BetModes`
- distributions
- reel strips
- book generation
- lookup tables
- existing dev test patterns

Do not create a separate math engine.

Required math tasks:

1. Add `E` to symbol definitions and roles.
2. Add feature config under a clear `decree_reels` key.
3. Add Decree-capable reel strips or configurable distributions.
4. Resolve Decree candidates before payout resolution.
5. Preserve original-board Key, Vault, and Diamond Seal source state.
6. Emit `decreeReelResolved`.
7. Recalculate line wins after conversion.
8. Apply multiplier stack.
9. Apply 5000x cap.
10. Regenerate books/configs/lookup tables.
11. Validate 92%, 93%, 94%, 95%, 96%, and 97% RTP editions.

Required math tests:

- Decree does not trigger on boot.
- Decree does not trigger when conversion does not improve a payable result.
- Single Decree Reel improves a known line.
- Multiple `E` symbols on same reel convert only once.
- Multiple eligible reels obey `max_decree_reels_per_spin`.
- Natural Diamond Seal plus Decree multiplier applies highest value only.
- Legacy Key on converted reel still collects from original board.
- Vault Scatter on converted reel still counts from original board.
- 5000x cap still truncates correctly.
- Bonus Buy still awards 10 Free Spins and does not double-debit.

## 16. Local RGS Requirements

The local RGS must remain a bridge, not a math engine.

It must:

- pass `decreeReelResolved` events through from Math SDK books;
- preserve authoritative balance;
- preserve authoritative Key state;
- preserve Legacy virtual Vault credit state;
- preserve spin mode and Free Spin state;
- preserve profile-specific lookup table selection;
- not generate client-side or server-side random Decree events outside books.

The `/health` endpoint should keep exposing current RTP profile, lookup path,
legacy key count, and target.

## 17. Frontend Requirements

Frontend must consume deterministic Decree events.

Required visual flow:

1. Executor's Seal lands and settles.
2. Seal activates with estate/legal decree styling.
3. Target reel is marked as decreed.
4. Original reel converts to Wild reel.
5. Decree multiplier is revealed.
6. Diamond Seal and Decree stack ordering is shown clearly.
7. Winning lines highlight from event data.
8. Win amount displays the actual settled/capped amount.

Constraints:

- No UI geometry changes.
- Portrait mobile support is required.
- No frontend payout calculation.
- No frontend random symbol reveal.
- No frontend modification of permanent Key state.

## 18. Current Source File Map

Use these files as the first code references when implementing or auditing this
document:

| Area | Primary source files |
| --- | --- |
| Math config, symbols, paytable, modes, caps | `games/2_0_The_Inheritance/game_config.py` |
| Local RGS state bridge | `tools/the-inheritance-local-rgs/server.py` |
| Local RGS regression checks | `games/2_0_The_Inheritance/dev_legacy_key_credit_test.py` |
| Frontend state mirror | `web-sdk/apps/the-inheritance/src/game/stateGame.svelte.ts` |
| Frontend book event handling | `web-sdk/apps/the-inheritance/src/game/bookEventHandlerMap.ts` |
| Frontend event typing | `web-sdk/apps/the-inheritance/src/game/typesBookEvent.ts` |
| Frontend display config | `web-sdk/apps/the-inheritance/src/game/config.ts` |
| Key panel display | `web-sdk/apps/the-inheritance/src/components/BoardFrame.svelte` |
| Info/paytable modal | `web-sdk/apps/the-inheritance/src/components/InheritanceInfoModal.svelte` |
| UI controls and balance/bet display | `web-sdk/apps/the-inheritance/src/components/InheritanceUi.svelte` |

This map is not a license to duplicate math in the frontend. Frontend files
mirror and animate deterministic Math/RGS data only.

## 19. Runtime Validation Checklist

Before calling Release 1 complete:

- 10 normal spins in a row.
- Losing spin.
- Winning spin.
- Maximum bet.
- Minimum bet.
- Insufficient balance.
- Stop during spin.
- Turbo speed.
- Auto spin.
- Legacy Key collection.
- Legacy Key virtual Vault support.
- Vault Scatter trigger.
- Free Spins.
- Bonus Buy.
- Info modal.
- Decree non-trigger case.
- Decree trigger case.
- Decree plus Diamond Seal case.
- Decree plus Vault Scatter case.
- Decree plus Legacy Key case.
- Desktop landscape.
- Mobile portrait.
- No red browser console errors.
- No blank screen.
- No duplicate counter text.
- No fixed or fake win amounts.

## 20. Known Gaps Before Decree Implementation

- `E` asset does not exist yet.
- `E` is not in active math symbol types yet.
- Decree reel strips and weights have not been simulated.
- Decree event type is not in frontend `typesBookEvent.ts` yet.
- Decree animation is not implemented.
- RTP impact is unknown until generated and validated.
- Historical docs still exist, but are superseded by this Master GDD and active
  math code.

## 21. Approval Rule

Do not implement Decree Reels from memory or visual guesswork. Build from this
document, then update this document whenever code-verified math decisions change.
