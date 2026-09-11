# Internationalization, Localization & Commercial Locale Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Product language policy
HCT is an English-first product targeting the United States/international English-speaking market as its initial commercial audience.

Canonical product locale: `en-US`.

Initial supported UI locales:
- `en-US` — canonical/default
- `pt-BR` — Portuguese (Brazil)
- `es` — Spanish, with future regional variants possible without architecture redesign

All new user-facing product work must be internationalization-ready from its first implementation. Localization is not a later retrofit.

## Canonical engineering language
The canonical language for source code identifiers, APIs, database/domain field names, events, telemetry keys, configuration keys, Strategy DSL keywords, node type identifiers, technical documentation, architecture records and internal machine-readable contracts is English.

Translations are presentation-layer resources. Localized text must not become canonical domain identifiers.

Example:
- canonical node id/type: `relative_strength_index`
- English label: `Relative Strength Index`
- Portuguese label: `Índice de Força Relativa`
- Spanish label: `Índice de Fuerza Relativa`

A strategy definition must therefore remain portable across languages without changing its semantic identity.

## No hard-coded user-facing strings
Frontend components must not embed product copy directly where a localization key is appropriate.

Conceptual example:
`strategy.builder.addCondition`

Locale resources resolve that key to the active language.

CI should eventually detect missing translation keys, orphaned keys and hard-coded user-facing strings where practical.

## Locale-aware presentation
The presentation layer must support locale-aware:
- dates and times;
- time zones;
- decimal/group separators;
- percentages;
- currency formatting;
- compact/large numbers;
- durations;
- relative time;
- pluralization;
- sorting/collation;
- accessibility labels;
- validation/error messages.

Trading math and stored canonical numeric values must never depend on localized display formatting.

## Commercial currency policy
Initial commercial plan pricing and canonical catalog currency are USD.

Pricing architecture must distinguish:
- canonical product price/currency;
- localized display formatting;
- taxes/fees where applicable;
- payment-provider settlement behavior;
- future regional price books if explicitly introduced.

Displaying a USD amount in Portuguese or Spanish does not automatically convert it to BRL/EUR/MXN/etc. Currency conversion or regional pricing requires a separate explicit commercial decision.

## Translation workflow
English copy is canonical. Every new user-facing feature should define English source copy and provide/queue Portuguese and Spanish translations in the same development workflow rather than postponing localization until the end.

Recommended lifecycle:
`English source key -> pt-BR translation -> es translation -> automated completeness checks -> linguistic review for sensitive surfaces -> release`

Financial, risk, security, liquidation, leverage, order, loss-limit, Copilot-autonomy and emergency-control text requires stricter review than decorative/general UI copy because mistranslation can affect user decisions.

## Strategy Builder and node localization
The nodal Strategy Builder must separate machine semantics from localized labels/descriptions.

Nodes should carry stable canonical identifiers while the UI localizes:
- node names;
- port labels;
- parameter labels;
- tooltips;
- validation errors;
- educational descriptions;
- warnings;
- strategy explanations.

A graph created in Portuguese must open in English or Spanish with identical behavior and only translated presentation text.

## Default strategy catalog localization
Every built-in strategy should provide localized:
- name where translation is appropriate;
- description;
- market/regime explanation;
- entry/exit explanation;
- risk and limitation disclosures;
- parameter help;
- validation-status explanation.

Canonical strategy IDs and versions remain language-neutral/English machine identifiers.

## Copilot localization
Copilot responses and explanations may be localized, but structured candidate actions, audit records and deterministic policy decisions must preserve canonical machine-readable fields independent of language.

Prompt/template architecture should explicitly separate locale from trading authority. A language change must never alter Safety/Risk/Execution semantics.

## Notification and transactional content
Email, in-app alerts, push notifications and future transactional messages should use the same locale-key architecture. High-assurance alerts require deterministic templates and tested translations.

## User locale model
Candidate user/tenant preferences:
- preferred UI locale;
- preferred time zone;
- preferred display currency where applicable;
- number/date formatting preference where supported.

Locale preference must not silently change exchange settlement currency, strategy math or account balances.

## SEO and public website readiness
Future marketing/public web surfaces should be prepared for locale-specific routes/metadata and `hreflang`-style localization where applicable. English/US remains the initial canonical commercial presentation.

## Testing and quality gates
Internationalization testing should include:
- missing-key detection;
- fallback behavior;
- interpolation/variable integrity;
- pluralization;
- long-string layout stress;
- locale-specific numeric/date formatting;
- chart/tooltip localization;
- node-editor localization;
- translated risk-warning snapshots;
- locale switching without semantic state mutation.

Fallback policy candidate:
`requested locale -> supported regional/base locale -> en-US`

Fallback must be visible in diagnostics, not silently corrupt content.

## Architecture rule
Internationalization is cross-cutting infrastructure, not a frontend-only concern. Backend-generated user-facing messages, notifications, reports, audit explanations and exported artifacts must use locale-aware templates or structured error/event codes that the presentation layer can localize.
