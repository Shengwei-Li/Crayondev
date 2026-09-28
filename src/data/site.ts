// Site-wide identity and links. Only CrayonDev26 appears here, never a real name.
export const site = {
  name: "CrayonDev26",
  description: "Minecraft mods and other things by CrayonDev26.",
  // TODO: check both profile URLs once the pages are live.
  links: [
    { label: "Modrinth", href: "https://modrinth.com/user/CrayonDev26" },
    { label: "CurseForge", href: "https://www.curseforge.com/members/crayondev26" },
  ],
};

// Catalogue number for a work: its position by date, oldest first.
export const catalogueNumber = (index: number) => String(index + 1).padStart(3, "0");
