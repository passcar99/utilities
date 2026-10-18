
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

from engine import merge_pdfs, parse_slices, PdfReader


class PDFMergeApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF Merger")
        root.geometry("760x420")

        toolbar = ttk.Frame(root, padding=10)
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar, text="Add PDF", command=self.add_files
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Edit slices", command=self.edit_slices
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Remove", command=self.remove
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Move up", command=lambda: self.move(-1)
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar, text="Move down", command=lambda: self.move(1)
        ).pack(side="left", padx=3)

        self.table = ttk.Treeview(
            root, columns=("file", "slices"),
            show="headings", selectmode="browse"
        )
        self.table.heading("file", text="PDF file")
        self.table.heading("slices", text="Page slices")
        self.table.column("file", width=540)
        self.table.column("slices", width=150)
        self.table.pack(fill="both", expand=True, padx=10, pady=5)

        bottom = ttk.Frame(root, padding=10)
        bottom.pack(fill="x")

        self.output = tk.StringVar(value="merged.pdf")
        ttk.Entry(bottom, textvariable=self.output).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            bottom, text="Save as...", command=self.choose_output
        ).pack(side="left", padx=5)

        ttk.Button(
            bottom, text="Merge PDFs",
            command=self.merge
        ).pack(side="right", padx=5)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Choose PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        for path in paths:
            if any(self.table.item(i, "values")[0] == path
                   for i in self.table.get_children()):
                continue

            spec = simpledialog.askstring(
                "Page slices",
                f"Pages from {path.split('/')[-1]}\n"
                "Examples: 1-3,8 or all",
                initialvalue="all",
                parent=self.root
            )
            if spec is not None:
                self.table.insert("", "end", values=(path, spec))

    def edit_slices(self):
        selected = self.table.selection()
        if not selected:
            return

        item = selected[0]
        path, old_spec = self.table.item(item, "values")
        spec = simpledialog.askstring(
            "Page slices", f"Pages to include from:\n{path}",
            initialvalue=old_spec, parent=self.root
        )
        if spec is not None:
            self.table.item(item, values=(path, spec))

    def remove(self):
        for item in self.table.selection():
            self.table.delete(item)

    def move(self, direction):
        selected = self.table.selection()
        if not selected:
            return

        item = selected[0]
        siblings = list(self.table.get_children())
        index = siblings.index(item)
        new_index = index + direction

        if 0 <= new_index < len(siblings):
            self.table.move(item, "", new_index)
            self.table.selection_set(item)

    def choose_output(self):
        path = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if path:
            self.output.set(path)

    def merge(self):
        rows = self.table.get_children()
        if not rows:
            messagebox.showwarning(
                "No files", "Add at least one PDF first."
            )
            return

        output = self.output.get().strip()
        if not output:
            messagebox.showerror("Missing output", "Choose an output file.")
            return

        inputs = [
            (self.table.item(row, "values")[0],
             self.table.item(row, "values")[1])
            for row in rows
        ]

        try:
            for path, spec in inputs:
                parse_slices(spec, len(PdfReader(path).pages))

            merge_pdfs(inputs, output)
            messagebox.showinfo(
                "Success", f"Merged PDF saved to:\n{output}"
            )
        except Exception as exc:
            messagebox.showerror("Merge failed", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergeApp(root)
    root.mainloop()
