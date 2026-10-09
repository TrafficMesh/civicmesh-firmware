---
name: trafficmesh-evidence-audit
description: Audit TrafficMesh readiness, implementation, field-trial, deployment, or production claims against artifacts, revisions, checks, scope, producer, and expiry. Use when verifying status statements or release readiness.
---

# TrafficMesh Evidence Audit

For each bounded claim, resolve its cited artifact at the stated revision and reproduce its check where safe and authorized. Classify the strongest supported state: proposed, documented, structurally checked, implemented, field-tested, deployed, or production-observed. Mark a claim unsupported when its artifact is absent, mutable without a digest, out of scope, stale, or proves a weaker state. Prose confidence does not raise evidence strength.

Return one row per input claim and list checks/evidence that could not be reproduced. Never conflate unit tests with camera calibration, bench tests with road trials, a successful deployment command with sustained operation, or docs/schema checks with runtime behavior.

Read `references/evidence-record.md`. This skill reports evidence; it cannot approve a release, claim legal compliance, merge, deploy, or authorize a field trial.