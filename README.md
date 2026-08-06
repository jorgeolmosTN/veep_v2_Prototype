# AnytimePay Q2 Prototype (AltaOne concept)

Clickthrough prototype for the AnytimePay early-wage-access concept, plus reference
walkthrough videos/frames from the design team.

## Contents

- `site/` — everything that gets published. This is a self-contained, static
  clickthrough (no backend, no build step).
  - `index.html` — the prototype. Open this in a browser.
  - `anytimepay-q2-prototype.html` — the raw prototype fragment (used to render
    scenes for screenshots/videos).
  - `frames/`, `videos/` — walkthrough screenshots and GIFs.
  - `anytimepay-q2-video-package.zip` — packaged video walkthroughs.
- `tools/` — authoring scripts used to (re)generate the frames/videos
  (`capture-prototype.js` via headless Chrome, `build-walkthroughs.py` via Pillow).
  Not needed to view the prototype; kept for reference only.

## Publishing (Cloudflare Pages + Cloudflare Access)

This repo is meant to be deployed as a Cloudflare Pages site, restricted to the
team via Cloudflare Zero Trust Access (no public URL).

1. **Cloudflare Pages**: create a project connected to this GitHub repo.
   - Build command: none (leave empty)
   - Build output directory: `site`
   - Branch to deploy: this branch (or `main` once merged)
2. **Cloudflare Access**: in Zero Trust → Access → Applications, add a
   Self-hosted application pointing at the Pages URL/domain, with a policy that
   allows only the `@truenorth.co` email domain (or specific teammate emails).
3. Share the Pages URL with the team — Access will prompt for an email OTP
   login before letting anyone view it.
