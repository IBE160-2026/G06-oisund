---
id: SPEC-password-management
status: draft-planning-only
companions:
  - brownfield.md
  - implementation-plan.md
  - qualification.md
sources: []
---

# Password management

**Experimental extension. Recommendations remain unapproved.** This kernel and companions describe a proposed scope, not permission to build or publish.

## Why

Operator-created accounts currently have neither an own-password change nor a forgotten-password recovery flow. Users need both without losing their existing account, workdays or retained data. Extend the accepted V1 application and Ubuntu deployment with the least operational complexity justified by actual users.

## Capabilities

- **CAP-1**
  - **intent:** A signed-in user who knows the current password can change their own password.
  - **success:** Correct current credentials allow a new password; incorrect credentials change nothing; subsequent login accepts the new password and rejects the old one for that account.
- **CAP-2**
  - **intent:** A user who forgot their password can recover the existing account after appropriate identity verification.
  - **success:** A valid account-bound recovery proof permits one password replacement; expired, consumed, superseded or wrong-account proof does not. The operator never needs to know the new password.
- **CAP-3**
  - **intent:** A password replacement ends old application access while preserving the user's data and truthful recovery behavior.
  - **success:** Old sessions and derived day access fail after commit, including concurrent login and cross-tab requests; new login to the same account reopens still-retained data without altering ownership, deadlines or saved facts.

## Constraints

- Preserve UUIDs, usernames, password compatibility, owner relationships, retention deadlines and private/demo isolation. Do not recreate or bulk-reset existing users.
- No assumed registered or verified email. Outer Access identity is not application account identity.
- Current-password verification for CAP-1; bounded attempts, one-use expiring proof for CAP-2, CSRF/Origin protection and no secret logging for both.
- No password mutation or queued credential replay offline. Server remains authoritative.
- Planning branch and extension outputs remain independent of automatic notices. No implementation, production change, merge, tag, release or version allocation in this task.

## Non-goals

- General profile system, web administration console, public signup, MFA/SSO redesign, security questions, temporary passwords or offline credential storage.
- Email enrollment/delivery in the proposed minimum; optional later scope requires a separate decision.

## Success signal

In an isolated synthetic environment, two existing users complete the two distinct flows and retain their data; rejected recovery attempts and revoked sessions cannot access either user's private records. The qualification matrix passes, followed by explicit owner acceptance.

## Assumptions

- A small operator-provisioned population can accept assisted recovery. User count, operator coverage and identity-verification channel are not established.
- Proposed 30-minute recovery validity and all-session logout are recommendations, not accepted policy.

## Open Questions

Q1–Q4 in implementation-plan.md govern support/identity checks, recovery channel, logout policy and delivery grouping. Resolve dependent decisions before implementation; no version number is requested.
