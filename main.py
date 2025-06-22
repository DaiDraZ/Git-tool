import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser


def run_git_command(args: list[str]):
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        return "Git is not installed or not available in the system."


def git_init():
    output = run_git_command(["init"])
    output_text.set(output)


def git_status():
    output = run_git_command(["status"])
    output_text.set(output)


def git_add():
    file_path = filedialog.askopenfilename(title="Chọn tệp để thêm vào Git")
    if file_path:
        output = run_git_command(["add", file_path])
        output_text.set(output)
    else:
        messagebox.showwarning("Lỗi", "Không có tệp nào được chọn.")


def git_commit():
    def commit_action():
        message = commit_message.get()
        if message:
            output = run_git_command(["commit", "-m", message])
            output_text.set(output)
            commit_window.destroy()
        else:
            messagebox.showwarning("Lỗi", "Thông điệp commit không được để trống.")

    commit_window = tk.Toplevel(root)
    commit_window.title("Tạo Commit")
    commit_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(commit_window, text="Nhập commit message:").pack(pady=5)
    commit_message = ttk.Entry(commit_window, width=40)
    commit_message.pack(pady=5)
    tk.Button(commit_window, text="Commit", command=commit_action).pack(pady=10)


def git_branch():
    def branch_action():
        branch_name = branch_input.get()
        if branch_name:
            output = run_git_command(["branch", branch_name])
            output_text.set(output)
            branch_window.destroy()
        else:
            messagebox.showwarning("Lỗi", "Tên nhánh không được để trống.")

    branch_window = tk.Toplevel(root)
    branch_window.title("Tạo nhánh mới")
    branch_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(branch_window, text="Tên nhánh mới:").pack(pady=5)
    branch_input = ttk.Entry(branch_window, width=40)
    branch_input.pack(pady=5)
    tk.Button(branch_window, text="Tạo nhánh", command=branch_action).pack(pady=10)


def git_checkout():
    def checkout_action():
        branch_name = branch_input.get()
        if branch_name:
            output = run_git_command(["checkout", branch_name])
            output_text.set(output)
            checkout_window.destroy()
        else:
            messagebox.showwarning("Lỗi", "Tên nhánh không được để trống.")

    checkout_window = tk.Toplevel(root)
    checkout_window.title("Chuyển nhánh")
    checkout_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(checkout_window, text="Tên nhánh muốn chuyển tới:").pack(pady=5)
    branch_input = ttk.Entry(checkout_window, width=40)
    branch_input.pack(pady=5)
    tk.Button(checkout_window, text="Chuyển", command=checkout_action).pack(pady=10)


def git_merge():
    def merge_action():
        branch_name = branch_input.get()
        if branch_name:
            output = run_git_command(["merge", branch_name])
            output_text.set(output)
            merge_window.destroy()
        else:
            messagebox.showwarning("Lỗi", "Tên nhánh không được để trống.")

    merge_window = tk.Toplevel(root)
    merge_window.title("Merge nhánh")
    merge_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(merge_window, text="Tên nhánh muốn merge:").pack(pady=5)
    branch_input = ttk.Entry(merge_window, width=40)
    branch_input.pack(pady=5)
    tk.Button(merge_window, text="Merge", command=merge_action).pack(pady=10)


class LogoStartApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="white")
        self.animation_ids = []

        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=300, highlightthickness=0)
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="Đang khởi động", font=("Arial", 14), bg="white")
        self.status_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.show_splash()

    def show_splash(self):
        try:
            img = Image.open("..\\Git tool\\github.png")
            img = img.resize((200, 200), Image.Resampling.LANCZOS).convert("RGBA")
            self.fade_in_logo(img)
        except Exception:
            self.status_label.config(text="Không tìm thấy logo!", fg="red")

        self.animate_dots()
        self.update_progress_bar(0)
        self.root.after(2000, self.load_main_content)

    def fade_in_logo(self, img, alpha=0.0, step=0.05):
        if alpha > 1.0:
            return

        img_with_alpha = img.copy()
        img_with_alpha.putalpha(int(alpha * 255))
        logo = ImageTk.PhotoImage(img_with_alpha)

        self.canvas.delete("logo")
        self.canvas.create_image(300, 150, image=logo, tags="logo")
        self.canvas.image = logo

        anim_id = self.root.after(50, self.fade_in_logo, img, alpha + step)
        self.animation_ids.append(anim_id)

    def animate_dots(self, count=0):
        dots = "." * (count % 4)
        self.status_label.config(text=f"Github đang khởi động {dots}")
        anim_id = self.root.after(500, self.animate_dots, count + 1)
        self.animation_ids.append(anim_id)

    def update_progress_bar(self, value):
        if value <= 100:
            self.progress_bar["value"] = value
            anim_id = self.root.after(30, self.update_progress_bar, value + 1)
            self.animation_ids.append(anim_id)

    def load_main_content(self):
        for anim_id in self.animation_ids:
            self.root.after_cancel(anim_id)

        main_frame.destroy()
        UserConfig(root)


class UserConfig(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        tk.Label(self, text="Github settings", font="Arial 20 bold").pack(anchor='center')

        ttk.Label(self, text="user.name").place(relx=0.25, rely=0.35)
        self.name_box = ttk.Entry(self, width=35, font='Arial')
        self.name_box.place(relx=0.35, rely=0.35)

        ttk.Label(self, text="user.email").place(relx=0.25, rely=0.45)
        self.email_box = ttk.Entry(self, width=35, font='Arial')
        self.email_box.place(relx=0.35, rely=0.45)

        tk.Button(self, text="Next", width=5, command=self.add_ssh_key).place(relx=0.65, rely=0.55)
        tk.Button(self, text="Cancel", width=5, command=root.quit).place(relx=0.55, rely=0.55)

        self.pack(expand=True, fill="both")

    def add_ssh_key(self):
        try:
            webbrowser.open("https://github.com/settings/keys")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở trình duyệt: {e}")


def starting_app():
    output_label.pack(fill="x", pady=5)
    output_box.pack(fill="both", expand=True, padx=10, pady=5)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Git Init", command=git_init, width=20).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Git Status", command=git_status, width=20).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Add File", command=git_add, width=20).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Commit", command=git_commit, width=20).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Create Branch", command=git_branch, width=20).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Checkout Branch", command=git_checkout, width=20).grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Merge Branch", command=git_merge, width=20).grid(row=3, column=0, padx=5, pady=5)


# Start Application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Git Tool")
    root.geometry("800x600")
    root.iconbitmap('..\\Git tool\\github.ico')

    output_text = tk.StringVar()
    output_text.set("Chào bạn! Hãy ghé repo mình tại:\nhttps://github.com/DaiDraZ/Git_Tool")

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill="both")

    output_label = tk.Label(main_frame, text="Git Output:", anchor="w")
    output_box = tk.Label(main_frame, textvariable=output_text, bg="black", fg="green", anchor="nw", justify="left", font="Arial 14")
    button_frame = tk.Frame(main_frame)

    LogoStartApp(main_frame)

    root.mainloop()
