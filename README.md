# InDesign Catalog Sync MCP

Master Control Panel for automating CSV ↔ Adobe InDesign catalog synchronization.

## Features
- Real-time CSV monitoring
- Data validation & versioning
- Pricing history audit
- Clean export for InDesign Data Merge
- Configurable field mappings

## Quick Start
1. `pip install -r requirements.txt`
2. Place your `master_products.csv` in `data/`
3. `python cli.py export`

Full demo in the presentation.

## Sample Data & Mapping
See `data/master_products.csv` and `config.yaml` for examples.

## Demo Commands
- `python cli.py update --csv data/master_products.csv`
- `python cli.py export`
- `python cli.py history --sku PROD001`

# InDesign Catalog Sync MCP - Mobile Ready

Master Control Panel for CSV ↔ Adobe InDesign.

## Mobile APK
- Install via Termux + Buildozer (see below)
- Tap buttons to Export/Update/History

## Build APK
```bash
buildozer android debug