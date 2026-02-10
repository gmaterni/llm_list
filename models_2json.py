#!/usr/bin/env python3

import os
import sys
import json
import re

def parse_window_size(size_str):
    """Extracts the numeric part from a string like '128k'."""
    match = re.search(r'(\d+)', size_str)
    if match:
        return int(match.group(1))
    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python models_2json.py <directory>")
        sys.exit(1)

    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: {data_dir} is not a directory")
        sys.exit(1)

    provider_config = {}

    for filename in os.listdir(data_dir):
        if filename.endswith("_wnd.txt"):
            provider = filename.replace("_wnd.txt", "")
            
            # Initialize provider entry
            provider_config[provider] = {
                "client": provider,
                "models": {}
            }
            
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or '|' not in line:
                            continue
                        
                        model_name, size_str = line.split('|', 1)
                        window_size = parse_window_size(size_str)
                        
                        provider_config[provider]["models"][model_name] = {
                            "windowSize": window_size
                        }
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Write to models.json
    output_file = "models.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(provider_config, f, indent=2)

    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    main()
