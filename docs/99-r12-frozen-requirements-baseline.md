# HCT-PLAN-0001-R12 — Frozen Requirements Baseline

Status: `FREEZE_CANDIDATE`
Baseline ID: `HCT-REQ-BASELINE-V1-CANDIDATE`
Increment: `HCT-PLAN-0001-R12`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define one normative, lossless requirements baseline without copying and potentially corrupting thousands of lines of already approved requirements.

The HCT frozen requirements baseline is a **composite immutable specification**: every component below is included in full by repository path and Git blob SHA. The source content is normative byte-for-byte at the recorded blob. Historical status labels inside a component do not override this manifest's freeze status.

## Normative components

| Component | Canonical source | Frozen source blob SHA | Requirement identity model |
|---|---|---|---|
| CORE/R01–R03 | `docs/02-requirements.md` | `292da9552ae816e4d51b8a299456305da1658e55` | exact file content; deterministic derived locator `REQ02::<heading>::B<ordinal>` for unnumbered bullets |
| R04 Execution | `docs/48-r04-execution-requirements-addendum.md` | `f20c1ed00bdb13801aaff8a3b648371bfcffba58` | exact file content; derived locator `R04::<heading>::B<ordinal>` for requirement bullets/invariants |
| R05 Realtime | `docs/54-r05-realtime-requirements-addendum.md` | `636ad01da9c25e760dd5e2f033b93a0f04578a17` | exact file content; derived locator `R05::<heading>::B<ordinal>` |
| R06 Intelligence | `docs/61-r06-intelligence-requirements-addendum.md` | `fea197e60532eb6ff3b11b628b9aabcbcfc00c41` | explicit `INT-001..INT-026` plus validation/safety clauses |
| R07 Validation Lab | `docs/67-r07-validation-laboratory-requirements-addendum.md` | `c8a426966c5a0dc34704d1413f506332e770c2c7` | explicit `VAL-001..VAL-032` plus validation/safety clauses |
| R08 Multi-tenant Security | `docs/73-r08-multitenant-security-requirements-addendum.md` | `c859c0c4a718e3017c34aa50013d4c50959853b4` | explicit TEN/SEC/IAM/ADM/COM/DATA/OPS IDs plus safety clause |
| R09 Cockpit/UI | `docs/80-r09-cockpit-uiux-requirements-addendum.md` | `bc897ebd470857a53055bdee85128b5bd31a5822` | explicit `R09-REQ-001..040` plus scope invariant |
| R10 Observability/Incident/FinOps | `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` | `023187ef23b01d5a11f978bbfe6e38abf172bb3b` | explicit `R10-REQ-001..045` plus scope invariant |
| R11 Integration | `docs/93-r11-integration-requirements-addendum.md` | `6935e9973696d5b706546d63d847ea398780d936` | explicit `R11-REQ-001..025` plus scope invariant |

## Baseline inclusion rule
Every normative statement in the nine frozen source blobs is included. The baseline does not rely on a shortened paraphrase.

This gives a direct no-loss property:
`Frozen Requirements = exact union of the nine recorded source blobs, subject only to explicit Decisions Ledger precedence for genuine conflicts.`

No requirement is removed merely because two sources overlap.

## Stable locators for pre-ID requirements
R01–R05 material contains requirements that predate the explicit ID convention. R12 does not rewrite those semantics just to make the documents look uniform.

For traceability, a stable derived locator is defined from the frozen source:
- normalized source prefix (`REQ02`, `R04`, `R05`);
- nearest markdown heading path;
- 1-based ordinal of the normative bullet within that heading;
- optional invariant/validation suffix when the requirement is in a named invariant/validation section.

Example form:
`R04::Unknown outcome requirements::B3`

Because the blob is frozen, heading + ordinal deterministically identifies the same normative statement. Future implementation tooling may additionally assign UUIDs, but it must preserve this source locator.

## Existing explicit requirement namespaces
The following namespaces remain canonical and SHALL NOT be renumbered during implementation:
- `INT-*`;
- `VAL-*`;
- `TEN-*`;
- `SEC-*`;
- `IAM-*`;
- `ADM-*`;
- `COM-*`;
- `DATA-*`;
- `OPS-*`;
- `R09-REQ-*`;
- `R10-REQ-*`;
- `R11-REQ-*`.

At least 209 individually numbered formal requirements exist across R06–R11, in addition to the exact frozen unnumbered requirements in CORE/R04/R05 and named validation/safety/invariant clauses.

## Precedence and conflict resolution
The frozen requirement set is interpreted under the repository source hierarchy.

When two requirement statements materially conflict:
1. approved Decisions Ledger controls the decision;
2. later approved formal round requirement/architecture controls earlier wording within its scope;
3. stricter HIGH_ASSURANCE safety/security/risk restriction controls where the conflict is merely permissive vs restrictive and no decision says otherwise;
4. unresolved material conflicts block freeze/implementation until explicitly resolved.

Overlap is not a conflict and is preserved for traceability.

## Applicability
Requirement applicability derives from current Scope plus `docs/92-r11-v1-module-classification-and-integration-hardening.md`:
- `V1_CORE` requirements are required for the intended V1 foundation;
- `V1_MINIMUM` requirements require the bounded V1 subset defined by Scope/R11 while advanced depth may be deferred;
- `IMPORTANT_POST_V1` remains architecturally governed but is not required for V1 completion unless separately promoted;
- `FUTURE` remains excluded from V1 activation unless a later explicit decision promotes it.

A requirement's safety/authority restriction continues to apply whenever the related capability exists, even if advanced functionality is deferred.

## Architecture readiness vs activation
Presence in this baseline does not imply that the highest-risk capability is active.

Examples:
- Copilot architecture may be V1 while production `FULL_COPILOT` remains unactivated;
- multi-tenant foundations are V1 while broad commercialization remains conditional;
- limited-live semantics are planned while `limited_live_authorized=false`;
- exchange abstraction is V1 while live venues other than MEXC remain FUTURE.

## Freeze status of source files
The internal round-local status labels in source components are historical metadata. Once this R12 baseline receives `FREEZE_APPROVED` and is merged/promoted, the exact recorded blobs above are **frozen normative requirements components** regardless of those historical labels.

A source component changing to a new blob SHA after freeze constitutes baseline drift and requires governed change control before the changed content can become normative.

## Change control after freeze
A material change to frozen requirements requires:
1. explicit change increment / Work Order scope;
2. source/requirement IDs affected;
3. reason and impact analysis across Scope, Architecture, Security, Risk, tests, DoD and dependent modules;
4. Decisions Ledger entry when behavior/scope/authority changes materially;
5. updated traceability and baseline manifest/version;
6. applicable regression/re-audit evidence;
7. checkpoint promotion.

Silent in-place semantic changes are prohibited.

## Authorization invariant
This requirements baseline is a planning artifact only.

Even after `FREEZE_APPROVED`:
- `implementation_authorized=false` until separately granted;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

## Finalization rule
Before R12 can approve freeze, the final audit SHALL verify that each recorded source path still resolves to the exact blob SHA above on the R12 branch unless the baseline itself is deliberately updated with an explained, audited correction.
