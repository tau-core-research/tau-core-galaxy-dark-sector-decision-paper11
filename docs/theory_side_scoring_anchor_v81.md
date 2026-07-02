# Theory-Side Scoring Anchor v81

## Purpose

This note records the theory-side scoring anchor now available from the Tau
Core theory hub for Paper 11.

The anchor is the restricted local `U_read` closure-defect partial-order
diagnostic:

```text
Theta_vec(c) =
(
    rank_status(ClosureStatus(c)),
    rank_obstruction(ClosureObstruction(c)),
    rank_mismatch(ClosureMismatch(c))
)
```

with the induced local partial order:

```text
c_i <=_read c_j iff Theta_vec(c_i) >=_D Theta_vec(c_j).
```

## Imported Status

The Tau Core theory hub currently records:

```text
RESTRICTED_LOCAL_ORDER_READOUT_ADMISSIBILITY_PASS_UNDER_STATED_ASSUMPTIONS
```

for the finite-local `U_read` closure-defect partial-order diagnostic.

This pass depends on the following formal gates:

```text
family non-circularity;
observer-interface admissibility;
null/gauge preservation;
CG_read conservative stability;
reported partial-order incomparability envelope.
```

## Role In Paper 11

Paper 11 may use this result only as a theory-side scoring primitive:

```text
proof-backed local scoring/readout anchor for endpoint-blind decision protocol
design.
```

It strengthens the protocol by showing that one local Tau Core scoring object
can be made:

```text
source-frozen;
non-circular;
observer-interface guarded;
null/gauge compatible;
coarse-graining conservative;
honest about incomparability.
```

## Claim Boundary

This anchor does not claim:

```text
global P_order;
global time;
physical time recovery;
physical readout;
galaxy rotation endpoint score;
dark-sector necessity or non-necessity;
dark matter rejection;
Response_tau formula;
S_tau_resp functional;
empirical validation.
```

## Paper 11 Consequence

The Paper 11 decision protocol remains blocked at the family-prediction and
formula side before endpoint scoring. The theory-side anchor only improves the
mathematical discipline of the scoring architecture.

It does not activate scoring rows, fill family prediction tables, select a
family winner, or change the current endpoint decision status.

## Status

```text
THEORY_SIDE_SCORING_ANCHOR_V81_CREATED
RESTRICTED_LOCAL_SCORING_PRIMITIVE_IMPORTED_AS_PROTOCOL_ANCHOR
ENDPOINT_SCORING_NOT_ACTIVATED_BY_THEORY_ANCHOR
DARK_SECTOR_DECISION_NOT_CLAIMED
PHYSICAL_TIME_NOT_CLAIMED
PHYSICAL_READOUT_NOT_CLAIMED
```
