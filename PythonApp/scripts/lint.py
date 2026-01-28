import subprocess
import sys


def run():
	subprocess.call(
		["ruff", "check", "note_app", "--fix"],
		stdout=sys.stdout,
		stderr=sys.stderr
	)