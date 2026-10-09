# Upstream Adoption Record Format

Store one JSON record per component in the owning repository's documented adoption location. Keep the record revision with implementation PRs.

Required information:

- `componentId`, `repository`, `scope`: stable component owner and common/city-specific boundary.
- `status`, `decisionOwner`, `decisionRef`: proposed/accepted/deferred/rejected and who can decide.
- `governingRefs`: exact ADR, contract, or owner-approved specification revisions.
- `candidates`: source URL, exact revision, license evidence, fit, limitations, and observed results.
- `selection`: adopt, adapter, upstream extension, bounded patch, fork, or build, with reason.
- `upstreamProvides`, `trafficmeshOwns`, `excluded`: prevent duplicated concepts and authority transfer.
- `evidence`: method, artifact, revision, outcome, and limitations.
- `maintenance`: owner, update plan, patch budget, and replacement trigger.
- `openGates`: legal, security, compatibility, hardware, operator, or owner approvals outstanding.

Acceptance requires the named human decision owner and reviewed evidence. Schema validity alone does not accept a design or prove behavior.