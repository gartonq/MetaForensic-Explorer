import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import PhotoImage, filedialog, messagebox

from engine import AppEngine

class GraphicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Metadata Viewer")

        self.style = ThemedStyle(self)
        self.style.set_theme("breeze")  # Set initial theme

        self.app_engine = AppEngine(self)

        # Choose directory
        self.label_dir = ttk.Label(self, text="Choose directory:")
        self.label_dir.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.entry_dir = ttk.Entry(self, textvariable=self.app_engine.folder_path)
        self.entry_dir.grid(row=0, column=1, pady=10, padx=10, sticky="we")

        self.button_dir = ttk.Button(self, text="Choose directory", command=self.app_engine.choose_directory)
        self.button_dir.grid(row=0, column=2, pady=10, padx=10, sticky="we")

        # Choose file
        self.label_file = ttk.Label(self, text="Choose file:")
        self.label_file.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        self.entry_file = ttk.Entry(self, textvariable=self.app_engine.file_path)
        self.entry_file.grid(row=1, column=1, pady=10, padx=10, sticky="we")

        self.button_file = ttk.Button(self, text="Choose file", command=self.app_engine.choose_file)
        self.button_file.grid(row=1, column=2, pady=10, padx=10, sticky="we")

        # Listbox and scrollbar
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=3, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.config(width=80, height=13)

        # Reset button
        self.button_reset = ttk.Button(self, text="Reset", command=self.app_engine.reset_fields)
        self.button_reset.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Mode toggle button
        self.light_mode_image = PhotoImage(file="pictures-button/on.png")
        self.dark_mode_image = PhotoImage(file="pictures-button/off.png")

        self.mode_button = ttk.Button(
            self,
            image=self.light_mode_image,
            text="Light Mode",
            compound="left",
            command=self.toggle_mode
        )
        self.mode_button.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        # Fullscreen binding for Linux
        if self.app_engine.system == 'Linux':
            self.bind('<F11>', self.app_engine.toggle_fullscreen)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.bind("<Configure>", self.on_resize)

        # Buttons for various functionalities
        self.button_tree = ttk.Button(self, text="Tree", command=self.app_engine.display_tree_python)
        self.button_tree.grid(row=6, column=0, columnspan=1, pady=10, padx=5, sticky="nsew")

        self.button_file_size = ttk.Button(self, text="File Size", command=self.app_engine.display_file_size)
        self.button_file_size.grid(row=6, column=1, columnspan=1, pady=10, padx=5, sticky="nsew")

        self.button_exiftool_linux = ttk.Button(self, text="Metadata", command=self.app_engine.display_exiftool_linux)
        self.button_exiftool_linux.grid(row=6, column=2, columnspan=1, pady=10, padx=5, sticky="nsew")

        self.button_file_extension = ttk.Button(self, text="File Extension", command=self.app_engine.display_file_extension)
        self.button_file_extension.grid(row=7, column=0, columnspan=1, pady=10, padx=5, sticky="nsew")

        self.button_strings = ttk.Button(self, text="Strings", command=self.app_engine.display_strings)
        self.button_strings.grid(row=7, column=1, columnspan=1, pady=10, padx=5, sticky="nsew")

        self.button_save_to_csv = ttk.Button(self, text="Save", command=self.app_engine.save_to_csv)
        self.button_save_to_csv.grid(row=7, column=2, columnspan=1, pady=10, padx=5, sticky="nsew")

    def toggle_mode(self):
        current_theme = self.style.theme_use()

        if self.mode_button.cget("text") == "Dark Mode":
            self.mode_button.configure(image=self.light_mode_image, text="Light Mode")
            self.style.set_theme("breeze")  # Set light theme
        else:
            self.mode_button.configure(image=self.dark_mode_image, text="Dark Mode")
            self.style.set_theme("equilux")  # Set dark theme

        self.apply_theme()  # Apply theme to other elements again

    def apply_theme(self):
        elements = [self, self.label_dir, self.entry_dir, self.button_dir, self.label_file,
                    self.entry_file, self.button_file, self.listbox, self.button_reset,
                    self.button_tree, self.button_file_size, self.button_exiftool_linux, self.button_file_extension,
                    self.button_strings, self.button_save_to_csv]
        current_theme = self.style.theme_use()

        for element in elements:
            element_class = element.winfo_class()

            if "background" in self.style.element_options(element_class):
                element.configure(bg=self.style.lookup(element_class, "background"))

            if "foreground" in self.style.element_options(element_class):
                element.configure(fg=self.style.lookup(element_class, "foreground"))

            if isinstance(element, ttk.Button):
                element_style = current_theme + ".TButton"
                element.configure(style=element_style)

        # Additional background handling for the whole application
        app_bg = self.style.lookup("TFrame", "background")
        self.configure(bg=app_bg)

        label_color = self.style.lookup("TLabel", "foreground")
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(foreground=label_color)

    def on_resize(self, event):
        
        self.listbox.config(width=self.winfo_width() - 20)

if __name__ == "__main__":
    graphic_app = GraphicApp()
    graphic_app.geometry("800x600")
    graphic_app.mainloop()
