# =============================================================================
# FILE:         main.py
# AUTHOR:       Hamoon Soleimani
# CREATED:      [Current Date, e.g., October 26, 2023]
# DESCRIPTION:  A modern desktop application to consolidate any code project 
#               into a single, structured text file for AI analysis.
# LICENSE:      MIT License - see LICENSE file for details.
# =============================================================================

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import platform
import subprocess

# --- Default Configuration ---
# You can change these default values
DEFAULT_INCLUDE_EXTENSIONS = [
    '.kt', '.java', '.xml', '.gradle', '.kts', '.pro', '.md', 
    '.json', '.yml', '.yaml', '.py', '.js', '.html', '.css'
]
DEFAULT_EXCLUDE_PATTERNS = [
    '.git', '.idea', 'build', '.gradle', 'gradle', 'captures', 
    'local.properties', '.DS_Store', '__pycache__', 'node_modules'
]

class ProjectConsolidator:
    """
    Handles the backend logic of scanning directories and consolidating files.
    """
    def __init__(self, root_dir, output_file, include_ext, exclude_patterns, 
                 progress_callback=None, status_callback=None, finished_callback=None):
        self.root_dir = root_dir
        self.output_file = output_file
        self.include_ext = include_ext
        self.exclude_patterns = exclude_patterns
        
        # Callbacks to update the GUI
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.finished_callback = finished_callback

    def run(self):
        """Starts the consolidation process."""
        thread = threading.Thread(target=self._process_files)
        thread.daemon = True
        thread.start()

    def _update_status(self, message):
        if self.status_callback:
            self.status_callback(message)
    
    def _update_progress(self, value):
        if self.progress_callback:
            self.progress_callback(value)

    def _process_files(self):
        self._update_status("Starting scan...")
        total_files_to_process = 0
        files_to_process_list = []

        # First, walk the tree to count files for the progress bar
        for dirpath, dirnames, filenames in os.walk(self.root_dir, topdown=True):
            # Prune excluded directories
            dirnames[:] = [d for d in dirnames if d not in self.exclude_patterns]
            
            for filename in filenames:
                if any(filename.endswith(ext) for ext in self.include_ext) and filename not in self.exclude_patterns:
                    total_files_to_process += 1
                    files_to_process_list.append(os.path.join(dirpath, filename))

        self._update_status(f"Found {total_files_to_process} files to process.")
        
        processed_files = 0
        total_lines = 0
        
        try:
            with open(self.output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
                project_name = os.path.basename(self.root_dir)
                outfile.write(f"--- Project Context for: {project_name} ---\n\n")
                
                for file_path in files_to_process_list:
                    relative_path = os.path.relpath(file_path, self.root_dir)
                    self._update_status(f"Processing: {relative_path}")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            content = infile.read()
                            lines = content.count('\n') + 1
                            total_lines += lines
                            
                            outfile.write("=" * 80 + "\n")
                            outfile.write(f"### FILE: {relative_path}\n")
                            outfile.write("=" * 80 + "\n")
                            
                            # Determine language for markdown block
                            lang = os.path.splitext(file_path)[1].lstrip('.')
                            outfile.write(f"```{lang}\n")
                            outfile.write(content)
                            outfile.write("\n```\n\n")
                            
                    except Exception as e:
                        outfile.write(f"--- ERROR reading {relative_path}: {e} ---\n\n")

                    processed_files += 1
                    self._update_progress(processed_files / total_files_to_process)
            
            output_size_kb = os.path.getsize(self.output_file) / 1024
            summary = {
                "status": "Success",
                "files_processed": processed_files,
                "total_lines": total_lines,
                "output_size_kb": output_size_kb
            }

        except Exception as e:
            summary = {"status": "Error", "message": str(e)}

        if self.finished_callback:
            self.finished_callback(summary)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Codebase Context Generator by Hamoon Soleimani")
        self.geometry("800x750")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_widgets()

    def create_widgets(self):
        # --- Frame 1: IO Paths ---
        io_frame = ctk.CTkFrame(self)
        io_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        io_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(io_frame, text="Project Directory:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.project_dir_entry = ctk.CTkEntry(io_frame, placeholder_text="Select a project folder...")
        self.project_dir_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(io_frame, text="Browse...", command=self.browse_project_dir).grid(row=0, column=2, padx=10, pady=5)

        ctk.CTkLabel(io_frame, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.output_file_entry = ctk.CTkEntry(io_frame, placeholder_text="Select a save location...")
        self.output_file_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(io_frame, text="Save As...", command=self.browse_output_file).grid(row=1, column=2, padx=10, pady=5)

        # --- Frame 2: Configuration ---
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        config_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(config_frame, text="File Extensions to Include (comma-separated):").pack(padx=10, pady=(10,0), anchor="w")
        self.include_entry = ctk.CTkEntry(config_frame)
        self.include_entry.insert(0, ", ".join(DEFAULT_INCLUDE_EXTENSIONS))
        self.include_entry.pack(padx=10, pady=5, fill="x", expand=True)

        ctk.CTkLabel(config_frame, text="Directories/Files to Exclude (comma-separated):").pack(padx=10, pady=(10,0), anchor="w")
        self.exclude_entry = ctk.CTkEntry(config_frame)
        self.exclude_entry.insert(0, ", ".join(DEFAULT_EXCLUDE_PATTERNS))
        self.exclude_entry.pack(padx=10, pady=5, fill="x", expand=True)

        # --- Frame 3: Actions, Progress, and Summary ---
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

        action_bar_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        action_bar_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        action_bar_frame.grid_columnconfigure(0, weight=1)

        self.generate_button = ctk.CTkButton(action_bar_frame, text="🚀 Generate Context File", command=self.start_generation)
        self.generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.status_label = ctk.CTkLabel(results_frame, text="Ready.", anchor="w")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(results_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.summary_textbox = ctk.CTkTextbox(results_frame, state="disabled", wrap="word", font=("Courier New", 12))
        self.summary_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        results_actions_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        results_actions_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        results_actions_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.copy_button = ctk.CTkButton(results_actions_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, state="disabled")
        self.copy_button.grid(row=0, column=0, padx=5, sticky="ew")
        self.open_button = ctk.CTkButton(results_actions_frame, text="Open Output File", command=self.open_output_file, state="disabled")
        self.open_button.grid(row=0, column=1, padx=5, sticky="ew")


    def browse_project_dir(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.project_dir_entry.delete(0, "end")
            self.project_dir_entry.insert(0, path)

    def browse_output_file(self):
        path = filedialog.asksaveasfilename(title="Save Output As", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.output_file_entry.delete(0, "end")
            self.output_file_entry.insert(0, path)

    def start_generation(self):
        project_dir = self.project_dir_entry.get()
        output_file = self.output_file_entry.get()
        
        if not project_dir or not os.path.isdir(project_dir):
            messagebox.showerror("Error", "Please select a valid project directory.")
            return
        if not output_file:
            messagebox.showerror("Error", "Please select an output file path.")
            return

        self.generate_button.configure(state="disabled", text="Processing...")
        self.copy_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.summary_textbox.configure(state="normal")
        self.summary_textbox.delete("1.0", "end")
        self.summary_textbox.configure(state="disabled")

        include_ext = [item.strip() for item in self.include_entry.get().split(',') if item.strip()]
        exclude_patterns = [item.strip() for item in self.exclude_entry.get().split(',') if item.strip()]

        consolidator = ProjectConsolidator(
            root_dir=project_dir,
            output_file=output_file,
            include_ext=include_ext,
            exclude_patterns=exclude_patterns,
            progress_callback=self.update_progress,
            status_callback=self.update_status,
            finished_callback=self.on_generation_complete
        )
        consolidator.run()

    def update_progress(self, value):
        self.progress_bar.set(value)

    def update_status(self, text):
        self.status_label.configure(text=text)

    def on_generation_complete(self, summary):
        self.generate_button.configure(state="normal", text="🚀 Generate Context File")
        
        self.summary_textbox.configure(state="normal")
        self.summary_textbox.delete("1.0", "end")
        
        if summary["status"] == "Success":
            self.status_label.configure(text=f"Success! Project context saved to {os.path.basename(self.output_file_entry.get())}")
            summary_text = (
                f"--- Generation Complete ---\n\n"
                f"Files Processed: {summary['files_processed']}\n"
                f"Total Lines of Code: {summary['total_lines']:,}\n"
                f"Output File Size: {summary['output_size_kb']:.2f} KB\n\n"
                f"Output saved to:\n{self.output_file_entry.get()}"
            )
            self.summary_textbox.insert("1.0", summary_text)
            self.copy_button.configure(state="normal")
            self.open_button.configure(state="normal")
        else:
            self.status_label.configure(text=f"Error: {summary['message']}")
            self.summary_textbox.insert("1.0", f"An error occurred:\n\n{summary['message']}")
            
        self.summary_textbox.configure(state="disabled")
    
    def copy_to_clipboard(self):
        output_file = self.output_file_entry.get()
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.clipboard_clear()
            self.clipboard_append(content)
            self.status_label.configure(text="Content copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file to copy: {e}")
            
    def open_output_file(self):
        output_file = self.output_file_entry.get()
        try:
            if platform.system() == "Windows":
                os.startfile(output_file)
            elif platform.system() == "Darwin": # macOS
                subprocess.call(("open", output_file))
            else: # Linux
                subprocess.call(("xdg-open", output_file))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
