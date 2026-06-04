# The Inheritance — Asset Manifest

This file tracks all visual assets required for the first playable visual prototype of **The Inheritance**.

## Folder Standard

```text
games/2_0_The_Inheritance/
├── assets/
│   ├── animations/
│   ├── backgrounds/
│   ├── Intro/
│   ├── prompts/
│   ├── Reels/
│   ├── reference/
│   ├── sounds/
│   ├── symbols/
│   └── ui/
├── library/
├── reels/
├── game_calculations.py
├── game_config.py
├── game_executables.py
├── game_optimization.py
├── game_override.py
├── gamestate.py
├── readme.txt
└── run.py
```

## UI Assets

| Asset | Save Name | Folder | Status | Notes |
|---|---|---|---|---|
| Full intro image | `inheritance_intro_full_picture_v01.png` | `assets/Intro/` | Created locally | Used as game loading / intro screen. |
| Main background | `inheritance_ui_main_background_v01.png` | `assets/backgrounds/` | Created locally | Empty mansion background behind reels. |
| Reel frame 5x4 | `inheritance_reel_frame_5x4_v01.png` | `assets/Reels/` | Created locally | Must remain equally divided: 5 columns x 4 rows. |
| Bottom UI panel | `inheritance_ui_bottom_panel_v01.png` | `assets/ui/` | Created locally | Contains spaces for Info, Speed, Volume, Spin, Auto, Buy, Balance, Bet -, Bet Amount, Bet +. |

## Button Assets

| Button | Save Name | Folder | Shape | Status | Notes |
|---|---|---|---|---|---|
| Spin | `Spin.png` | `assets/ui/` | Circular | Created locally | Main spin button. |
| Speed level 1 | `speed.png` | `assets/ui/` | Square | Created locally | One lightning flash. |
| Speed level 2 | `speed1.png` | `assets/ui/` | Square | Created locally | Two lightning flashes. |
| Volume | `Volume.png` | `assets/ui/` | Square | Created locally | Sound on icon. |
| Auto Spin | `Auto.png` | `assets/ui/` | Square | Created locally | Circular arrows icon. |
| Info | `Info.png` | `assets/ui/` | Square | Created locally | Letter `i` icon. |
| UI Panel | `UI.png` | `assets/ui/` | Wide panel | Created locally | Latest version changes Options to Info and Win to Balance. |

## Symbol Assets

| Symbol | Recommended Save Name | Folder | Function |
|---|---|---|---|
| Legacy Key | `inheritance_symbol_legacy_key_v01.png` | `assets/symbols/` | Scatter / key collection. |
| Family Crest Wild | `inheritance_symbol_family_crest_wild_v01.png` | `assets/symbols/` | Wild. |
| Secret Vault | `inheritance_symbol_secret_vault_v01.png` | `assets/symbols/` | Bonus / vault feature symbol. |
| Estate Keeper | `inheritance_symbol_estate_keeper_v01.png` | `assets/symbols/` | Collector symbol. |
| Heiress Portrait | `inheritance_symbol_heiress_portrait_v01.png` | `assets/symbols/` | Highest premium symbol. |
| Sealed Will | `inheritance_symbol_sealed_will_v01.png` | `assets/symbols/` | Premium symbol. |
| Diamond Brooch | `inheritance_symbol_diamond_brooch_v01.png` | `assets/symbols/` | Premium symbol. |
| Antique Pocket Watch | `inheritance_symbol_antique_pocket_watch_v01.png` | `assets/symbols/` | Premium symbol. |
| Treasure Chest | `inheritance_symbol_treasure_chest_v01.png` | `assets/symbols/` | Cash / premium symbol. |
| Covered Portrait Mystery | `inheritance_symbol_covered_portrait_mystery_v01.png` | `assets/symbols/` | Mystery symbol. |
| Diamond Seal Multiplier | `inheritance_symbol_diamond_seal_multiplier_v01.png` | `assets/symbols/` | Multiplier symbol. |
| Magnifying Glass | `inheritance_symbol_magnifying_glass_v01.png` | `assets/symbols/` | Premium / investigation symbol. |
| Old Letter | `inheritance_symbol_old_letter_v01.png` | `assets/symbols/` | Premium / story symbol. |
| A | `inheritance_symbol_A_v01.png` | `assets/symbols/` | Low symbol. |
| K | `inheritance_symbol_K_v01.png` | `assets/symbols/` | Low symbol. |
| Q | `inheritance_symbol_Q_v01.png` | `assets/symbols/` | Low symbol. |
| J | `inheritance_symbol_J_v01.png` | `assets/symbols/` | Low symbol. |
| 10 | `inheritance_symbol_10_v01.png` | `assets/symbols/` | Low symbol. |

## Production Notes

- Keep all source images in high-resolution PNG.
- Use game-ready resized versions for runtime.
- Recommended symbol runtime size: 256x256 or 300x300.
- Recommended square button runtime size: 256x256.
- Avoid spaces in file names.
- Keep UI text editable in code where possible; do not lock changing values into flat PNGs unless needed.
