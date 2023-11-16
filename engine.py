import os
import filetype
import magic
import platform
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import subprocess
import csv
import pyexifinfo
import hashlib


class AppEngine:
    def __init__(self, root):
        self.root = root
        self.system = platform.system()
        self.folder_path = tk.StringVar()
        self.file_path = tk.StringVar()
        self.treeview = None
        self.text_widget = None
        self.tree_button_click_count = 0
        self.data_to_save = None

    def choose_directory(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)

    def toggle_fullscreen(self, event):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def display_tree_python(self):
        if self.folder_path.get():
            folder_path = self.folder_path.get()

            if self.treeview:
                self.treeview.destroy()

            if self.tree_button_click_count == 0:
                for folder, _, files in os.walk(folder_path):
                    relative_path = os.path.relpath(folder, folder_path)
                    indent_level = relative_path.count(os.sep)

                    self.root.listbox.insert(
                        tk.END,
                        f"{'    ' * indent_level}└─ {os.path.basename(folder)}\\",
                    )

                    for file in files:
                        file_path = os.path.join(folder, file)
                        content_type_filetype = filetype.guess(file_path)
                        file_size = os.path.getsize(file_path)

                        if content_type_filetype:
                            self.root.listbox.insert(
                                tk.END,
                                f"{'    ' * (indent_level + 1)}└─ {file} - {content_type_filetype.mime}",
                            )
                        else:
                            self.root.listbox.insert(
                                tk.END,
                                f"{'    ' * (indent_level + 1)}└─ {file} - Unsupported type",
                            )
                    self.tree_button_click_count += 1
            else:
                # ADD new action after second click
                self.root.listbox.delete(0, tk.END)

                for folder, _, files in os.walk(folder_path):
                    relative_path = os.path.relpath(folder, folder_path)
                    indent_level = relative_path.count(os.sep)

                    self.root.listbox.insert(
                        tk.END,
                        f"{'    ' * indent_level}└─ {os.path.basename(folder)}\\",
                    )

                    for file in files:
                        file_path = os.path.join(folder, file)
                        content_type_filetype = filetype.guess(file_path)
                        file_size = os.path.getsize(file_path)

                        if content_type_filetype:
                            self.root.listbox.insert(
                                tk.END,
                                f"{'    ' * (indent_level + 1)}└─ {file} - {content_type_filetype} - File Size: {file_size} bajts",
                            )
                        else:
                            self.root.listbox.insert(
                                tk.END,
                                f"{'    ' * (indent_level + 1)}└─ {file} - Unsupported type - File Size: {file_size} bajts",
                            )

                self.tree_button_click_count = 0  # Reset counter
            self.data_to_save = "tree"

    def display_file_size(self):
        file_path = self.file_path.get()
        folder_path = self.folder_path.get()

        if not file_path and not folder_path:
            messagebox.showinfo("Error", "Please choose a file or a directory.")
            return

        try:
            # Delete old Treeview before starting
            if self.treeview:
                self.treeview.destroy()

            # Create new Treeview
            self.treeview = ttk.Treeview(
                self.root.listbox, columns=("File Name", "File size"), show="headings"
            )
            self.treeview.heading("File Name", text="File Name")
            self.treeview.heading("File size", text="File size (bajt)")
            if file_path:  # One file manage
                file_size = os.path.getsize(file_path)
                self.display_treeview({os.path.basename(file_path): file_size})
            elif folder_path:  # Function for the entire catalog
                self.root.listbox.delete(0, tk.END)

                for root, _, files in os.walk(folder_path):
                    row_counter = 0
                    toggle_color = True

                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            color = "oddrow" if toggle_color else "evenrow"
                            self.display_treeview(
                                {f"{file} - File Size": file_size}, color=color
                            )

                            row_counter += 1

                            # Changing the value of a boolean variable every other row
                            if row_counter % 1 == 0:
                                toggle_color = not toggle_color
                        except FileNotFoundError:
                            self.display_treeview({f"{file} - File not found": ""})

            self.data_to_save = "file_size"
        except FileNotFoundError:
            messagebox.showinfo("Error", "File not found.")

    def display_exiftool_linux(self):
        file_path = self.file_path.get()
        folder_path = self.folder_path.get()

        if not file_path and not folder_path:
            messagebox.showinfo("Error", "Please choose a file or a directory.")
            return

        try:
            # Delete old Treeview before starting
            if self.treeview:
                self.treeview.destroy()

            # Create new Treeview
            self.treeview = ttk.Treeview(
                self.root.listbox, columns=("Tag", "Description"), show="headings"
            )
            self.treeview.heading("Tag", text="Tag")
            self.treeview.heading("Description", text="Description")

            if folder_path:  # Function for the entire catalog
                self.root.listbox.delete(0, tk.END)

                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        metadata = pyexifinfo.get_json(file_path)
                        if isinstance(metadata, list) and len(metadata) > 0:
                            metadata_dict = metadata[0]
                            self.display_treeview(metadata_dict)
                            self.treeview.insert(
                                "",
                                "end",
                                values=(
                                    "--------------------------------------------",
                                    "--------------------------------------------",
                                ),
                                tags=("oddrow",),
                            )
                        else:
                            # For an empty file, create one empty field in Treeview
                            self.display_treeview({}, include_header=False)

            elif file_path:  # One file manage
                metadata = pyexifinfo.get_json(file_path)

                if isinstance(metadata, list) and len(metadata) > 0:
                    metadata_dict = metadata[0]
                else:
                    metadata_dict = {}

                self.display_treeview(metadata_dict)

            self.data_to_save = "exiftool"
        except FileNotFoundError:
            messagebox.showinfo(
                "Error", "Exiftool is not available. Please install it."
            )

    def display_treeview(self, metadata_dict, color="oddrow", include_header=True):
        # Wstaw dane do Treeview
        row_counter = 0

        if include_header:
            for tag, value in metadata_dict.items():
                self.treeview.insert("", "end", values=(tag, value), tags=(color,))
                row_counter += 1
                color = "evenrow" if color == "oddrow" else "oddrow"

        else:
            values = tuple(metadata_dict.values())
            self.treeview.insert("", "end", values=values, tags=(color,))
        # # If metadata_dict is empty, add one blank field to keep the headers visible
        # if row_counter == 0:
        #     self.treeview.insert("", "end", values=("", ""), tags=("oddrow",))

        # set style tag
        self.treeview.tag_configure("oddrow", background="white")
        self.treeview.tag_configure("evenrow", background="#f0f0f0")

        # add scroll bar
        treeview_scrollbar = ttk.Scrollbar(
            self.root.listbox, orient="vertical", command=self.treeview.yview
        )
        treeview_scrollbar.grid(row=2, column=4, sticky="ns")
        self.treeview.configure(yscrollcommand=treeview_scrollbar.set)

        # Calculate the height of the Treeview based on the number of rows in the Listbox
        listbox_height = self.root.listbox.winfo_reqheight()
        row_height = 20  # One row height 20 px
        treeview_height = min(listbox_height, row_counter * row_height)

        # center Tree
        self.treeview.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.root.listbox.grid_rowconfigure(2, weight=1)
        self.root.listbox.grid_columnconfigure(0, weight=1)

    def display_file_extension(self):
        file_path = self.file_path.get()
        folder_path = self.folder_path.get()

        if not file_path and not folder_path:
            messagebox.showinfo("Error", "Please choose a file or a directory.")
            return

        # Delete old Treeview before starting
        if self.treeview:
            self.treeview.destroy()

        # Create new Treeview
        self.treeview = ttk.Treeview(
            self.root.listbox,
            columns=("File Name", "File Type (magic)", "File Type (filetype)"),
            show="headings",
        )
        self.treeview.heading("File Name", text="File Name")
        self.treeview.heading("File Type (magic)", text="File Type (magic)")
        self.treeview.heading("File Type (filetype)", text="File Type (filetype)")

        try:
            if file_path:  # One file manage
                try:
                    file_name = os.path.basename(file_path)
                    content_type_magic = (
                        magic.from_file(file_path, mime=True)
                        if magic.from_file(file_path, mime=True)
                        else None
                    )
                    content_type_filetype = (
                        filetype.guess(file_path) if filetype.guess(file_path) else None
                    )

                except UnicodeDecodeError:
                    file_name = os.path.basename(file_path)
                    content_type_magic = "Change file name (magic-lib problem)"

                content_type_filetype = (
                    filetype.guess(file_path) if filetype.guess(file_path) else None
                )

                # Use the display_treeview function to display the data
                self.display_treeview(
                    {
                        "File Name": file_name,
                        "File Type (magic)": content_type_magic,
                        "File Type (filetype)": content_type_filetype.mime
                        if content_type_filetype
                        else "Unknown",
                    },
                    include_header=False,
                )

            elif folder_path:
                self.root.listbox.delete(0, tk.END)

                for root, _, files in os.walk(folder_path):
                    row_counter = 0
                    toggle_color = True

                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_name = os.path.basename(file_path)
                            content_type_magic = magic.from_file(file_path, mime=True)
                        except UnicodeDecodeError:
                            file_name = os.path.basename(file_path)
                            content_type_magic = "Change file name (magic-lib problem)"

                        content_type_filetype = (
                            filetype.guess(file_path)
                            if filetype.guess(file_path)
                            else None
                        )

                        # Use the display_treeview function to display the data
                        self.display_treeview(
                            {
                                "File Name": file_name,
                                "File Type (magic)": content_type_magic,
                                "File Type (filetype)": content_type_filetype.mime
                                if content_type_filetype
                                else "Unknown",
                            },
                            color="oddrow" if toggle_color else "evenrow",
                            include_header=False,
                        )

                        row_counter += 1
                        try:
                            # Changing the value of a boolean variable every other row
                            if row_counter % 1 == 0:
                                toggle_color = not toggle_color
                        except Exception as e:
                            # Use the display_treeview function to display the error
                            self.display_treeview(
                                {
                                    "File Name": file,
                                    "File Type (magic)": "Error",
                                    "File Type (filetype)": "Error",
                                },
                                color="errorrow",
                                include_header=False,
                            )
                            messagebox.showinfo("Error", f"An error occurred: {str(e)}")
            self.data_to_save = "file_extension"
        except FileNotFoundError:
            messagebox.showinfo("Error", "File not found.")

    def display_strings(self):
        if self.file_path.get():
            file_path = self.file_path.get()

            if self.treeview:
                self.treeview.destroy()

            try:
                with open(file_path, "r", errors="replace") as file:
                    file_content = file.read()

                # Remove the old Text widget if it exists
                if hasattr(self, "text_widget") and self.text_widget is not None:
                    self.text_widget.destroy()

                # Create a new Text widget
                self.text_widget = tk.Text(self.root.listbox, wrap="word", height=10)

                # Add a vertical scrollbar
                text_widget_scrollbar = ttk.Scrollbar(
                    self.root.listbox, orient="vertical", command=self.text_widget.yview
                )
                text_widget_scrollbar.grid(row=2, column=4, sticky="ns")
                self.text_widget.configure(yscrollcommand=text_widget_scrollbar.set)

                self.text_widget.insert(tk.END, file_content)

                # Calculate the height of the Text widget based on the number of text lines
                num_lines = file_content.count("\n") + 1
                row_height = 20  # Assume the height of a single line is 20 pixels
                text_widget_height = min(10 * row_height, num_lines * row_height)

                # Center the Text widget
                self.text_widget.grid(row=2, column=0, columnspan=4, sticky="nsew")
                self.root.listbox.grid_rowconfigure(2, weight=1)
                self.root.listbox.grid_columnconfigure(0, weight=1)
                self.data_to_save = "strings"
            except FileNotFoundError:
                messagebox.showinfo("Error", "File not found.")

    def reset_fields(self):
        self.folder_path.set("")
        self.file_path.set("")
        self.root.listbox.delete(0, tk.END)

        # Remove the Treeview if it exists
        if self.treeview:
            self.treeview.destroy()
            self.treeview = None

        # Remove the Text widget if it exists
        if hasattr(self, "text_widget") and self.text_widget is not None:
            self.text_widget.destroy()
            self.text_widget = None

    def save_helper(self, save_file):
        csv_writer = csv.writer(save_file)
        headers = [
            self.treeview.heading(column)["text"] for column in self.treeview["columns"]
        ]
        csv_writer.writerow(headers)

        for item_id in self.treeview.get_children():
            item = self.treeview.item(item_id)
            values = item["values"]
            csv_writer.writerow(values)

    def save_to_csv(self):
        if self.data_to_save == "tree" or self.data_to_save == "strings":
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Text files", "*.txt")]
            )
        else:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")],
            )

        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8", newline="") as save_file:
                    if self.data_to_save == "tree":
                        for index in range(self.root.listbox.size()):
                            save_file.write(self.root.listbox.get(index) + "\n")
                    elif self.data_to_save == "strings":
                        text_widget_content = self.text_widget.get("1.0", tk.END)
                        save_file.write(text_widget_content)

                    elif self.data_to_save == "file_extension":
                        csv_writer = csv.writer(save_file)
                        headers = [
                            self.treeview.heading(column)["text"]
                            for column in self.treeview["columns"]
                        ]
                        csv_writer.writerow(headers)

                        for item_id in self.treeview.get_children():
                            item = self.treeview.item(item_id)
                            values = item["values"]
                            csv_writer.writerow(values)

                    elif self.data_to_save == "file_size":
                        self.save_helper(save_file)

                    elif self.data_to_save == "exiftool":
                        self.save_helper(save_file)

                messagebox.showinfo(
                    "Data Saved", f"Data saved successfully to: {save_path}"
                )

            except PermissionError:
                messagebox.showinfo(
                    "Error", "Permission error. Please choose a different location."
                )
