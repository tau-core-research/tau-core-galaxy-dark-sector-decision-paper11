# Frozen Policy Bundle Instance v01

**Doc class:** frozen-reference policy bundle  
**Status:** v01 reference freeze only; no field-complete manifest, no response formula, no endpoint scoring  

This document records the first Paper 11 policy-bundle instance:

```text
PB11_v01
```

It freezes references to the current Tau Core dark-sector policy/stub layer so
that later endpoint work cannot silently redefine source, state, admissibility,
term, selection, or channel policies after looking at galaxy residuals.

The machine-readable manifest is:

```text
data/source_manifest/frozen_policy_bundle_instance_v01.csv
```

## What Is Frozen

The bundle freezes references to:

- `B_tau^base` carrier stub
- `B_tau^base` null/gauge policy stub
- `delta M` source-class policy stub
- `delta M` extraction-freeze stub
- `X_resp` state-kind menu stub
- `Adm_resp` admissibility policy stub
- `S_tau^resp` term-policy stub
- `Select_stab` policy stub
- `ChannelHandoff_tau` policy stub

## What Is Not Frozen

This is not a filled response model. It does not supply:

- concrete `B_tau^base` carrier elements;
- `delta M` source instance;
- `X_resp` construction;
- `Adm_resp` construction;
- `S_tau^resp` functional;
- `Select_stab` rule;
- `ChannelHandoff_tau` rule;
- channel map;
- readout map;
- endpoint score.

## Claim Boundary

Allowed status:

```text
FROZEN_POLICY_BUNDLE_REFERENCE_INSTANCE_V01
```

Forbidden promotions:

```text
Response_tau formula;
S_tau^resp functional;
physical Tau dark-sector field;
galaxy endpoint result;
standard dark matter rejection.
```
