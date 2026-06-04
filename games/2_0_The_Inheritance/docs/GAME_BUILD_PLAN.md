# The Inheritance — Game Build Plan

## Current Priority

Build the game in this order:

1. Visual assembly
2. Clickable UI functionality
3. Reel animation prototype
4. Temporary visual spin logic
5. Stake Engine / Math SDK integration
6. RTP and volatility simulation
7. Final math tuning
8. Publishing package

## Phase 1 — Visual Assembly

### Goal

Create a complete static game screen using the already generated PNG assets.

### Required Layers

```text
1. Intro screen
2. Main mansion background
3. Reel frame 5x4
4. Symbol grid
5. Bottom UI panel
6. Buttons
7. Balance / bet / win text rendered in code
8. Effects layer
```

### UI Layout

The main UI panel should include:

| Area | Function |
|---|---|
| Info | Opens paytable / rules screen. |
| Speed | Toggles speed level 1 and 2. |
| Volume | Toggles sound on/off. |
| Spin | Starts one spin. |
| Auto | Toggles auto spin. |
| Buy | Opens bonus buy confirmation popup. |
| Balance | Shows current balance. |
| Bet - | Reduces bet amount. |
| Bet Amount | Shows selected bet. |
| Bet + | Increases bet amount. |

## Phase 2 — Clickable UI

### Required Interactions

| Button | First Prototype Behavior |
|---|---|
| Spin | Randomly fills the 5x4 reels with symbols. |
| Speed | Switches between one-flash and two-flash state. |
| Volume | Toggle muted/unmuted. |
| Auto | Toggle auto spin state. |
| Buy | Show placeholder popup. |
| Info | Show placeholder paytable screen. |
| Bet - | Decrease bet. |
| Bet + | Increase bet. |

## Phase 3 — Reel Prototype

### Initial Reel Settings

```text
Grid: 5 columns x 4 rows
Visible symbols: 20
Spin direction: vertical
Stop order: left to right
```

### First Reel Behavior

```text
Spin click
↓
Disable buttons
↓
Animate reel blur
↓
Stop reels one by one
↓
Reveal symbols
↓
Check simple placeholder wins
↓
Enable buttons
```

## Phase 4 — Game Features Placeholder

The first visual version should support the following feature placeholders:

| Feature | Prototype Status |
|---|---|
| Legacy Key scatter | Visual only first. |
| Family Crest Wild | Visual only first. |
| Secret Vault | Placeholder popup. |
| Estate Keeper collector | No math yet. |
| Diamond Seal Multiplier | No math yet. |
| Mystery Portrait | Placeholder reveal later. |

## Phase 5 — Math Phase

Math comes after the visual prototype is stable.

### Target Math Direction

| Item | Target |
|---|---:|
| RTP | 96.2% |
| Volatility | High |
| Bonus frequency | 1 in 150–250 spins |
| Hit frequency | 25%–32% |
| Max win | 5,000x initial version |
| Grid | 5x4 |
| Pay system | 40 paylines first |

### Math Files To Build

```text
game_config.py
game_calculations.py
gamestate.py
game_override.py
game_optimization.py
reels/
library/
```

## Phase 6 — Publishing Readiness

Before publishing to Stake.krd or any real-money environment, the game must have:

- Final math model
- RTP report
- Volatility report
- Max exposure report
- Paytable
- Game rules
- Responsible gaming statement
- Provably fair verification approach where applicable
- Fully optimized assets
- Desktop and mobile testing

## Important Rule

The current visual work is not real-money ready. Do not connect the game to real-money play until the math simulation and regulatory / platform requirements are complete.
