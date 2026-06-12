# Listen page — SESSION HANDOFF (for next chat)

**Date:** 2026-06-11. Page is LIVE at listen.fiatmusica.com.
**Project:** song-time-traveler. Edit `index.html` in Dropbox
(`~/Dropbox/__FLECTIVE/__ my coding projects/song-time-traveler/`), copy to clone
(`~/Documents/GitHub/song-time-traveler/`), then: `git add -A && git commit -m "..." && git push`.

## JUST FIXED (may or may not be deployed yet — confirm)
- Add-to-album button (was crashing on missing album-count element)
- Spacebar pause/play reliability (blur focus after clicks)
- Player scrub thumb now always visible
- Reduced excessive hero top whitespace

## STILL OPEN — DO NEXT
1. **Player next/prev should step through EVERY arrangement**, not skip song-to-song.
   Currently next/prev jump between songs (each at its single). Jim wants them to walk
   through all triangulations: deep -> ethereal -> percussive -> ... -> next song's
   arrangements. This is the #1 unfixed bug.
2. **Vocabulary scrub of the live page** to locked terms (see
   `_FEEDBACK-DRAFT_fiatmusica-listen.md` vocabulary section):
   - "rendering/renderings" -> BANNED (AI term). Use rendition / arrangement / performance.
   - Page still says "renderings," "change your angle," etc. — scrub all of it.
   - Keep "triangulation" as the concept; arrangements/renditions = the instances.
3. **Build the feedback experience** — full copy drafted in
   `_FEEDBACK-DRAFT_fiatmusica-listen.md`. One-question-at-a-time flow, Formspree delivery,
   spine question = "Would you assume a professional wrote this?"
4. **Write the rock-history essay** — brief in `_ESSAY-QUEUED_triangulation-rock-history.md`
   (Mad World / Hendrix / Neil Young; Platonic song; literary rock-crit voice).

## DEFERRED POLISH (in `_POLISH-TODO_listen-page.md`)
- Play button position differs between triangulated (top-right) and single (inline-left) cards.
- Cover image maybe too small vs lyrics.
- What should clicking the cover image do? (undecided)
- Per-song vs per-rendition thumbnail (undecided)

## BIGGER, FILED (in `_NEXT-STEPS_listen-fiatmusica-layer2.md`)
- Album types schema (Official / Preset / Sessions / Eclectic), needs rendition genre TAGS +
  album-entity metadata. Streamlit app (`fiatmusica_app/fiat_musica_v8_1.py`) is the blueprint.
- Login / accounts / play-stats — defer until simple version proves engagement.
- Waveform scrub bar (SoundCloud-style) — deferred, build with Layer 2.

## VOCAB/PHILOSOPHY canonical reference
Lives in `_FEEDBACK-DRAFT_fiatmusica-listen.md` top section. Single source of truth for
rendition-vs-rendering, triangulation, Platonic song, entrée, AI-as-access-not-legitimacy.
