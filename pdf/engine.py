
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def parse_slices(spec: str, page_count: int) -> list[int]:
    """Return zero-based page indices from a 1-based slice specification."""
    if spec.strip().lower() == "all":
        return list(range(page_count))

    pages = []

    for part in spec.split(","):
        part = part.strip()

        if not part:
            raise ValueError("Empty page range")

        if "-" in part:
            bounds = part.split("-")
            if len(bounds) != 2:
                raise ValueError(f"Invalid range: {part}")

            start, end = map(int, bounds)
            if start < 1 or end < start or end > page_count:
                raise ValueError(
                    f"Invalid range {part}; PDF has {page_count} pages"
                )
            pages.extend(range(start - 1, end))
        else:
            page = int(part)
            if not 1 <= page <= page_count:
                raise ValueError(
                    f"Invalid page {page}; PDF has {page_count} pages"
                )
            pages.append(page - 1)

    return pages


def merge_pdfs(inputs, output):
    """inputs is a sequence of (filename, slice_spec) pairs."""
    writer = PdfWriter()

    for filename, spec in inputs:
        reader = PdfReader(filename)

        for index in parse_slices(spec, len(reader.pages)):
            writer.add_page(reader.pages[index])

    with open(output, "wb") as stream:
        writer.write(stream)
