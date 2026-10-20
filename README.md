# asset-orphan

Find asset files (images, fonts, media, PDFs) that are never referenced anywhere in your source code.

## Description

`asset-orphan` walks a project tree, collects asset files by extension, and checks whether each
one is referenced in any other (text) file. Assets that never appear are reported as orphans —
great for cleaning up dead images, stale icons, and unused fonts before shipping.

## Features

- Detects common asset extensions: images, fonts, media, PDFs.
- Skips noise directories (`.git`, `node_modules`, build output, caches).
- Case-insensitive reference matching on basename and relative path.
- Text and JSON output formats.
- Optional non-zero exit code for CI gates.
- Zero runtime dependencies (stdlib only).

## Install

```sh
git clone https://github.com/example/asset-orphan
cd asset-orphan
python -m asset_orphan .
```

## Usage

```sh
# scan current directory
asset-orphan .

# JSON output
asset-orphan . --format json

# CI gate
asset-orphan . --exit-code
```

Example output:

```
Scanned: /path/to/project
Assets: 12, used: 9, orphans: 3

Orphan assets:
  assets/old-logo.png
  fonts/unused.woff2
  img/scratch.jpg
```

## License

MIT
