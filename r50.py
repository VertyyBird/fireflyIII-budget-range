#!/usr/bin/env python3
import argparse
import sys
import subprocess
import os

# ANSI colours
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

parser = argparse.ArgumentParser(description="Generate Firefly-friendly budget ranges.")
parser.add_argument("amount", type=float, nargs="?", help="The base amount to calculate from.")
parser.add_argument("percent", type=float, nargs="?", default=50, help="Optional percent range (default 50)")
parser.add_argument("-n", "--name", type=str, help="Optional name/label to include")
parser.add_argument("-s", "--save", action="store_true", help="Save the Firefly rule to ~/Documents/budget_notes.txt")
parser.add_argument("-c", "--copy", action="store_true", help="Copy Firefly rule to clipboard")
parser.add_argument("-l", "--list", action="store_true", help="List all saved entries and exit")

args = parser.parse_args()
filepath = os.path.expanduser("~/Documents/budget_notes.txt")

# --list mode
if args.list:
    try:
        with open(filepath, "r") as f:
            entries = f.read().strip()
            if entries:
                print(f"{CYAN}Saved budget entries:{RESET}\n{entries}")
            else:
                print(f"{CYAN}No entries saved yet.{RESET}")
    except FileNotFoundError:
        print(f"{RED}No saved file found at:{RESET} {filepath}")
    sys.exit(0)

if args.amount is None:
    print(f"{RED}Error:{RESET} Amount is required unless using --list")
    sys.exit(1)

low = args.amount - (args.amount * (args.percent / 100))
high = args.amount + (args.amount * (args.percent / 100))

# Build the Firefly rule
firefly_rule = f"Amount ≥ ${low:.2f} and ≤ ${high:.2f}"
if args.name:
    line = f"{args.name} (${args.amount:.2f}): {firefly_rule}"
else:
    line = f"${args.amount:.2f}: {firefly_rule}"

# Output
print(f"{CYAN}Original:{RESET} ${args.amount:.2f}|{RED}-{args.percent:.0f}%: ${low:.2f}{RESET}|{GREEN}+{args.percent:.0f}%: ${high:.2f}{RESET}")
print(f"\n{CYAN}Firefly rule:{RESET} Amount {RED}≥ ${low:.2f}{RESET} and {GREEN}≤ ${high:.2f}{RESET}")
if args.name:
    print(f"\n{CYAN}Labelled as:{RESET} {args.name}")

# Optional clipboard copy
if args.copy:
    try:
        subprocess.run(["xclip", "-selection", "clipboard"], input=line.encode(), check=True)
        print(f"{CYAN}Copied to clipboard.{RESET}")
    except FileNotFoundError:
        print(f"{RED}Clipboard tool (xclip) not found. Skipping copy.{RESET}")

# Optional save to file
if args.save:
    try:
        existing_lines = []
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                existing_lines = [l.strip() for l in f if l.strip()]

        def extract_name_amount(entry):
            if ":" in entry:
                prefix = entry.split(":")[0]
                if "(" in prefix and ")" in prefix:
                    name = prefix.split("(")[0].strip()
                    amt = prefix.split("(")[1].replace(")", "").strip()
                    try:
                        amt = float(amt.replace("$", ""))
                    except:
                        amt = None
                    return name, amt
            return None, None

        new_name, new_amt = extract_name_amount(line)
        match_found = False
        exact_match = False

        for existing in existing_lines:
            name, amt = extract_name_amount(existing)
            if name == new_name and amt == new_amt:
                match_found = True
                if existing == line:
                    exact_match = True
                break

        if exact_match:
            print(f"{CYAN}Exact entry already exists. No action taken.{RESET}")
        elif match_found:
            print(f"{CYAN}An entry with the same name and amount already exists.{RESET}")
            print(f"{CYAN}What would you like to do?{RESET}")
            print("[o] Overwrite")
            print("[d] Drop the new one")
            print("[n] Write as new line (duplicate)")
            choice = input("Choice (o/d/n): ").strip().lower()

            if choice == "o":
                existing_lines = [l for l in existing_lines if extract_name_amount(l) != (new_name, new_amt)]
                with open(filepath, "w") as f:
                    for l in existing_lines:
                        f.write(l + "\n")
                    f.write(line + "\n")
                print(f"{CYAN}Entry overwritten in file:{RESET} {filepath}")
            elif choice == "n":
                with open(filepath, "a") as f:
                    f.write(line + "\n")
                print(f"{CYAN}Duplicate entry saved to file:{RESET} {filepath}")
            else:
                print(f"{CYAN}Skipped saving.{RESET}")
        else:
            with open(filepath, "a") as f:
                f.write(line + "\n")
            print(f"{CYAN}Saved to file:{RESET} {filepath}")
    except Exception as e:
        print(f"{RED}Failed to save:{RESET} {e}")
