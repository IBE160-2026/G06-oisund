# Lifecycle/device — acquisition digest

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

All accessed 2026-10-26. Statements below concern documentation, not observed device behavior.

- Chrome, https://developer.chrome.com/docs/web-platform/page-lifecycle-api, updated 2026-10-16: pages can freeze/discard; mobile termination events are unreliable. Class lifecycle; medium single-publisher. Supports conservative foreground policy together with W3C; not a fixed screen-lock latency.
- Android, https://developer.android.com/training/monitoring-device-state/doze-standby, updated 2026-10-22: Doze restricts network/tasks; stationary unplugged screen-off conditions matter. Class OS lifecycle; medium. Native-app guidance cannot establish a browser's exact callback behavior.
- Android Help, https://support.google.com/android/answer/6179507?hl=en, publication unknown: app permissions and approximate/precise location choices affect access. Class device compatibility; medium/unverified for Lenovo. Hardware/source adequacy and UI vary.
- Brave Help, https://support.brave.app/hc/en-us/articles/360018205431-How-do-I-change-site-permissions, updated 2024-11-11: default location prompt documented, but instructions are computer-specific. Class compatibility; medium for documented setting, unverified for current Android parity. Search did not establish Lenovo/Brave behavior; old community reports were not treated as qualification evidence.
- Chrome, https://developer.chrome.com/blog/geolocation-on-secure-contexts-only, historical Chrome 50 guidance, page publication not extracted: secure origin required, localhost exception described. Class secure-context contract; corroborates W3C. Does not approve an insecure LAN origin or certify current tablet setup.

Coverage ends this bounded round. Remaining questions require model/SKU and physical Chrome/Brave checks, not another broad web sweep. No clocked delivery, battery-runtime or accuracy guarantee found.
