from tkinter import Label, Menu, ttk
import tkinter as tk
import os
import tkinter
import time
import sys


class UI():
    def __init__(self, root) -> None:
        self.root = root
        self.countLine = 1
        self.currentTheme = "Light"




        self.Menu()
        self.textEditor()
        self.statusBar()

    def textEditor(self):
        mainframe = tk.Frame(self.root, background='blue')
        mainframe.pack(fill=tk.BOTH, expand=tk.TRUE)
        style = ttk.Style()
        style.configure("TScrollbar", troughcolor='lightgray', background='gray', arrowcolor='white')
        style.configure("Custom.Vertical.TScrollbar", troughcolor='lightblue', background='blue', arrowcolor='darkblue')

        self.columnLine = tk.Text(mainframe, width=3, bg="#f0f0f0", state="disabled", font=("Consolas", 12))
        self.columnLine.pack(side=tk.LEFT, fill=tk.Y)

        self.text_editor = tk.Text(mainframe, wrap="none", undo=True, font=("Consolas", 12))
        self.text_editor.pack(side="left", fill=tk.BOTH, expand=True)

        y_scrollbar = ttk.Scrollbar(self.text_editor, style="Custom.Vertical.TScrollbar", orient="vertical", cursor="Arrow", command=self.text_editor.yview)
        self.text_editor.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")

    # def sync_scroll(self, *args):
    #     """Đồng bộ cuộn giữa thanh số dòng và nội dung chính"""
    #     # self.line_numbers.yview(*args)
    #     self.text_editor.yview(*args)




    def statusBar(self):
        self.status_bar = tk.Label(self.root, text="Line: 1 Column: 1", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        self.text_editor.bind("<KeyRelease>", self.update_status_bar)
        self.text_editor.bind("<ButtonRelease>", self.update_status_bar)

    def update_status_bar(self, event=None):
        """Cập nhật dòng và cột trong thanh trạng thái"""

        cursor_position = self.text_editor.index("insert")
        Line, column = cursor_position.split(".")
        self.status_bar.config(text=f"Line: {Line} Column: {int(column) + 1}")




    def Menu(self):
        themes = {
            "Light": {"bg": "#ffffff", "fg": "#000000"},
            "Dark": {"bg": "#2b2b2b", "fg": "#ffffff"},
            "Solarized": {"bg": "#fdf6e3", "fg": "#000000"}
        }

        menubar = tk.Menu(self.root)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", accelerator="Ctrl+N")
        file_menu.add_command(label="Open file..", accelerator="Ctrl+O")
        file_menu.add_command(label="Open folder..")

        # submenu - smu
        smu_open_recent = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Open recent", menu=smu_open_recent)

        smu_open_recent.add_command(label="Reopen closed file", accelerator="Ctrl+Shift+T")
        smu_open_recent.add_separator()
        smu_open_recent.add_command(label='Path here')
        smu_open_recent.add_separator()
        smu_open_recent.add_command(label='Path here')
        smu_open_recent.add_separator()
        smu_open_recent.add_command(label='Clear items')

        smu_reopen_w_enc = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Reopen with encoding", menu=smu_reopen_w_enc)
        smu_reopen_w_enc.add_command(label="UTF")
        smu_reopen_w_enc.add_separator()
        smu_reopen_w_enc.add_command(label="encoding")
        smu_reopen_w_enc.add_separator()
        smu_reopen_w_enc.add_command(label="Hexademical")


        file_menu.add_command(label="Split view")
        file_menu.add_command(label="Save", accelerator="Ctrl+S")

        smu_save_w_enc = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Save with encoding", menu=smu_save_w_enc)
        smu_save_w_enc.add_command(label="UTF")
        smu_save_w_enc.add_separator()
        smu_save_w_enc.add_command(label="encoding")
        smu_save_w_enc.add_separator()
        smu_save_w_enc.add_command(label="Hexademical")

        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S")
        file_menu.add_command(label="Save all")
        file_menu.add_command(label="Print..")
        file_menu.add_separator()

        file_menu.add_command(label="New window", accelerator="Ctrl+Shift+N")
        file_menu.add_command(label="Close window", accelerator="Ctrl+Shift+W")
        file_menu.add_separator()

        file_menu.add_command(label="Close File", accelerator="Ctrl+W")
        file_menu.add_command(label="Reverse file")
        file_menu.add_command(label="Close all file")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Repeat", accelerator="Ctrl+Y")

        smu_u_s = Menu(file_menu, tearoff=0)
        edit_menu.add_cascade(label="Undo Selection", menu=smu_u_s)
        smu_u_s.add_command(label="Undo insert snippet", accelerator="Ctrl+U")
        smu_u_s.add_command(label="Soft redo", accelerator="Ctrl+Shift+U")
        edit_menu.add_separator()

        edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="Copy as HTML")
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        edit_menu.add_command(label="Paste and Indent", accelerator="Ctrl+Shift+V")
        edit_menu.add_command(label="Paste from History", accelerator="Ctrl+K,Ctrl+V")
        edit_menu.add_separator()

        smu_line = Menu(edit_menu, tearoff=0)
        edit_menu.add_cascade(label="Line", menu=smu_line)
        smu_line.add_command(label="Indent", accelerator="Ctrl+[")
        smu_line.add_command(label="Unindent", accelerator="Ctrl+]")
        smu_line.add_command(label="Reindent", accelerator="Ctrl+k,Ctrl+]")
        smu_line.add_command(label="Swap Line Up", accelerator="Ctrl+Shift+Up")
        smu_line.add_command(label="Swap Line Down", accelerator="Ctrl+Shift+Down")
        smu_line.add_command(label="Duplicate Line", accelerator="Ctrl+Shift+D")
        smu_line.add_command(label="Delete Line", accelerator="Ctrl+Shift+K")
        smu_line.add_command(label="Join Line", accelerator="Ctrl+Shift+J")

        smu_comment = Menu(edit_menu, tearoff=0)
        edit_menu.add_cascade(label="Commment", menu=smu_comment)
        smu_comment.add_command(label="Toggle Commment", accelerator="Ctrl+/")
        smu_comment.add_command(label="Toggle Block Commment", accelerator="Ctrl+Shift+/")

        smu_text = Menu(edit_menu, tearoff=0)
        edit_menu.add_cascade(label="Text")
        smu_text.add_command(label="Revert Hunk", accelerator="Ctrl+K,Ctrl+Z")
        smu_text.add_command(label="Revert Modification", accelerator="Ctrl+K,Ctrl+Shift+Z")
        smu_text.add_command(label="Revert Diff Hunk", accelerator="Ctrl+K,Ctrl+Shift+/")
        smu_text.add_command(label="", accelerator="")
        smu_text.add_command(label="", accelerator="")
        smu_text.add_command(label="", accelerator="")

        edit_menu.add_cascade(label="Tag")
        edit_menu.add_cascade(label="Mark")
        edit_menu.add_cascade(label="Code folding")
        edit_menu.add_cascade(label="Covert case")
        edit_menu.add_cascade(label="Wrap")
        edit_menu.add_command(label="Show completion", accelerator="Ctrl+Space")
        edit_menu.add_separator()



        edit_menu.add_command(label="Sort Line", accelerator="F9")
        edit_menu.add_command(label="Sort Line (Case sensitive)", accelerator="Ctrl+F9")
        edit_menu.add_cascade(label="Permutes Line")
        edit_menu.add_cascade(label="Permutes Selection")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        selection_menu = tk.Menu(menubar, tearoff=0)
        selection_menu.add_command(label="Split into lines", accelerator="Ctrl+Shift+L")
        selection_menu.add_command(label="Single Selection", accelerator="Escape")
        selection_menu.add_separator()

        selection_menu.add_command(label="Select all", accelerator="Ctrl+A")
        selection_menu.add_command(label="Expand Selection", accelerator="Ctrl+Shift+A")
        selection_menu.add_command(label="Expand Selection to lines", accelerator="Ctrl+L")
        selection_menu.add_command(label="Expand Selection to lines Upward", accelerator="Alt+L")
        selection_menu.add_command(label="Expand Selection to Block")
        selection_menu.add_command(label="Expand Selection to Paragraph")
        selection_menu.add_command(label="Expand Selection to Scope", accelerator="Ctrl+Shift+Space")
        selection_menu.add_command(label="Expand Selection to Brackets", accelerator="Ctrl+Shift+M")
        selection_menu.add_command(label="Expand Selection to Indentation")
        selection_menu.add_separator()

        selection_menu.add_command(label="Add previous Line", accelerator="Ctrl+Alt+Up")
        selection_menu.add_command(label="Add next Line", accelerator="Ctrl+Alt+Down")
        selection_menu.add_separator()

        selection_menu.add_cascade(label="Tab Selection")
        menubar.add_cascade(label="Selection", menu=selection_menu)



        find_menu = tk.Menu(menubar, tearoff=0)
        find_menu.add_command(label="Find...", accelerator="Ctrl+F")
        find_menu.add_command(label="Find next", accelerator="F3")
        find_menu.add_command(label="Find previous", accelerator="Shift+F3")
        find_menu.add_command(label="Incremental find", accelerator="Ctrl+I")
        find_menu.add_separator()

        find_menu.add_command(label="Replace", accelerator="Ctrl+H")
        find_menu.add_command(label="Replace next", accelerator="Ctrl+Shift+H")
        find_menu.add_separator()

        find_menu.add_command(label="Quick find", accelerator="Ctrl+F3")
        find_menu.add_command(label="Quick find all", accelerator="Alt+F3")
        find_menu.add_command(label="Quick add next", accelerator="Ctrt+D")
        find_menu.add_command(label="Quick skip next", accelerator="Ctrl+K,Ctrl+D")
        find_menu.add_separator()

        find_menu.add_command(label="Use selections for Find", accelerator="Ctrl+E")
        find_menu.add_command(label="Use selections for Replace", accelerator="Ctrl+Shift+F")
        find_menu.add_separator()

        find_menu.add_command(label="Find in files", accelerator="Ctrl+Shift+F")
        find_menu.add_cascade(label="Find result", accelerator="Ctrl+F")
        find_menu.add_command(label="Cancel find in files")
        menubar.add_cascade(label="Find", menu=find_menu)


        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_cascade(label="Side bar")
        view_menu.add_command(label="Hide minimap")
        view_menu.add_command(label="Hide Taps")
        view_menu.add_command(label="Hide status bar")
        view_menu.add_command(label="Hide menu")
        view_menu.add_command(label="Show console", accelerator="Ctrl+`")
        view_menu.add_separator()

        view_menu.add_command(label="Enter full screen", accelerator="F11")
        view_menu.add_command(label="Enter distraction free mode", accelerator="Shift+F11")
        view_menu.add_separator()

        view_menu.add_cascade(label="Layout")
        view_menu.add_cascade(label="Group")
        view_menu.add_cascade(label="Focus Group")
        view_menu.add_cascade(label="Move file to Group")
        view_menu.add_separator()

        view_menu.add_cascade(label="Systax")
        view_menu.add_cascade(label="Indentation")
        view_menu.add_cascade(label="Line endings")
        view_menu.add_separator()

        view_menu.add_command(label="Word wrap")
        view_menu.add_cascade(label="Word wrap column")
        view_menu.add_cascade(label="Ruler")
        view_menu.add_separator()

        view_menu.add_command(label="Spell check", accelerator="F6")
        view_menu.add_command(label="Next misspelling", accelerator="Ctrl+F6")
        view_menu.add_command(label="Prev misspelling", accelerator="Ctrl+Shift+F6")
        view_menu.add_cascade(label="Dictionary")
        menubar.add_cascade(label="View", menu=view_menu)


        goto_menu = tk.Menu(menubar, tearoff=0)
        goto_menu.add_command(label="Goto anything...", accelerator="Ctrl+P")
        goto_menu.add_separator()

        goto_menu.add_command(label="Goto symbol...", accelerator="Ctrl+R")
        goto_menu.add_command(label="Goto symbol in project", accelerator="Ctrl+Shift+R")
        goto_menu.add_command(label="Goto definition", accelerator="F12")
        goto_menu.add_command(label="Goto reference...", accelerator="Shift+F12")
        goto_menu.add_command(label="Goto Line...", accelerator="Ctrl+G")
        goto_menu.add_separator()

        goto_menu.add_command(label="Next Modification", accelerator="Ctrl+.")
        goto_menu.add_command(label="Prev Modification", accelerator="Ctrl+,")
        goto_menu.add_separator()

        goto_menu.add_command(label="Jump back", accelerator="Alt+-")
        goto_menu.add_command(label="Jump forward", accelerator="Shift+Alt+-")
        goto_menu.add_separator()

        goto_menu.add_cascade(label="Switch File")
        goto_menu.add_separator()

        goto_menu.add_cascade(label="Scroll")
        goto_menu.add_cascade(label="Bookmarks")
        goto_menu.add_separator()

        goto_menu.add_command(label="Jump to matching Bracket", accelerator="Ctrl+M")
        menubar.add_cascade(label="Goto", menu=goto_menu)


        tool_menu = tk.Menu(menubar, tearoff=0)
        tool_menu.add_command(label="Command palette", accelerator="Ctrl+P")
        tool_menu.add_command(label="Snippet")
        tool_menu.add_separator()

        tool_menu.add_cascade(label="Build system")
        tool_menu.add_command(label="Build", accelerator="Ctrl+B")
        tool_menu.add_command(label="Build with...", accelerator="Ctrl+Shift+B")
        tool_menu.add_command(label="Cancel build", accelerator="Ctrl+Break")
        tool_menu.add_cascade(label="Build result")
        tool_menu.add_checkbutton(label="Save all on build")
        tool_menu.add_separator()

        tool_menu.add_command(label="Record macro", accelerator="Ctrl+Q")
        tool_menu.add_command(label="Replay macro", accelerator="Ctrl+Shift+Q")
        tool_menu.add_command(label="Save macro...")
        tool_menu.add_cascade(label="Macros")
        tool_menu.add_separator()

        tool_menu.add_cascade(label="Developer")
        menubar.add_cascade(label="Tools", menu=tool_menu)


        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="Open project")
        project_menu.add_command(label="Switch project")
        project_menu.add_command(label="Quick Switch project", accelerator="Alt+Shift+P")
        project_menu.add_cascade(label="Open recent")
        project_menu.add_separator()

        project_menu.add_command(label="Save project as...")
        project_menu.add_command(label="Close project", state="disabled")
        project_menu.add_command(label="Edit project", state="disabled")
        project_menu.add_separator()

        project_menu.add_command(label="New workspace for project", state="disabled")
        project_menu.add_command(label="Save workspace as...")
        project_menu.add_separator()

        project_menu.add_command(label="Add folder in project")
        project_menu.add_command(label="Remove all folder from project")
        project_menu.add_command(label="Refresh folder")
        menubar.add_cascade(label="Project", menu=project_menu)


        preferences_menu = tk.Menu(menubar, tearoff=0)
        preferences_menu.add_command(label="Browse Packages")
        preferences_menu.add_separator()

        preferences_menu.add_command(label="Settings")
        preferences_menu.add_command(label="Settings - Systax specific")
        preferences_menu.add_command(label="Settings - Distaction Free")
        preferences_menu.add_separator()

        preferences_menu.add_command(label="Key Bindings")
        preferences_menu.add_command(label="Mouse Bindings")
        preferences_menu.add_separator()

        preferences_menu.add_command(label="Select Color Scheme")
        preferences_menu.add_command(label="Customize Color Scheme")
        preferences_menu.add_separator()

        preferences_menu.add_command(label="Select Theme")
        preferences_menu.add_command(label="Customize Theme")
        preferences_menu.add_separator()

        preferences_menu.add_cascade(label="Font")
        preferences_menu.add_cascade(label="Packages Setting")
        preferences_menu.add_command(label="Packages Control")


        menubar.add_cascade(label="Preferences", menu=preferences_menu)


        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentary")
        help_menu.add_command(label="Report a Bug")
        help_menu.add_command(label="Github")
        help_menu.add_separator()

        help_menu.add_command(label="Indexing status")
        help_menu.add_separator()

        help_menu.add_command(label=" Active License")
        help_menu.add_separator()


        help_menu.add_command(label="Check for Updates")
        help_menu.add_command(label="Changelog...")
        help_menu.add_command(label="License and Attribution")
        help_menu.add_command(label="About NapanIdle")

        menubar.add_cascade(label="Help", menu=help_menu)







        # theme_menu = tk.Menu(menubar, tearoff=0)
        # for theme in themes:
        #     theme_menu.add_command(label=theme)
        # menubar.add_cascade(label="Theme", menu=theme_menu)

        self.root.config(menu=menubar)


class LineNumberCanvas(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, width=40, bg="#1a1a2e", highlightthickness=0, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.schedule_redraw)
        self.text_widget.bind("<MouseWheel>", self.schedule_redraw)
        self.text_widget.bind("<ButtonRelease-1>", self.schedule_redraw)
        self.text_widget.bind("<Configure>", self.schedule_redraw)
        self.text_widget.bind("<FocusIn>", self.schedule_redraw)
        self.after_id = None

    def schedule_redraw(self, event=None):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(50, self.redraw)

    def redraw(self):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(35, y, anchor="ne", text=line_num, fill="#888", font=("Hack", 10))
            i = self.text_widget.index(f"{i}+1line")



if "__main__" == __name__:
    root = tkinter.Tk()
    title = os.path.abspath(__file__) + "- NapanIdle"


    root.title(title)
    root.minsize(800, 600)


    ui = UI(root)


    root.mainloop()


