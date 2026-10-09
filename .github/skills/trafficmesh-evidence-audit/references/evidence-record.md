# Evidence Record Fields

- `claimId`: stable identifier.
- `claim`: exact, bounded statement.
- `scope`: repository, system, city/operator, field trial, or production scope.
- `state`: evidence state asserted.
- `artifact`: path or immutable URL.
- `revision`: commit, digest, hardware revision, or version.
- `producer`: human, tool, or agent that produced it.
- `verification`: command, test, inspection, or review method and result.
- `observedAt`: timestamp of verification.
- `expiresAt`: refresh deadline, or null for immutable facts.
- `limitations`: what this evidence does not establish.