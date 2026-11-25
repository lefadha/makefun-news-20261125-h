// Ship the page this repository commits to /output/entry.png, and prove the bytes that land
// are the bytes in the commit. Node 22, standard library only; the sandbox has no network.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The image is one 1024x1024 PNG, drawn by render.py from stories.py (35 dated wire items,
// 8 regions, 00:00-13:20 UTC on 25 November 2026). This program does not draw it: it holds
// the committed file to the competition's gate and copies it, so a run is a byte copy.

import { copyFileSync, mkdirSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import { join } from "node:path";
import { crc32 } from "node:zlib";

const SOURCE = "entry.png";
const MAX_BYTES = 1048576;
const SIDE = 1024;

function fail(why: string): never {
  console.error("entry refused: " + why);
  process.exit(1);
}

/** The gate reads the first bytes, the IHDR and every chunk's checksum: do the same. */
function inspect(path: string): number {
  const bytes = readFileSync(path);
  if (bytes.length > MAX_BYTES) fail(`image is ${bytes.length} bytes, over the 1 MiB cap`);
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  for (let i = 0; i < signature.length; i++) {
    if (bytes[i] !== signature[i]) fail("first bytes are not a PNG signature");
  }
  const chunkType = bytes.subarray(12, 16).toString("ascii");
  if (chunkType !== "IHDR") fail(`first chunk is ${chunkType}, not IHDR`);
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== SIDE || height !== SIDE) fail(`image is ${width}x${height}, not ${SIDE}x${SIDE}`);
  const depth = bytes[24];
  const colourType = bytes[25];
  if (depth !== 8 || (colourType !== 2 && colourType !== 6)) {
    fail(`pixels are depth ${depth} type ${colourType}, not 8-bit truecolour`);
  }
  // walk to IEND, checking each chunk's checksum as the gate does, so a damaged or
  // truncated file is refused here rather than after a submission is spent
  let at = 8;
  let ended = false;
  while (at + 12 <= bytes.length) {
    const length = bytes.readUInt32BE(at);
    const type = bytes.subarray(at + 4, at + 8).toString("ascii");
    const held = bytes.readUInt32BE(at + 8 + length);
    const computed = crc32(bytes.subarray(at + 4, at + 8 + length));
    if (held !== computed) fail(`chunk ${type} fails its checksum`);
    at += 12 + length;
    if (type === "IEND") {
      ended = true;
      break;
    }
  }
  if (!ended) fail("the PNG ends before its IEND chunk");
  if (at > bytes.length) fail("a chunk runs past the end of the file");
  return bytes.length;
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const destination = join(outDir, "entry.png");
const size = inspect(SOURCE);
mkdirSync(outDir, { recursive: true });
copyFileSync(SOURCE, destination);

// read the copy back in blocks: the judge sees exactly these bytes, so prove they landed
const expected = statSync(SOURCE).size;
if (statSync(destination).size !== expected) fail("the copy on disk is a different size");
const fd = openSync(destination, "r");
const block = Buffer.alloc(4096);
let read = 0;
let offset = 0;
while (offset < expected) {
  read = readSync(fd, block, 0, block.length, offset);
  if (read <= 0) break;
  offset += read;
}
if (offset !== expected) fail(`read back ${offset} of ${expected} bytes`);
const tail = readFileSync(destination).subarray(expected - 8, expected - 4).toString("ascii");
if (tail !== "IEND") fail(`last chunk is ${tail}, not IEND`);

console.log(`wrote ${destination}: ${size} bytes, ${SIDE}x${SIDE}, read back whole`);
