# SmartDeutschLehrer

German grammar drill app (PWA) that complements Duolingo: noun gender, plurals, adjective endings, cases.
No streaks, no XP — short lessons whenever you feel like it.

- Plain HTML/CSS/JS, no build step. Served by GitHub Pages.
- All personal data (lessons, results, progress) lives in a separate **private** repository; the app talks to it
  through the GitHub API with a fine-grained token stored only on the device.
- Lessons are generated between sessions by a local task on the owner's PC and validated against a
  Wiktionary-derived noun dictionary before they are committed.

Bump `CACHE` in `sw.js` and `APP_VERSION` in `index.html` on every release.
Icons: `python -I tools/make_icons.py`.
