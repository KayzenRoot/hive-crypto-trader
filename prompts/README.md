# Prompt Artifacts

Hive Crypto Trader uses `GEF Bootstrap V1.0.0 Universal` as the default prompt/review engineering overlay, subordinate to the canonical HCT source hierarchy and current checkpoint authority.

## User-facing delivery

Complete executable prompts and independent-review prompts are delivered as **downloadable PDF artifacts only** under `docs/104-chat-delivery-and-prompt-artifact-policy.md`.

Do not duplicate the full prompt inline or in a chat writing/code block.

## Repository sources

Canonical Work Orders remain in `work-orders/`. Prompt-support artifacts may be stored here when repository persistence is useful, but a repository Markdown source does not replace the required user-facing PDF handoff.

Every new governed prompt should bind, when applicable:
- project/repository;
- Work Order;
- risk class;
- expected branch/base/head;
- source hierarchy/checkpoint;
- GEF task/context controls;
- scope/out-of-scope and allowed patch surface;
- preservation/security constraints;
- acceptance criteria;
- tests/evidence;
- review format;
- STOP CONDITION.

First executor prompt for a repository/session must include safe repository synchronization and Context Lock before mutation.
