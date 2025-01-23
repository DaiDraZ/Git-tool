import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import keyword
import subprocess
import sys

class SimpleIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple IDE - Sublime Text Clone")
        self.geometry("900x600")
        self.filename = None  # File đang được mở

        # Các theme hỗ trợ
        self.themes = {
            "Light": {"bg": "#ffffff", "fg": "#000000"},
            "Dark": {"bg": "#2b2b2b", "fg": "#ffffff"},
            "Solarized": {"bg": "#fdf6e3", "fg": "#657b83" }
        }
        self.current_theme = "Light"

        # Tạo các thành phần
        self.create_menu()
        self.create_editor()  # Gọi editor trước
        self.create_status_bar()
        self.create_run_button()  # Tạo nút Run

        # Đảm bảo số dòng được cập nhật ngay sau khi tạo editor
        self.update_line_numbers()

    def create_menu(self):
        """Tạo thanh menu"""
        menubar = tk.Menu(self)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open File", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu Theme
        theme_menu = tk.Menu(menubar, tearoff=0)
        for theme in self.themes:
            theme_menu.add_command(label=theme, command=lambda t=theme: self.set_theme(t))
        menubar.add_cascade(label="Theme", menu=theme_menu)

        self.config(menu=menubar)

    def create_editor(self):
        """Tạo trình soạn thảo văn bản"""
        editor_frame = tk.Frame(self)
        editor_frame.pack(fill="both", expand=True)

        # Thanh số dòng
        self.line_numbers = tk.Text(editor_frame, width=4, bg="#f0f0f0", state="disabled", font=("Consolas", 12))
        self.line_numbers.pack(side="left", fill="y")

        # Tạo Text widget cho nội dung chính
        self.text_editor = tk.Text(editor_frame, wrap="none", undo=True, font=("Consolas", 12))
        self.text_editor.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        # Cuộn dọc và ngang
        y_scrollbar = tk.Scrollbar(editor_frame, orient="vertical", command=self.sync_scroll)
        x_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.text_editor.xview)
        self.text_editor.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

        # Sự kiện
        self.text_editor.bind("<KeyRelease>", self.on_key_release)  # Tô màu từ khóa khi gõ
        self.text_editor.bind("<KeyPress>", self.handle_bracket_completion)  # Hoàn thành dấu ngoặc
        self.text_editor.bind("<Return>", self.handle_enter)  # Thêm indent khi nhấn Enter
        self.text_editor.bind("<Up>", self.handle_move_up)  # Điều chỉnh indent khi di chuyển lên

    def create_status_bar(self):
        """Tạo thanh trạng thái"""
        self.status_bar = ttk.Label(self, text="Line: 1 | Column: 1", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # Cập nhật vị trí con trỏ
        self.text_editor.bind("<KeyRelease>", self.update_status_bar)
        self.text_editor.bind("<ButtonRelease>", self.update_status_bar)

    def create_run_button(self):
        """Tạo nút Run"""
        run_button = ttk.Button(self, text="Run", command=self.run_code)
        run_button.pack(side="bottom", pady=5)

    def update_status_bar(self, event=None):
        """Cập nhật dòng và cột trong thanh trạng thái"""
        cursor_position = self.text_editor.index("insert")
        line, column = cursor_position.split(".")
        self.status_bar.config(text=f"Line: {line} | Column: {int(column) + 1}")

    def update_line_numbers(self, event=None):
        """Cập nhật số dòng"""
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        line_count = int(self.text_editor.index("end-1c").split(".")[0])
        lines = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", lines)
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, *args):
        """Đồng bộ cuộn giữa thanh số dòng và nội dung chính"""
        self.line_numbers.yview(*args)
        self.text_editor.yview(*args)

    def handle_bracket_completion(self, event):
        """Tự động hoàn thành dấu ngoặc khi người dùng gõ dấu ngoặc mở"""
        char = event.char
        if char == '(':
            cursor_position = self.text_editor.index(tk.INSERT)

            # Chèn dấu ngoặc đóng tương ứng ngay sau dấu ngoặc mở
            self.text_editor.insert(cursor_position, ')')

            # Di chuyển con trỏ vào giữa dấu ngoặc
            new_cursor_position = self.text_editor.index(tk.INSERT + " - 1c")
            self.text_editor.mark_set(tk.INSERT, new_cursor_position)

    def handle_enter(self, event):
        """Thêm indent (4 khoảng trắng) khi nhấn Enter"""
        cursor_position = self.text_editor.index(tk.INSERT)

        # Lấy dòng hiện tại và kiểm tra nếu dòng này không rỗng
        line = self.text_editor.get(f"{cursor_position.split('.')[0]}.0", f"{cursor_position.split('.')[0]}.end")

        # Tính toán số spaces ở đầu dòng hiện tại
        indent_level = len(line) - len(line.lstrip(' '))  # Số khoảng trắng ở đầu dòng

        # Nếu dòng có dấu ":", tăng indent gấp đôi
        if ":" in line:
            indent_level = indent_level + 4  # Tăng thêm 4 spaces cho dấu ":"

        # Tạo mức indent cho dòng mới
        indent = " " * indent_level

        # Thêm indent cho dòng mới
        self.text_editor.insert(cursor_position, "\n" + indent)

        return "break"  # Ngừng hành động mặc định của Enter

    def handle_move_up(self, event):
        """Xử lý khi di chuyển lên trên và giảm mức indent nếu cần"""
        cursor_position = self.text_editor.index(tk.INSERT)
        line_number = int(cursor_position.split('.')[0])

        if line_number > 1:
            previous_line = self.text_editor.get(f"{line_number - 1}.0", f"{line_number - 1}.end")

            # Kiểm tra nếu dòng trước có dấu ':', giảm mức indent
            indent_level = previous_line.count(':')
            indent = "    " * indent_level

            # Di chuyển con trỏ đến dòng trước đó và điều chỉnh indent
            self.text_editor.insert(f"{line_number}.0", "\n" + indent)
            return "break"

    def highlight_keywords(self):
        """Tô màu từ khóa Python"""
        self.text_editor.tag_remove("keyword", "1.0", tk.END)

        # Lấy tất cả nội dung văn bản
        content = self.text_editor.get("1.0", tk.END)

        # Tìm và highlight từng từ khóa
        for keyword_item in keyword.kwlist:
            start_index = "1.0"
            while True:
                start_index = self.text_editor.search(rf"\b{keyword_item}\b", start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword_item)}c"
                self.text_editor.tag_add("keyword", start_index, end_index)
                start_index = end_index

        # Đảm bảo các từ khóa có thể được tô màu và in đậm
        self.text_editor.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))

    def on_key_release(self, event=None):
        """Tô màu từ khóa khi gõ"""
        self.highlight_keywords()

    def run_code(self):
        """Chạy mã Python từ Text widget"""
        code = self.text_editor.get("1.0", tk.END)

        try:
            exec(code)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_theme(self, theme_name):
        """Đổi theme của IDE"""
        theme = self.themes.get(theme_name)
        if theme:
            self.configure(bg=theme["bg"])
            self.text_editor.config(bg=theme["bg"], fg=theme["fg"])
            self.line_numbers.config(bg=theme["bg"], fg=theme["fg"])
            self.status_bar.config(bg=theme["bg"], fg=theme["fg"])
            self.current_theme = theme_name

    def new_file(self):
        """Tạo file mới"""
        self.text_editor.delete("1.0", tk.END)
        self.filename = None

    def open_file(self):
        """Mở file từ hệ thống"""
        file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r",encoding="utf-8") as file:
                code = file.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", code)
            self.filename = file_path

    def save_file(self):
        """Lưu file"""
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text_editor.get("1.0", tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        """Lưu file với tên mới"""
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            self.filename = file_path
            self.save_file()


if __name__ == "__main__":
    app = SimpleIDE()
    app.mainloop()
