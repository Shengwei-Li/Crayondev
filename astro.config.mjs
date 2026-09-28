import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  site: "https://crayondev26.org",
  trailingSlash: "never",
  build: { format: "file" },
  integrations: [mdx()],
});
