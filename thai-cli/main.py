#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys

# Map subcommand names to their script files and descriptions
COMMANDS = {
    "Anki Sync & Export": {
        "dump": ("dump_anki.py", "Exports all Anki notes to a timestamped CSV. Uses multithreading for speed."),
        "dump-freq": ("dump_freq_4000.py", "Exports the ~Freq 4000 deck to CSV, stripping sound tags and HTML."),
    },
    "Duplicate Auditing": {
        "audit-dupes": ("cross_model_dupes.py", "Identifies duplicate entries in the Front field (excluding ~Freq 4000)."),
        "process-dupes": ("process_dupes.py", "Interactive utility to review duplicates and flag them with 'delete-me'."),
    },
    "Vocab Analysis": {
        "nilsen-missing": ("nilsen_missing.py", "Finds words from the Jørgen Nilsen dictionary missing from Anki."),
        "fetch-common": ("get_thai_5000.py", "Downloads the top 5000 common Thai words."),
        "compare-vocab": ("compare_common_vocab.py", "Cross-references Anki vocab with common word lists."),
        "translate-missing": ("translate_missing_vocab.py", "Translates missing words using Google Translate."),
    },
    "Quote Handling": {
        "classify-quotes": ("classify_quotes.py", "Analyzes quotation styles in specific decks."),
        "quote-stats": ("quote_stats.py", "Provides detailed quotation statistics."),
        "strip-quotes": ("strip_outer_quotes.py", "Removes nested or unnecessary outer quotes across all decks."),
        "unify-quotes": ("unify_phrases_double_quotes.py", "Unifies quotation styles (standardizing double quotes in phrases)."),
    }
}

class CategorizedHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        return super()._format_action_invocation(action)

def main():
    parser = argparse.ArgumentParser(
        prog="thai",
        description="Thai Anki Management CLI - A unified toolkit for managing your collection.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Build description with categories for the help menu
    help_text = "Available commands grouped by category:\n\n"
    all_cmd_map = {}
    
    for category, cmds in COMMANDS.items():
        help_text += f"[{category}]\n"
        for name, (script, desc) in cmds.items():
            help_text += f"  {name:<20} - {desc}\n"
            all_cmd_map[name] = script
        help_text += "\n"
    
    parser.epilog = help_text

    subparsers = parser.add_subparsers(dest="command", help="The command to execute")

    # Register each command as a subparser
    for name in all_cmd_map.keys():
        sub = subparsers.add_parser(name)
        # Allow passing through additional arguments to the underlying scripts
        sub.add_argument("args", nargs=argparse.REMAINDER, help=f"Arguments to pass to {all_cmd_map[name]}")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    script_name = all_cmd_map.get(args.command)
    # The scripts are now in the same directory as main.py
    # Use realpath to handle the case where this is called via a symlink
    script_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(script_dir, script_name)

    if not os.path.exists(script_path):
        print(f"Error: Script '{script_name}' not found at {script_path}")
        sys.exit(1)

    # Construct the command to run
    cmd = [sys.executable, script_path]
    if args.args:
        cmd.extend(args.args)

    try:
        # Run the script, inheriting stdin/stdout for interactivity
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nCommand '{args.command}' failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
