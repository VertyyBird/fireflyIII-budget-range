# r50 — Firefly Budget Range Generator
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

A command-line tool to generate ±% budget ranges for recurring expenses and save them for use with [Firefly III](https://firefly-iii.org), the self-hosted personal finance manager.

## Features
- Calculates ±% range for a given base amount
- Outputs a Firefly III rule string
- Optional label and note saving
- Clipboard support via `xclip`
- Smart duplicate handling with overwrite, skip, or duplicate options

## Usage
```bash
r50 5               # Base amount $5 with default ±50%
r50 4 25            # $4 ±25%
r50 -n Spotify -s 5 20  # Labelled, saved
r50 -l              # List saved entries
```

### Options
- `-n`, `--name`       Label your rule with a name
- `-s`, `--save`       Save to `~/Documents/budget_notes.txt`
- `-c`, `--copy`       Copy rule to clipboard using `xclip`
- `-l`, `--list`       List saved entries

### Example Output

```bash
$ r50 -n Spotify -s -c 5 25
Original: $5.00|-25%: $3.75|+25%: $6.25

Firefly rule: Amount ≥ $3.75 and ≤ $6.25

Labelled as: Spotify
Copied to clipboard.
An entry with the same name and amount already exists.
What would you like to do?
[o] Overwrite
[d] Drop the new one
[n] Write as new line (duplicate)
Choice (o/d/n): n
Duplicate entry saved to file: /home/<user>/Documents/budget_notes.txt
```

## Requirements
- Python 3.6+
- xclip for clipboard support

## Installation
You can install r50 in just a few steps:

### 1. Download the script
If you're on GitHub, click the green **Code** button and choose **Download ZIP**. Then extract it somewhere like your Desktop.

Or if you have git installed:
```bash
git clone https://github.com/yourusername/firefly-budget-range.git
cd firefly-budget-range
```

### 2. Make the script executable
This lets your system run it like a command:
```bash
chmod +x r50.py
```

### 3. Move it to a folder in your PATH
This allows you to run it from anywhere. A common choice is your `~/bin` folder:
```bash
mkdir -p ~/bin
mv r50.py ~/bin/r50
```
> 💡 We're renaming it to just `r50` for convenience.

### 4. Make sure ~/bin is in your PATH
Add this to the bottom of your `~/.bashrc`, `~/.zshrc`, or `~/.profile` (whichever your shell uses):
```bash
export PATH=\"$HOME/bin:$PATH\"
```

Then refresh your terminal:
```bash
source ~/.bashrc   # or source ~/.zshrc, etc.
```

### 5. (Optional) Install clipboard support
If you want `r50` to copy results to your clipboard, install `xclip`:
```bash
sudo apt install xclip      # Debian/Ubuntu
# or
sudo dnf install xclip      # Fedora
# or
sudo pacman -S xclip        # Arch
```

### You're ready!
Now you can run `r50` from anywhere:
```bash
r50 10         # Calculates ±50% of $10
r50 -n Netflix -s 13.99
```

## License
MIT
