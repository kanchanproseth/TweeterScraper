import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CopyableTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add right-click context menu
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Copy", command=self.copy_selection)
        
        # Bind right-click and keyboard shortcuts
        self.bind("<Button-3>", self.show_menu)  # Right-click
        self.bind("<Control-c>", self.copy_selection)  # Windows/Linux
        self.bind("<Command-c>", self.copy_selection)  # macOS

    def show_menu(self, event):
        """Display context menu on right-click"""
        self.menu.post(event.x_root, event.y_root)

    def copy_selection(self, event=None):
        """Copy selected rows to clipboard"""
        selected_items = self.selection()
        if not selected_items:
            return

        # Get column headers
        columns = self["columns"]
        header = "\t".join([self.heading(col)["text"] for col in columns])
        
        # Get selected data
        rows = []
        for item in selected_items:
            row = [self.set(item, col) for col in columns]
            rows.append("\t".join(row))
        
        # Combine header and rows
        clipboard_text = header + "\n" + "\n".join(rows)
        
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(clipboard_text)
        self.update()