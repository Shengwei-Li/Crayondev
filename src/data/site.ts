import { siBuymeacoffee, siCurseforge, siDiscord, siKofi, siModrinth, siReddit, siX, siYoutube } from "simple-icons";

// Site-wide identity and links. Only CrayonDev26 appears here, never a real name.
export const site = {
  name: "CrayonDev26",
  description: "Mods, games and other things by CrayonDev26.",
};

// Profiles, in display order. `href: null` shows the icon greyed out as a placeholder;
// fill in the URL when the account exists. `support` marks donation links.
export const socials = [
  { name: "Modrinth", icon: siModrinth, href: "https://modrinth.com/user/CrayonDev26" },
  { name: "CurseForge", icon: siCurseforge, href: "https://www.curseforge.com/members/crayondev26/projects" },
  { name: "Discord", icon: siDiscord, href: null },
  { name: "Reddit", icon: siReddit, href: null },
  { name: "X", icon: siX, href: null },
  { name: "YouTube", icon: siYoutube, href: null },
  { name: "Ko-fi", icon: siKofi, href: "https://ko-fi.com/R5R41BQQGZ", support: true },
  { name: "Buy Me a Coffee", icon: siBuymeacoffee, href: null, support: true },
] as { name: string; icon: { path: string }; href: string | null; support?: boolean }[];

// Catalogue number for a work: its position by date, oldest first.
export const catalogueNumber = (index: number) => String(index + 1).padStart(3, "0");
