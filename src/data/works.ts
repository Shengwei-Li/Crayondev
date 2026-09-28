import { getCollection } from "astro:content";

// All published works, oldest first, so a work's position is its catalogue number.
export async function getWorks() {
  const works = await getCollection("works", ({ data }) => !data.draft);
  return works.sort((a, b) => a.data.date.getTime() - b.data.date.getTime());
}
