import argparse
import pandas as pd
import yaml
import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_PATH = 'config.yaml'
DATA_DIR = 'data'
HISTORY_DIR = 'history'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_history(df, sku=None):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'history_{timestamp}.csv'
    if sku:
        filename = f'history_{sku}_{timestamp}.csv'
    df.to_csv(os.path.join(HISTORY_DIR, filename), index=False)
    print(f"✅ History saved: {filename}")

def validate_data(df, config):
    errors = []
    rules = config.get('validation_rules', {})
    for col, rule in rules.items():
        if col in df.columns:
            if rule == 'numeric':
                if not pd.to_numeric(df[col], errors='coerce').notna().all():
                    errors.append(f"Non-numeric in {col}")
            if rule == 'integer':
                if not pd.to_numeric(df[col], errors='coerce').dropna().mod(1).eq(0).all():
                    errors.append(f"Non-integer in {col}")
    if errors:
        print("Validation errors:", errors)
        return False
    print("✅ Validation passed.")
    return True

def export_for_indesign(csv_path=None):
    config = load_config()
    if not csv_path:
        csv_path = os.path.join(DATA_DIR, 'master_products.csv')
    df = pd.read_csv(csv_path)
    if validate_data(df, config):
        mappings = config.get('field_mappings', {})
        for old, new in mappings.items():
            if old in df.columns:
                df = df.rename(columns={old: new})
        export_cols = config.get('export_columns', df.columns.tolist())
        export_df = df[export_cols]
        out_path = os.path.join(DATA_DIR, 'indesign_merge.csv')
        export_df.to_csv(out_path, index=False)
        print(f"✅ Exported: {out_path}")
        save_history(df)

def update_csv(csv_path):
    df = pd.read_csv(csv_path)
    config = load_config()
    if validate_data(df, config):
        master = os.path.join(DATA_DIR, 'master_products.csv')
        df.to_csv(master, index=False)
        print("✅ Master updated.")
        save_history(df)
        export_for_indesign()

def show_history(sku=None):
    files = sorted([f for f in os.listdir(HISTORY_DIR) if f.endswith('.csv')], reverse=True)
    if sku:
        files = [f for f in files if sku in f]
    for f in files[:5]:
        print(f"📄 {f}")
        print(pd.read_csv(os.path.join(HISTORY_DIR, f)).head(3))
        print("---")

class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            print(f"🔄 CSV changed: {event.src_path}")

def monitor_csv():
    observer = Observer()
    observer.schedule(CSVHandler(), DATA_DIR, recursive=False)
    observer.start()
    print("👀 Monitoring active (Ctrl+C to stop)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser(description="InDesign Catalog Sync MCP")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('export')
    update_p = subparsers.add_parser('update')
    update_p.add_argument('--csv', required=True)
    subparsers.add_parser('history')
    subparsers.add_parser('monitor')

    args = parser.parse_args()

    if args.command == 'export':
        export_for_indesign()
    elif args.command == 'update':
        update_csv(args.csv)
    elif args.command == 'history':
        show_history()
    elif args.command == 'monitor':
        monitor_csv()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()