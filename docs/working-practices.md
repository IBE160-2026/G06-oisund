# Owner walkthrough before final verification

Adopted by Jonas on29October2026 under E12-A2. For relevant user-flow changes, arrange an early combined owner walkthrough before the final test gate. This is a standing practice, not a claim that future walkthroughs have already happened.

Show the complete affected path with actual visible controls, save/failure feedback, navigation and focus/scrolling behavior. Ask for one concrete set of feedback covering unnecessary steps, readability and touch comfort. Record the tested source/build/device, which actions were automated or human, actual feedback and decisions. Continue independent work while feedback is pending. Design direction, passed tests and explicit product acceptance are separate facts.

Reuse accepted observations when the affected behavior and tested inputs are unchanged. If feedback changes the product, run the relevant final checks against the resulting version; never relabel earlier failures or old physical evidence as fresh passes. Do not mark product acceptance given until Jonas explicitly grants it.

For the D1–D3 follow-up, Jonas approved the proposed abandonment/rejection/UTC-offset direction as an implementation starting point. That early design direction does not accept the implemented candidate or the A7 subjective checks. The final candidate report groups remaining owner checks; historical accepted V1 and c067fdb remain unchanged.
