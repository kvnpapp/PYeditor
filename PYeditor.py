import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pygments import highlight
import subprocess

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyeditor")

        self.bg_color = "#2d2d2d"
        self.fg_color = "white"
        self.input_bg_color = "#1e1e1e"
        self.output_bg_color = "#2d2d2d"

        self.menu_bar = Menu(self.root, bg=self.bg_color, fg=self.fg_color)
        self.root.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        self.run_menu = Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Code", command=self.run_code)

        self.text_editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=25, font=("Arial", 12), bg=self.input_bg_color, fg=self.fg_color)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_editor.bind("<KeyRelease>", self.highlight_code)

        self.terminal = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10, font=("Arial", 12), bg=self.output_bg_color, fg=self.fg_color)
        self.terminal.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, code)
                self.highlight_code()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                code = self.text_editor.get(1.0, tk.END)
                file.write(code)

    def run_code(self):
        code = self.text_editor.get(1.0, tk.END)
        self.terminal.delete(1.0, tk.END)
        process = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if output:
            self.terminal.insert(tk.END, output + "\n")
        if error:
            self.terminal.insert(tk.END, error + "\n", "error")

            self.terminal.tag_configure("error", foreground="red")
            self.terminal.tag_add("error", "end - {} chars".format(len(error)), "end")

    def highlight_code(self, event=None):
        code = self.text_editor.get(1.0, tk.END)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, code)
        highlighted_code = highlight(code, PythonLexer(), Terminal256Formatter())
        self.text_editor.tag_configure("code", foreground="white")
        self.text_editor.tag_add("code", "1.0", "end")
        self.text_editor.mark_set("insert", "1.0")
        self.text_editor.see("insert")

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()
