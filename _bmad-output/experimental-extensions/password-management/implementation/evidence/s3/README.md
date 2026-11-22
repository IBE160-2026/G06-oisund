# S3 blank-form evidence

Captured by `frontend/tests/password-recovery.spec.ts`, test `blank recovery form tablet PC themes and enlarged text`, with actual ThemeControl button, Edge headless, isolated preview UI15440/API18441, 200% root font size, viewports800×1100 and1280×1100. Every field is blank. Trace/video and automatic failure screenshots are disabled. These are browser simulations, not physical-device/owner acceptance.

Four PNGs preserve Day/Night tablet/PC renders. The four JSON files record computed contrast: main text, input text, input border, button text and focused input outline against their actual computed backgrounds. Assertions require text≥4.5, border/focus≥3 and3px focus outline; minimum58px controls and no horizontal overflow also pass. Source fingerprints are in `source-sha256.json`; baseline and run history are in [S3 evidence](../../s3-evidence.md). Final synthetic preview JS bundle: `main-DnQxIuR2.js`.

The regenerated night screenshot correctly reads «Visning: Natt». Prior test-only mismatched-label renders in tmp were replaced and are not part of this tracked evidence. No screenshot contains a username, password, recovery code or private work.
