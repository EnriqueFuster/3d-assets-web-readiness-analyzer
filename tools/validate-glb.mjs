import { readFile, writeFile } from "node:fs/promises";
import { basename } from "node:path";
import process from "node:process";
import { validateBytes, version } from "gltf-validator";

const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error("Usage: npm run validate -- <input.glb> <report.json>");
  process.exit(2);
}

try {
  const bytes = new Uint8Array(await readFile(inputPath));
  const report = await validateBytes(bytes, {
    uri: basename(inputPath),
    format: "glb",
    maxIssues: 1000,
    externalResourceFunction: async () => {
      throw new Error("External resources are not supported for self-contained GLB fixtures.");
    }
  });

  await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  console.log(`glTF Validator ${version()} wrote ${outputPath}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}

