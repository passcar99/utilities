
import argparse
import sys
from pathlib import Path

from engine import merge_pdfs


def main():
    parser = argparse.ArgumentParser(
        description="Merge selected pages from multiple PDF files.",
        epilog=(
            "Example: python cli.py --output merged.pdf "
            "first.pdf 1-3,8 second.pdf 2,5-7"
        ),
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Output PDF filename"
    )
    parser.add_argument(
        "items", nargs="+",
        help="Each PDF filename followed by its page slices"
    )

    args = parser.parse_args()
    inputs = []
    filename = None
    slices = []

    def finish_group():
        if filename is None:
            return
        if not slices:
            parser.error(f"No page slices specified for {filename}")
        inputs.append((filename, ",".join(slices)))

    for item in args.items:
        if item.lower().endswith(".pdf"):
            # finish the previous group
            finish_group()
            filename = item
            slices = []
        elif filename is None:
            parser.error(f"Expected a PDF filename, got: {item}")
        else:
            slices.append(item)

    finish_group()

    if not inputs:
        parser.error("At least one input PDF is required")

    try:
        merge_pdfs(inputs, args.output)
        print(f"Merged {len(inputs)} PDFs into {args.output}")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
