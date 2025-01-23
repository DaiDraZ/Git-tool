import tkinter as tk
import keyword

def highlight_keywords(text_widget):
    """Tô màu các từ khóa đặc biệt trong Python"""
    # Xóa các tag đã được áp dụng trước đó
    text_widget.tag_remove("keyword", "1.0", tk.END)

    # Lấy tất cả nội dung văn bản
    content = text_widget.get("1.0", tk.END).splitlines()

    # Duyệt qua từng dòng của văn bản
    for i, line in enumerate(content):
        words = line.split()  # Chia dòng thành các từ riêng biệt
        for word in words:
            # Kiểm tra nếu từ là từ khóa Python
            if word in keyword.kwlist:
                start_index = f"{i+1}.{line.find(word)}"
                end_index = f"{i+1}.{line.find(word) + len(word)}"
                text_widget.tag_add("keyword", start_index, end_index)

    # Cấu hình tag "keyword" để thay đổi màu sắc và kiểu chữ
    text_widget.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))

def on_key_release(event, text_widget):
    """Gọi hàm highlight khi người dùng gõ phím"""
    highlight_keywords(text_widget)

def handle_bracket_completion(event, text_widget):
    """Tự động hoàn thành dấu ngoặc khi người dùng gõ dấu ngoặc mở"""
    char = event.char
    if char == '(':
        cursor_position = text_widget.index(tk.INSERT)
        
        # Chèn dấu ngoặc đóng tương ứng ngay sau dấu ngoặc mở
        text_widget.insert(cursor_position, ')')
        
        # Di chuyển con trỏ vào giữa dấu ngoặc
        new_cursor_position = text_widget.index(tk.INSERT + " - 1c")
        text_widget.mark_set(tk.INSERT, new_cursor_position)

def handle_enter(event, text_widget):
    """Thêm indent (4 khoảng trắng) khi nhấn Enter"""
    cursor_position = text_widget.index(tk.INSERT)
    
    # Lấy dòng hiện tại và kiểm tra nếu dòng này không rỗng
    line = text_widget.get(f"{cursor_position.split('.')[0]}.0", f"{cursor_position.split('.')[0]}.end")
    
    # Tính toán số spaces ở đầu dòng hiện tại
    indent_level = len(line) - len(line.lstrip(' '))  # Số khoảng trắng ở đầu dòng

    # Nếu dòng có dấu ":", tăng indent gấp đôi
    if ":" in line:
        indent_level = indent_level + 4  # Tăng thêm 4 spaces cho dấu ":"

    # Tạo mức indent cho dòng mới
    indent = " " * indent_level

    # Thêm indent cho dòng mới
    text_widget.insert(cursor_position, "\n" + indent)
    
    return "break"  # Ngừng hành động mặc định của Enter

def handle_move_up(event, text_widget):
    """Xử lý khi di chuyển lên trên và giảm mức indent nếu cần"""
    cursor_position = text_widget.index(tk.INSERT)
    line_number = int(cursor_position.split('.')[0])
    
    if line_number > 1:
        previous_line = text_widget.get(f"{line_number - 1}.0", f"{line_number - 1}.end")
        
        # Kiểm tra nếu dòng trước có dấu ':', giảm mức indent
        indent_level = previous_line.count(':')
        indent = "    " * indent_level
        
        # Di chuyển con trỏ đến dòng trước đó và điều chỉnh indent
        text_widget.insert(f"{line_number}.0", "\n" + indent)
        return "break"

# Tạo một cửa sổ Tkinter
root = tk.Tk()
root.title("Bracket Completion and Highlight Keywords")
root.geometry("600x400")

# Tạo widget Text để nhập nội dung
text_widget = tk.Text(root, wrap="none", font=("Consolas", 12))
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

# Bind sự kiện gõ phím để highlight từ khóa và tự động hoàn thành dấu ngoặc
text_widget.bind("<KeyRelease>", lambda event: on_key_release(event, text_widget))
text_widget.bind("<KeyPress>", lambda event: handle_bracket_completion(event, text_widget))

# Bind sự kiện Enter để thêm indent
text_widget.bind("<Return>", lambda event: handle_enter(event, text_widget))

# Bind sự kiện di chuyển lên trên
text_widget.bind("<Up>", lambda event: handle_move_up(event, text_widget))

# Khởi chạy giao diện người dùng
root.mainloop()
