import tkinter as tk
import keyword

def highlight_keywords(text_widget):
    # Delete tag before 
    text_widget.tag_remove("keyword", "1.0", tk.END)

    # Get all code
    content = text_widget.get("1.0", tk.END).splitlines()

    # review each line of Code
    for i, line in enumerate(content):
        words = line.split()
        for word in words:
            # Check python tag
            if word in keyword.kwlist:
                start_index = f"{i+1}.{line.find(word)}"
                end_index = f"{i+1}.{line.find(word) + len(word)}"
                text_widget.tag_add("keyword", start_index, end_index)

    # Change color tag
    text_widget.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))

def on_key_release(event, text_widget):
    highlight_keywords(text_widget)

def handle_bracket_completion(event, text_widget):
    """Auto completion close braket ..."""
    char = event.char
    if char == '(':
        cursor_position = text_widget.index(tk.INSERT)
        text_widget.insert(cursor_position, ')')
        new_cursor_position = text_widget.index(tk.INSERT + " - 1c")
        text_widget.mark_set(tk.INSERT, new_cursor_position)

def handle_enter(event, text_widget):
    """Add 4 space"""
    cursor_position = text_widget.index(tk.INSERT)
    
    # check empty lines
    line = text_widget.get(f"{cursor_position.split('.')[0]}.0", f"{cursor_position.split('.')[0]}.end")
    
    # calc left space numbers
    indent_level = len(line) - len(line.lstrip(' '))  # Số khoảng trắng ở đầu dòng

    # if line have ":",
    if ":" in line:
        indent_level = indent_level + 4  # Tăng thêm 4 spaces cho dấu ":"

    indent = " " * indent_level
    text_widget.insert(cursor_position, "\n" + indent)
    
    return "break"

def handle_move_up(event, text_widget):
    """Xử lý khi di chuyển lên trên và giảm mức indent nếu cần"""
    cursor_position = text_widget.index(tk.INSERT)
    line_number = int(cursor_position.split('.')[0])
    
    if line_number > 1:
        previous_line = text_widget.get(f"{line_number - 1}.0", f"{line_number - 1}.end")
        indent_level = previous_line.count(':')
        indent = " " * indent_level * 4
        text_widget.insert(f"{line_number}.0", "\n" + indent)
        return "break"

root = tk.Tk()
root.title("Bracket Completion and Highlight Keywords")
root.geometry("600x400")

# Creat coding space
text_widget = tk.Text(root, wrap="none", font=("Consolas", 12))
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

# Call event
text_widget.bind("<KeyRelease>", lambda event: on_key_release(event, text_widget))

text_widget.bind("<KeyPress>", lambda event: handle_bracket_completion(event, text_widget))

text_widget.bind("<Return>", lambda event: handle_enter(event, text_widget))

text_widget.bind("<Up>", lambda event: handle_move_up(event, text_widget))

# Khởi chạy giao diện người dùng
root.mainloop()
