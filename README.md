# NEC Civil MCQ Trainer

A free, mobile-friendly, open-source practice app for Nepal Engineering Council (NEC) Civil Engineering Licence Exam preparation.

**[Open the MCQ Trainer](https://liambasnet2500-creator.github.io/nec-civil-mcq-trainer/)**

> **Independent educational project.** Not affiliated with or endorsed by the Nepal Engineering Council. Verify code references, exam patterns, and answer keys against current official sources.

## Features

- 646 civil engineering multiple-choice questions arranged by chapters and sub-chapters
- Practice and mock-exam modes, concept explanations, and progress tracking
- Mobile-friendly interface and full-screen control (subject to browser support)
- Mathematics rendering with bundled KaTeX resources
- Question bank and most app assets embedded in a single HTML file, suitable for offline use
- Progress saved locally in the browser; special Claude-host integration is optional and not available on GitHub Pages

## Start

Visit the **[hosted trainer](https://liambasnet2500-creator.github.io/nec-civil-mcq-trainer/)**, or download `index.html` and open it in a modern browser.

This is the existing trainer imported from the private development workspace, **not a newly generated quiz**. The original project was prepared for an earlier examination; students should check that the questions, codes, and regulations remain current.

## Repository layout

- `index.html` — the original standalone trainer adapted with basic HTML metadata for web hosting
- `question-bank.json` — the trainer's 646-question dataset, also embedded in `index.html`
- `tools/` — retained app template and source/extraction/build scripts from the original project
- `.github/workflows/deploy-pages.yml` — GitHub Pages static-site deployment

The archived build scripts refer to intermediate files and a source PDF that are **not** included here. Consequently, this repository publishes the original runnable application and the available scripts, but the entire question-extraction pipeline is not reproducible from this repository alone.

## Privacy

The public website does not require a sign-in. On GitHub Pages, practice progress is stored in your browser's local storage. Clearing browser data can erase this progress. Optional integration originally designed for Claude's hosted environment remains inactive on a normal website.

## Licensing and attribution

- **Original application and tooling code:** MIT License; see [LICENSE](LICENSE).
- **Question-bank text, answers, and explanations:** included with the maintainer's confirmed redistribution rights. These educational materials are **not automatically offered under the MIT code license**. Contact the maintainer before republishing or adapting them separately.
- **KaTeX:** third-party library embedded in the app; MIT licensed by its contributors (see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)). Some web fonts are fetched from Google Fonts when connected; the app has system font fallbacks.

## Contributions

Issues, accessibility fixes, bug reports and code improvements are welcome. Do not submit copyrighted question-book material unless you have the necessary permissions. Use GitHub Issues and Pull Requests on this repository.
