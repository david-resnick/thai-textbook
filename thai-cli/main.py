#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys

# Map subcommand names to their script files (relative to the project root)
COMMANDS = {
    "Anki Sync & Export": {
        "dump": "dump_anki.py",
        "dump-freq": "dump_freq_4000.py",
    },
    "Duplicate Auditing": {
        "audit-dupes": "cross_model_dupes.py",
        "process-dupes": "process_dupes.py",
    },
    "Vocab Analysis": {
        "nilsen-missing": "nilsen_missing.py",
        "fetch-common": "get_thai_5000.py",
        "compare-vocab": "compare_common_vocab.py",
        "translate-missing": "translate_missing_vocab.py",
    },
    "Quote Handling": {
        "classify-quotes": "classify_quotes.py",
        "quote-stats": "quote_stats.py",
        "strip-quotes": "strip_outer_quotes.py",
        "unify-quotes": "unify_phrases_double_quotes.py",
    },
    # Future/Placeholder for mentioned but missing scripts
    "Legacy/External": {
        "clean-anki-front": "clean_anki_front.py",
        "list-vocab-quotes": "list_vocab_quotes.py",
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
        for name, script in cmds.items():
            help_text += f"  {name:<20} -> Runs {script}\n"
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
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
