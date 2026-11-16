# Canary rollout replay

> **This is a replay of test conversations, not real users.** None of these projects has live traffic.

Method: in the project's frozen comparison both versions already answered the same items. The replay treats each stored conversation as a request and hashes "item#run" into buckets 0–99; requests below the canary share are served by the staging version's stored answer, the rest by production. The share goes 10% → 50% → 100%; at each step the rollback rules below (written before the replay) are checked, and if one fires the replay stops and production stays.

Rollback rules:

- staging's share of malformed advice is above production's
- staging loses brand or price more often than production
- staging's mean cost per conversation is more than 10% above production's

The samples are tiny (a few to a few dozen conversations per step), so this shows the mechanism, not a statistical result.

## `grounded-review/advice`: v1.1 → v1.3

Requests replayed: 36 (mt4: 12 new ads, 3 runs per version)

| Canary share | Served by staging | Malformed advice | Brand or price lost | Mean cost | Rules fired |
|---|---|---|---|---|---|
| 10% | 1 | staging 0/1 · production 6/35 | staging 0/1 · production 2/35 | staging 0.0057 · production 0.0069 | none |
| 50% | 17 | staging 0/17 · production 3/19 | staging 0/17 · production 1/19 | staging 0.0065 · production 0.0072 | none |
| 100% | 36 | staging 0/36 · production 6/36 | staging 0/36 · production 2/36 | staging 0.0068 · production 0.0069 | none |

**Result: full release.** No rule fired at any step; production moves to v1.3.

Cost is in US dollars. At the 100% step no request is served by production, so production's stored answers to all requests are the reference.

Source files: `grounded-review-public/eval/results/multiturn-mt4-v1.1.jsonl` (bb262b3d8268), `grounded-review-public/eval/results/multiturn-mt4-v1.3.jsonl` (ff1db0e0ca09)

## `grounded-review/advice`: v1.1 → v1.2

Requests replayed: 36 (mt3: 12 new ads, 3 runs per version)

| Canary share | Served by staging | Malformed advice | Brand or price lost | Mean cost | Rules fired |
|---|---|---|---|---|---|
| 10% | 3 | staging 0/3 · production 4/33 | staging 0/3 · production 3/33 | staging 0.0076 · production 0.0069 | none |
| 50% | 15 | staging 3/15 · production 3/21 | staging 1/15 · production 3/21 | staging 0.0080 · production 0.0066 | staging's share of malformed advice is above production's; staging's mean cost per conversation is more than 10% above production's |

**Result: rollback.** Production stays at v1.1; v1.2 is withdrawn.

Cost is in US dollars.

Source files: `grounded-review-public/eval/results/multiturn-mt3-v1.1.jsonl` (903512b60ade), `grounded-review-public/eval/results/multiturn-mt3-v1.2.jsonl` (547256bcdcb8)
