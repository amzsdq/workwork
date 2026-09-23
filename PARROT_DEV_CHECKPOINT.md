# Parrot durable development checkpoint

Generation: 1
Owner session: `PARROT-20260923T1740Z-G1`
Latest artifact: `parrot_extension_v0.7.1.zip`
Status: CONTINUE
Server-observed work duration: `43 seconds` (`2026-09-23T17:40:25Z` → `2026-09-23T17:41:08Z`)

## Completed change

Hardened composer ownership for normal Parrot repeat sends:

- Parrot now refuses a normal automatic send when the ChatGPT composer already contains text (`draft_present`).
- This prevents an automatic repeat from overwriting a user's manual draft.
- If Parrot itself injects its payload but fails before clicking Send, it removes only its own exact unchanged payload.
- If the user changed the composer after injection, cleanup does not erase the user's modified text.

## Verification

- `node --check`: content.js, background.js, dashboard.js, popup.js passed.
- manifest JSON parse passed.
- ZIP integrity (`unzip -t`) passed.
- Manifest version bumped 0.7.0 -> 0.7.1.

## Remaining risks

- Normal repeat-send accounting still marks `PARROT_SENT` immediately after click rather than waiting for a stronger DOM receipt. Generation grace detects some failures, but sentCount/onboarding accounting can still be optimistic if a click is swallowed.
- Route delivery receipt currently treats composer clear/change or generation start as dispatch confirmation; this should be regression-tested against current ChatGPT DOM.
- Content-script reload can defer pending route redelivery until background redispatch.

## Next concrete task

Add a conservative normal-send dispatch receipt before incrementing sentCount, without creating duplicate-send risk. Prefer evidence from generation start/user-message DOM over a generic composer mutation.