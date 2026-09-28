import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const link = z.object({ label: z.string(), href: z.string() });

// One folder per work in src/content/works/<slug>/ with an index.md or index.mdx and its images.
// Nothing here is Minecraft-specific: a mod, a game, a tool or anything else fits the same fields.
const works = defineCollection({
  loader: glob({ pattern: "*/index.{md,mdx}", base: "./src/content/works", generateId: ({ entry }) => entry.split("/")[0] }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      tagline: z.string(),
      // Free text shown in the catalogue, e.g. "Minecraft mod", "Game", "Tool".
      kind: z.string(),
      // Short facts shown under the title, e.g. ["NeoForge 1.21.1", "Needs GeckoLib 4.9+"].
      facts: z.array(z.string()).default([]),
      status: z.enum(["released", "in development", "idea"]),
      date: z.coerce.date(),
      // Lead image. `coverNight` is shown instead when the visitor's system is in dark mode.
      cover: image(),
      coverNight: image().optional(),
      // Short muted loop (path under public/). Replaces the cover once it exists.
      video: z.string().optional(),
      // Small pixel-art icon for the catalogue.
      icon: image().optional(),
      download: link.optional(),
      links: z.array(link).default([]),
      draft: z.boolean().default(false),
    }),
});

const log = defineCollection({
  loader: glob({ pattern: "*.{md,mdx}", base: "./src/content/log" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      summary: z.string(),
      // Slug of the work this entry is about, if any.
      work: z.string().optional(),
      cover: image().optional(),
      draft: z.boolean().default(false),
    }),
});

export const collections = { works, log };
