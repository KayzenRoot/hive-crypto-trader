# Architecture

Status: `NOT_YET_DEFINED`

No runtime architecture is approved in HCT-BOOT-0001.

Governance architecture only:
`Analyze -> Source Check -> Next Necessary Increment -> Work Order -> Context Lock -> Preflight -> Executor -> Tests/Evidence -> PR -> Audit -> Verdict -> Checkpoint Delta -> Merge -> Next`

A correction never creates a new functional increment. It remains a Correction Delta under the same Work Order/PR when safe.