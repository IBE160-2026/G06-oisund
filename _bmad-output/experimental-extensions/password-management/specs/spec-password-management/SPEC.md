---
id: SPEC-password-management
status: draft-planning-only
companions:
  - brownfield.md
  - implementation-plan.md
  - qualification.md
  - ../../planning/epics.md
  - ../../planning/technical-contract.md
  - ../../planning/coverage.md
sources: []
---

# Password management

**Experimental extension. Owner scope decisions recorded on 2026-10-31; technical choices are proposed in the implementation-ready story package.** This kernel and companions are planning artifacts, not permission to build or publish.

## Why

Operator-created accounts currently have neither an own-password change nor a forgotten-password recovery flow. Users need both without losing their existing account, workdays or retained data. Extend the accepted V1 application and Ubuntu deployment with the least operational complexity justified by actual users.

## Capabilities

- **CAP-1**
  - **intent:** A signed-in user who knows the current password can change their own password.
  - **success:** Correct current credentials allow a new password; incorrect credentials change nothing; subsequent login accepts the new password and rejects the old one for that account.
- **CAP-2**
  - **intent:** A user who forgot their password can recover the existing account after appropriate identity verification, including Jonas using independent SSH access to issue a code for his own app account without app login.
  - **success:** A valid account-bound recovery proof permits one password replacement; expired, consumed, superseded or wrong-account proof does not. The operator never needs to know the new password.
- **CAP-3**
  - **intent:** A password replacement ends old application access while preserving the user's data and truthful recovery behavior.
  - **success:** Old sessions and derived day access fail after commit, including concurrent login and cross-tab requests; new login to the same account reopens still-retained data without altering ownership, deadlines or saved facts.

## Constraints

- Initial users: Jonas and the course teacher; Jonas administers account recovery. Use administrative one-use codes and a separate delivery. Both password flows revoke all application sessions and require login on every device.
- Preserve UUIDs, usernames, password compatibility, owner relationships, retention deadlines and private/demo isolation. Do not recreate or bulk-reset existing users.
- No assumed registered or verified email. Outer Access identity is not application account identity.
- Current-password verification for CAP-1; bounded attempts, one-use expiring proof for CAP-2, CSRF/Origin protection and no secret logging for both.
- No password mutation or queued credential replay offline. Server remains authoritative.
- Planning branch and extension outputs remain independent of automatic notices. No implementation, production change, merge, tag, release or version allocation in this task.

## Non-goals

- General profile system, web administration console, public signup, MFA/SSO redesign, security questions, temporary passwords or offline credential storage.
- Email enrollment/delivery and public availability in the initial scope; either requires a separate future decision.

## Success signal

In an isolated synthetic environment, two existing users complete the two distinct flows and retain their data; rejected recovery attempts and revoked sessions cannot access either user's private records. The qualification matrix passes, followed by explicit owner acceptance.

## Assumptions

- Proposed 30-minute recovery validity and detailed attempt/audit limits remain technical recommendations.
- No response-time or round-the-clock support commitment is inferred from Jonas taking responsibility.

## Open Questions

Q2–Q4 and Q1 population/operator are resolved in implementation-plan.md. Own-account SSH recovery without app login is explicitly decided. No unresolved product choice blocks story implementation. Before operational use, verify the documented identity-check/contact and capture-free terminal procedure and operator absence instructions. Implementation still needs a separate explicit instruction; no version number is allocated.
