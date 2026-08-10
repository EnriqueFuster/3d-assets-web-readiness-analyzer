import { writeFile } from "node:fs/promises";
import { basename } from "node:path";
import process from "node:process";

import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { inspect } from "@gltf-transform/functions";
import { MeshoptDecoder } from "meshoptimizer";

const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error("Usage: npm run inspect:json -- <input.glb> <report.json>");
  process.exit(2);
}

try {
  const io = new NodeIO()
  .registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({
    "meshopt.decoder": MeshoptDecoder
  });
  const document = await io.read(inputPath);
  const root = document.getRoot();
  const report = {
    source: basename(inputPath),
    extensionsUsed: root.listExtensionsUsed().map((extension) => extension.extensionName),
    extensionsRequired: root.listExtensionsRequired().map((extension) => extension.extensionName),
    ...inspect(document)
  };

  await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  console.log(`glTF Transform inspection wrote ${outputPath}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
