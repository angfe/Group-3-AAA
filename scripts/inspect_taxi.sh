#!/usr/bin/env bash
set -euo pipefail

# inspect_taxi.sh - quick CSV inspection using xsv
# Usage: inspect_taxi.sh [CSV_FILE] [PREVIEW_ROWS] [COLUMN...]
# If no CSV_FILE given, defaults to data/Taxi_Trips_(2024-)_20260514.csv
# If no COLUMNs given, the script will try to auto-detect common numeric columns.

file="${1:-data/Taxi_Trips_(2024-)_20260514.csv}"
preview="${2:-10}"
# columns begin at position 3 (if any)
cols=()
if [ "$#" -ge 3 ]; then
  cols=("${@:3}")
fi

if ! command -v xsv >/dev/null 2>&1; then
  echo "xsv is required but not found. Install from https://github.com/BurntSushi/xsv"
  exit 1
fi

if [ ! -f "$file" ]; then
  echo "File not found: $file"
  exit 1
fi

echo "File: $file"
echo
echo "== Headers =="
# show headers with index numbers
xsv headers "$file" | nl -ba
echo
echo "== Row count =="
xsv count "$file" || echo "(xsv count failed)"
echo
echo "== Preview (first $preview rows) =="
# Use head to grab header + first N rows; some xsv builds reject the slice args
head -n $((preview + 1)) "$file" | xsv table || head -n $((preview + 1)) "$file"
echo

echo "== Writing selected stats using xsv =="
mkdir -p data/interim
# If columns are provided, use -s to select them; else, stats for all columns
if [ ${#cols[@]} -gt 0 ]; then
  sel=$(IFS=,; echo "${cols[*]}")
  xsv stats -s "$sel" "$file" > data/interim/selected_stats.csv || echo "xsv stats failed for $file (columns: $sel)"
else
  xsv stats "$file" > data/interim/selected_stats.csv || echo "xsv stats failed for $file"
fi

echo
echo "Done."
