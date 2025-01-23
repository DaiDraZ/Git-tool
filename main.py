import subprocess,os
import tkinter as tk
from tkinter import FALSE, ttk
from tkinter import filedialog, messagebox
from tkinter import font
from PIL import Image, ImageTk
import time
import webview


def run_git_command(args: list[str]):
    try:
        result = subprocess.run(
            ["git"] + args, 
            capture_output=True, 
            text=True
        )
        output = result.stdout + result.stderr
        return output
    except FileNotFoundError:
        return "Git does not installed or not available on the system."
def ssh_command():
    pass

# Git method


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
        messagebox.showwarning("Error", "")


def git_commit():
    def commit_action():
        message = commit_message.get()
        if message:
            output = run_git_command(["commit", "-m", message])
            output_text.set(output)
            commit_window.destroy()
        else:
            messagebox.showwarning("Error", "Message should not empty")

    commit_window = tk.Toplevel(root)
    commit_window.title("Creat commit")
    # commit_window.iconphoto(False, github_icon) 
    commit_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(commit_window, text="Type commit messaging : ").pack(pady=5)
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
            messagebox.showwarning("Error", "Branch name does not empty !!!")

    branch_window = tk.Toplevel(root)
    branch_window.title("Creat new branch")
    # branch_window.iconphoto(False, github_icon) 
    branch_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(branch_window, text="New branch name : ").pack(pady=5)
    branch_input = ttk.Entry(branch_window, width=40)
    branch_input.pack(pady=5)
    tk.Button(branch_window, text="Creat branch", command=branch_action).pack(pady=10)


def git_checkout():
    def checkout_action():
        branch_name = branch_input.get()
        if branch_name:
            output = run_git_command(["checkout", branch_name])
            output_text.set(output)
            checkout_window.destroy()
        else:
            messagebox.showwarning("Error", "Branch name shouldn't empty")

    checkout_window = tk.Toplevel(root)
    checkout_window.title("Switch branch")
    # checkout_window.iconphoto(False, github_icon) 
    checkout_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(checkout_window, text="Type new branch name to switch :").pack(pady=5)
    branch_input = ttk.Entry(checkout_window, width=40)
    branch_input.pack(pady=5)
    tk.Button(checkout_window, text="switch", command=checkout_action).pack(pady=10)


def git_merge():
    def merge_action():
        branch_name = branch_input.get()
        if branch_name:
            output = run_git_command(["merge", branch_name])
            output_text.set(output)
            merge_window.destroy()
        else:
            messagebox.showwarning("Error", "Branch name shouldn't not empty")

    merge_window = tk.Toplevel(root)
    merge_window.title("Merge branch")
    # merge_window.iconphoto(False, github_icon) 
    merge_window.iconbitmap('..\\Git tool\\github.ico')
    tk.Label(merge_window, text="Name branch to merge : ").pack(pady=5)
    branch_input = tk.Entry(merge_window, width=40)

    branch_input.pack(pady=5)
    tk.Button(merge_window, text="Merge", command=merge_action).pack(pady=10)



def git_config(options : int):

    pass



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
            self.fade_in_logo(img, alpha=0)  
        except Exception:
            self.status_label.config(text="Logo not found !", fg="red")

        self.animate_dots()
        self.update_progress_bar(0)
        self.root.after(2000, self.load_main_content)

    def fade_in_logo(self, img, alpha, step=0.05):
        if alpha <= 1.0:
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
        self.status_label.config(text=f"Github begin starting {dots}")
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
        
        User_config(root)
        # starting_app()


class User_config(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root)

        self.title = tk.Label(self,text="Github settings",font="Arial 20 bold")
        self.title.pack(anchor='center')

        self.name_label = ttk.Label(self,text="user.name")
        self.name_label.place(relx=0.25,rely=0.35)
        self.name_box = ttk.Entry(self,width=35,font='Arial')
        self.name_box.place(relx=0.35,rely=0.35)

        self.email_label = ttk.Label(self,text="user.email")
        self.email_label.place(relx=0.25,rely=0.45)
        self.name_box = ttk.Entry(self,width=35,font='Arial')
        self.name_box.place(relx=0.35,rely=0.45)


        self.login_btn = tk.Button(self,width=5,text="Next",command=self.open_browser)
        self.login_btn.place(relx=0.65,rely=0.55)

        self.cancel_btn = tk.Button(self,text="Cancel",width=5)
        self.cancel_btn.place(relx=0.55,rely=0.55)

        self.pack(expand=True,fill="both")

        

    def add_ssh_key(self):
        try:
            result = os.system("start chrome https://github.com/settings/keys")
        except FileNotFoundError:
            return "Git does not installed or not available on the system."
    
    def open_browser(self):
        # window.set_icon('..\\Git tool\\github.png')
        window = webview.create_window(
            title="Add SSH Key to your GitHub",
            url="https://github.com/settings/keys",
            width=self.winfo_width(),
            height=self.winfo_height(),
            fullscreen=False,
            confirm_close=True
        )
        webview.start(debug=False)
        window.create_confirmation_dialog(title="Warning !",message="Are you add SSH_KEY ? if you dont,please add ssh_key in your github or generation key again !",)

def starting_app():
    output_label.pack(fill="x", pady=5)
    output_box.pack(fill="both", expand=True, padx=10, pady=5)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Khởi tạo Git (init)", command=git_init, width=20).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Trạng thái (status)", command=git_status, width=20).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Thêm tệp (add)", command=git_add, width=20).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Tạo Commit", command=git_commit, width=20).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Tạo nhánh mới (branch)", command=git_branch, width=20).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Chuyển nhánh (checkout)", command=git_checkout, width=20).grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Merge nhánh", command=git_merge, width=20).grid(row=3, column=0, padx=5, pady=5)

class frame_config(tk.Frame):
    def __init__(self,root) -> None:
        super.__init__(root)



# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True,fill="both")

    LogoStartApp(main_frame)

    root.title("Git Tool")
    root.geometry("600x400")
    root.minsize(800, 600)
    # github_icon = tk.PhotoImage(file='..\\Git tool\\github.png')
    root.iconbitmap('..\\Git tool\\github.ico') 

    # Screen log
    output_text = tk.StringVar()
    output_text.set("Welcome guy, hope you like my tool. Can you give me 1 star in \n https://github.com/DaiDraZ/Git_Tool .Thank you ")
    output_label = tk.Label(main_frame, text="Log command :", anchor="w")

    output_box = tk.Label(main_frame, textvariable=output_text, bg="black", fg="green", bd=1, relief="raised", anchor="nw", justify="left", font="Arial 14")

    # Button 
    button_frame = tk.Frame(main_frame)

    root.mainloop()
