# UADS GEF V1 Machine Evidence Specification — HCT

Status: `GOVERNED_CANDIDATE`
Schema family: `GEF_MACHINE_EVIDENCE_V1`

## Principle

Machine evidence is primary. Human narrative is a deterministic projection where practical.

## Minimal manifest

```json
{
  "schemaVersion": "GEF_MACHINE_EVIDENCE_V1",
  "workOrder": "HCT-...",
  "baseSha": "...",
  "headSha": "...",
  "taskClass": "T0|T1|T2|T3",
  "contextRadius": "C0|C1|C2|C3|C4",
  "changedFiles": [],
  "proofs": {},
  "tests": [],
  "evals": {},
  "gates": {},
  "resolvedFindings": [],
  "openFindings": [],
  "telemetry": {},
  "stopState": "COMPLETE_CANDIDATE"
}
```

## Proof entry

Each proof SHOULD contain `proofId`, `status`, material `inputs`, `validityFingerprint`, command/check identity, exit/result, exact head when hosted, and duration when available.

Valid statuses: `PASS`, `FAIL`, `CARRY_FORWARD`, `INVALIDATED`, `UNKNOWN`.

## Gate Receipt

A hosted receipt SHALL record provider, workflow, run ID, job/check, head SHA, conclusion, and required/optional classification.

A receipt must not be represented as current exact-head evidence if its head differs.

## Evidence Validity Fingerprint

The fingerprint SHALL include only material validity inputs but must include all relevant source/test/config/toolchain/policy/OS inputs. The algorithm/version must be recorded.

## Human report

Human Markdown may summarize the manifest, but cannot contradict it. If values are unavailable, write `UNKNOWN`; do not infer.

## HCT compatibility

Existing `evidence/HCT-*.md` files remain valid human evidence artifacts. New increments should progressively add a machine manifest alongside or embedded as a deterministic JSON artifact, without forcing retroactive rewrites.

## Self-reference rule

Do not require a committed evidence file to contain the SHA of the commit that contains that same file. Final exact-head/run identities belong in external gate receipts/PR evidence.
