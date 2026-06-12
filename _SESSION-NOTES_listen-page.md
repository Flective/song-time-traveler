# _SESSION-NOTES_ — Fiat Musica Listen Page (song-time-traveler)

**Updated:** 2026-06-11
**Project folder:** `~/Dropbox/__FLECTIVE/__ my coding projects/song-time-traveler/`
**Deploy clone:** `~/Documents/GitHub/song-time-traveler/` → GitHub `Flective/song-time-traveler` → Vercel → `listen.fiatmusica.com`

---

## DEPLOY (one command, copies + commits + pushes)
```
cp "/Users/jamesyett/Dropbox/__FLECTIVE/__ my coding projects/song-time-traveler/index.html" ~/Documents/GitHub/song-time-traveler/index.html && cd ~/Documents/GitHub/song-time-traveler && git add -A && git commit -m "msg" && git push
```
For multiple files, use rsync of the whole folder (exclude node_modules/.git/.DS_Store).
Then hard-refresh or use an incognito window to bypass cache. Vercel deploy must show "Ready" for the latest commit.

---

## DONE (compact view + IA pass)
- Feedback questionnaire page BUILT: feedback.html, the recovered 5-question form (stay/skip, hook 1-10, sounds-like, lyric strength, would-listen-full) + optional comment + thank-you state. Front-end only; data-capture hook is marked in the JS (`DATA CAPTURE GOES HERE`) for a Formspree/Google Forms/Worker POST later. Linked in nav on all pages.
- Hero copy reframed: the single is now described as ONE of the triangulations (the one marked as the way in / radio cut), not a separate thing. Also fixed "renderings" -> "renditions" there.
- Nav now 5 items (The Songs | The Idea . Essay . Feedback . About) across all pages. WATCH: may crowd on narrow screens — consider a mobile menu later.
- Compact List view added (Cards/List toggle): each row = play button · thumbnail · title · one button per version (every triangulation; single songs show one). Row play button plays the single; version buttons play that version. No "1+N" count.
- Toggle button given a real fill (was a naked outline).
- Catalog summary near toggle: "N songs · M renditions".
- Tiny-text floor raised on the credit sub-label.
- "The Idea" moved to its OWN page (walk-around.html); removed from songs page; nav unified across all 4 pages: The Songs | The Idea ↗ · Essay ↗ · About ↗.
- Questionnaire concept RECOVERED from past chats: 5-question song-feedback form (keep/skip on first 5s; rate hook 1-10; what does it sound like; lyric strength; would you listen to full) + optional comment. Strategic framing: songs are the selection mechanism; questionnaire doubles as fundraising market research. NOT yet built as a page.

## DONE THIS SESSION
- next/prev + auto-advance now walk a FLAT sequence of every arrangement across all songs (not song-to-song).
- Lyrics switched to sans-serif (DM Sans), tighter line-height (1.4).
- Album feature fully REMOVED from listen page (the real playable album belongs on play.fiatmusica). The "add to album" button led nowhere, so it was pulled along with its bar/modal/JS.
- Triangulation essay written: `essay.html` ("The Song Behind the Song"), literary rock-criticism voice, Mad World / Hendrix / Neil Young throughline, byline James Pauli. Linked in nav.
- Nav restructured into two groups: in-page anchors (The Songs · The Idea) | separate pages (Essay ↗ · About ↗) with outward-arrow markers. Applied across index, about, essay.
- "When I Stumble" added (4 versions: casual/mellow/duet/pastiche; single = casual).
- Card redesign: title top-left, image directly below; expanding lyrics also grows the thumbnail into the full image under the title; lyrics box has distinct background; single + triangulated cards share one background, single card shorter; expand/collapse toggle moved onto the LYRICS header line (top-right); minimum font sizes raised; no default-"selected" look on load (single marked only with a quiet dot until played); credit line = "Words & music: James Pauli".

---

## OPEN / TO BUILD (held deliberately — pick up next sessions)

### High value, concrete
1. **Compact catalog view** — one attractive row per song (tiny thumbnail + title + version count + maybe play count), 15–20 per page, scrollable. A way to assess the whole catalog at a glance. RECOMMENDED NEXT BUILD.

### Design / feature passes
2. **High-design play button** — replace the standard play control with a custom, bigger, graphically meaningful button. Intended direction: reactive to the music; later, refractive-glass effects, lyrics going by. Beautiful, inviting, central — NOT clownish-big.
3. **Full-screen video mode** — video thumbnail/placeholder in the card; on open, opens FULL SCREEN in the most beautiful mode possible, easy navigation, quality imagery (not a corner embed).

### Information architecture
4. **"Walk around the song" graphic → its own page** — remove the Idea figure from the songs page; make it a standalone page on the site.
5. **FAQ page + testimonials** — include testimonials; Jim to seek buy-in/testimonials (e.g. someone at Berklee School of Music) for the triangulation concept.

### Ecosystem / data model (bigger thinking)
6. **Play counts visible to listeners** — display number of plays so popularity becomes a public signal.
7. **Favoriting / voting** — listeners favorite songs.
8. **Hit-as-triangulation model** — treat the radio/hit cut as just another triangulation. A song could have e.g. 5 triangulations with one OR two marked as "hit"/radio (the bulleted ones). Popularity data could promote/demote: unpopular versions might be retired; very popular ones get the bullet. Evolves into a song-optimization + exploration ecosystem.

### Carry-over from earlier (not yet done)
9. **Vocabulary scrub** — hero still says "renderings" and "change your angle"; locked rule: "rendering" BANNED as the AI term → use rendition/arrangement/performance; "triangulation" = the concept. Scrub the page copy to match. (Blurbs were written with "rendering" in a few places too — sweep those.)

---

## BLURB ACCURACY TODO
The triangulation blurbs (rollover descriptions) for "When I Stumble" and others were written from the version NAMES, not the actual recordings. Jim to confirm/correct so descriptions match what each cut actually sounds like.

## DATA MODEL REFERENCE
`const SONGS = [...]` near the bottom of index.html. Each: `{ id, title, single:'<key>', lyrics:`...`, video:'', triangulations:[ {key,label,file,color,blurb}, ... ] }`. Single-version songs render the compact (shorter) card; multi render the full card. Audio in `songs/` (local mp3s, relative paths).
