# crayondev26.org

Astro, static output, deployed as a Cloudflare Worker with static assets.

```bash
pnpm install
pnpm dev        # http://localhost:4321
pnpm build      # -> dist/
pnpm deploy     # build + wrangler deploy
```

## Adding things

- **A work** (mod, game, tool, anything): make a folder `src/content/works/<slug>/` with an `index.mdx`
  and its images. Fields are in `src/content.config.ts`. `kind` is free text ("Minecraft mod", "Game",
  "Tool"...), `facts` is a list of short strings. Catalogue numbers are assigned by `date`, oldest first.
  The newest work is featured on the home page.
- **Day and night**: `cover` is shown in light mode, `coverNight` (optional) in dark mode.
- **Loop video**: put a short muted .mp4 in `public/` and set `video: /name.mp4`. It replaces the cover.
- **Item tooltips**: in an `.mdx` file, `import Tooltip from "../../../components/Tooltip.astro"` and use
  `<Tooltip name="..." icon={...} lines={[...]} />`. Tones: gray, green, blue, gold, aqua, purple, white.
- **A log entry**: add `src/content/log/<slug>.md`. See `example.md` (a draft). The Log link appears in the
  navigation once one entry is published.
- **Site name and profile links**: `src/data/site.ts`.
