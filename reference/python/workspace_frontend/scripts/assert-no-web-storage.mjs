import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const forbidden = ["localStorage", "sessionStorage"];
const root = fileURLToPath(new URL("../src/", import.meta.url));
const failures = [];

function walk(path) {
  for (const entry of readdirSync(path)) {
    const full = join(path, entry);
    if (statSync(full).isDirectory()) {
      walk(full);
      continue;
    }
    if (!/\.(ts|tsx|js|jsx)$/.test(entry)) continue;
    const source = readFileSync(full, "utf8");
    for (const token of forbidden) {
      if (source.includes(token)) failures.push(`${full}: forbidden browser storage token ${token}`);
    }
  }
}
walk(root);
if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log("P9.03 web-storage guard PASS");
