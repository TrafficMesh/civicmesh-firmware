---
name: trafficmesh-upstream-adoption
description: Evaluate open-source or commercial upstream options for a TrafficMesh component, dependency, adapter, or implementation change. Record whether to adopt, adapt, patch, fork, or build; use before introducing upstream code or a substantial dependency.
---

# TrafficMesh Upstream Adoption

Use at component design boundaries and for material implementation changes. Scale the review to risk. This skill does not authorize code import, issue writes, merge, deployment, production changes, or city policy decisions.

## Component review

1. Bind the owning repository/component, inspected revisions, governing project decisions/contracts, and city/operator scope. Inspect existing TrafficMesh code first.
2. State what TrafficMesh owns and its trust boundary. Separate reusable mechanics from TrafficMesh-owned identity, policy, custody of evidence, privacy, and operator authority.
3. Inspect primary source, documentation, tests, release history, license, and security notes. Compare meaningful options: adopt/configure, adapter, upstream extension, bounded patch, fork, build, or no suitable upstream.
4. Test the smallest promising seam with synthetic allow, deny, retry, recovery, and privacy cases as relevant. Label actual execution separately from documentation-based inference.
5. Produce the adoption record in `references/record-format.md`: exact revision, license evidence, excluded behavior, maintenance/update plan, replacement trigger, affected consumers, evidence, and unresolved approvals. A proposed record is not an accepted dependency.

## Implementation delta

Before code changes, resolve the component's adoption record. If absent, propose one. Check whether the task changes source revision, license, integration mode, authority boundary, or downstream contract. At review, compare the diff, dependency graph, tests, notices, and software bill of materials against the record.

## Stop conditions

- Do not import source with unknown provenance, license, or security-update path; legal compatibility belongs to qualified reviewers.
- Do not let an upstream identity, public-market, data-access, or egress model override TrafficMesh and city/operator authority.
- A fork needs an owner, patch budget, security/rebase plan, and exit path.
- Follow user and repository permissions for remote actions. Skill invocation grants none.
- A passing schema or signed artifact is not runtime evidence or authorization.