import os
import sys

from textual.features import parse_features

from waylonwalker.app import WaylonWalker


def main():

    # this works, but putting it behind argparse, click, or typer would be much
    # better

    dev = "--dev" in sys.argv

    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if dev:
        features.add("debug")
        features.add("devtools")

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    app = WaylonWalker()
    app.run()


if __name__ == "__main__":
    main()
