import tkinter as tk
import keyword


def highlight_keywords(text_widget):
    """Tô màu các từ khóa Python"""
    text_widget.tag_remove("keyword", "1.0", tk.END)
    content = text_widget.get("1.0", tk.END).splitlines()

    for i, line in enumerate(content):
        words = line.split()
        for word in words:
            if word in keyword.kwlist:
                start_index = f"{i+1}.{line.find(word)}"
                end_index = f"{i+1}.{line.find(word) + len(word)}"
                text_widget.tag_add("keyword", start_index, end_index)

    text_widget.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))


def on_key_release(event, text_widget):
    """Kích hoạt tô màu từ khóa khi gõ phím"""
    highlight_keywords(text_widget)


def handle_bracket_completion(event, text_widget):
    """Tự động thêm dấu đóng khi nhập ngoặc mở"""
    if event.char == '(':
        cursor_position = text_widget.index(tk.INSERT)
        text_widget.insert(cursor_position, ')')
        text_widget.mark_set(tk.INSERT, f"{cursor_position} - 1c")


def handle_enter(event, text_widget):
    """Tự động thụt dòng khi nhấn Enter"""
    cursor_position = text_widget.index(tk.INSERT)
    line_index = cursor_position.split('.')[0]
    line = text_widget.get(f"{line_index}.0", f"{line_index}.end")

    indent_level = len(line) - len(line.lstrip(' '))
    if ":" in line:
        indent_level += 4

    indent = " " * indent_level
    text_widget.insert(cursor_position, "\n" + indent)
    return "break"


# Giao diện chính
root = tk.Tk()
root.title("Python Editor - Highlight & Auto-Indent")
root.geometry("600x400")

text_widget = tk.Text(root, wrap="none", font=("Consolas", 12))
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

# Gán sự kiện
text_widget.bind("<KeyRelease>", lambda event: on_key_release(event, text_widget))
text_widget.bind("<KeyPress>", lambda event: handle_bracket_completion(event, text_widget))
text_widget.bind("<Return>", lambda event: handle_enter(event, text_widget))

# Chạy ứng dụng
root.mainloop()
