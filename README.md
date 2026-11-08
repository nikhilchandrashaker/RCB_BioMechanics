# RCB Biomechanics Lab (eras version)

Estimate-based biomechanics and shoulder-load model for **41 Royal Challengers Bengaluru players** across three overlapping groups: the IPL 2026 squad (25), the 2025 title squad (19, 16 also in the 2026 squad) and a selected 2011-17 Kohli / de Villiers / Gayle core (14, including Kohli). Roles: 11 batters, 5 wicketkeepers, 14 all-rounders, 11 bowlers.

## Important caveats
- Public sources do not provide measured joint-angle, bat-sensor or workload data. Speeds are **estimates** (broadcast readings, role archetypes) and are weaker for retired players.
- Seasonal balls bowled, balls faced and throws are **assumptions** for a typical RCB season for each player, including partial seasons. They are **not verified career statistics**. They drive the results more than the speeds do.
- The player selection is a judgment sample, not every player in RCB history. Past-era rosters come from general knowledge and should be verified.
- Results are hypotheses, not medical, injury-risk or selection guidance.

## Files
| File | What it is |
|---|---|
| `rcb_biomechanics_dataset.csv` | One row per player: role, hand, bowling type, est. speeds, action class, confidence, era, assumed workloads, load components, Shoulder Load Index (SLI), fatigue index, Monte Carlo 5th/95th percentiles, relative band, modeled carry |
| `RCB_Shoulder_Biomechanics_Paper.pdf` | Research paper: methods, 7 figures, results table |
| `rcb_figures.zip` | The figures as PNGs |
| `model.py`, `figs.py`, `paper.py` | Code that rebuilds the dataset, figures and paper |
| Dashboard and shoulder-model pages | Interactive RCB-themed pages (era filter, per-player profiles, adjustable model) |

## Dataset columns
`era`: 2026 squad, 2025 title squad, 2011-17 core (players can have several). `est_bat_speed_kph`, `est_release_kph`: estimated speeds. `est_balls_bowled_season`, `est_balls_faced_season`, `est_throws_season`: assumed workloads (`workload_basis` repeats this). `action_factor`: 1.10 slinging, 1.05 open-chest or round-arm, else 1.00. `bowling_load`, `batting_load`, `fielding_load`: components on a scale where the highest-load player (Hazlewood) is 100. `shoulder_load_index`: their sum. `peak_fatigue_idx`: peak of the recovery model. `sli_p05`, `sli_p95`: Monte Carlo range. `relative_risk_band`: Low below the sample median (56.0), Moderate to the 80th percentile (66.2), High above; a within-sample ranking, not a clinical threshold. `modeled_carry_m_vs135`: modeled carry against a 135 kph ball at 30 degrees.

Note: because the sample grew from 25 to 41 players and the scale is re-based on the highest-load player, index values differ from the earlier 25-player version for some players.

## Model
- Impact: `v_out = 0.95*v_bat + 0.25*v_in`; carry = `0.72*v_out^2*sin(60deg)/g`
- Bowling load = `(v_rel/143)^2 * action_factor * balls / 100`
- Batting load = `0.35 * (v_bat/118)^2 * balls_faced / 100`
- Fielding load = `per_throw * keeper_factor * throws / 100` (0.50 outfield, 0.25 keeper; keeper factor 1.5)
- Fatigue: `F(t+1) = F(t)*exp(-4.5/3) + L`, 14 matches, 4.5-day spacing, tau = 3 days
- Uncertainty: 2,000 draws, speed sd 3%, workload lognormal sigma 0.2, seed 7

## Reproduce / improve
Run `python model.py`, then `figs.py`, then `paper.py` (needs pandas, numpy, matplotlib, reportlab). Edit the player table at the top of `model.py` to change inputs. The highest-value upgrade is replacing assumed workloads with verified ball-by-ball and career data, then extending to the full list of RCB players.

## Known gaps
Handedness or bowling type is unverified for Mangesh Yadav, Satvik Deswal, Kanishk Chouhan, Vihaan Malhotra and Swastik Chikara. Paper citations (Dennis 2003, Gabbett 2016) are marked "verify".
