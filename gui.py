"""
HEIC to PNG Converter - Modern GUI Application
Enhanced for Crisp High-DPI Display, Responsive Layout, Clear Typography,
and Full Bilingual (Traditional Chinese & English) Internationalization.
"""

import os
import sys
import queue
import threading
from pathlib import Path
from typing import List, Set

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Windows High-DPI Awareness (Per-Monitor V2 for ultra-crisp ClearType rendering)
try:
    import ctypes
    # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 (-4) is the sharpest mode on Win 10/11
    ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except Exception:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Drag and Drop support
HAS_DND = False
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except Exception:
    pass

import converter
import i18n


def format_size(bytes_num: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"


class HEICConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root

        # Language state (auto-detected system language: 'zh' or 'en')
        self.lang = i18n.detect_system_language()

        self.root.title(self.t("app_title"))

        # Determine base directory (support both PyInstaller bundle and script)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.base_dir = Path(sys._MEIPASS)
        else:
            self.base_dir = Path(__file__).resolve().parent

        self.ico_path = self.base_dir / "assets" / "heic_app.ico"
        self.icon_72_path = self.base_dir / "assets" / "app_icon_72.png"
        self.icon_master_path = self.base_dir / "assets" / "app_icon.png"

        self.app_icon_photo = None
        if self.icon_72_path.exists():
            try:
                # Composite onto exact background color (#F8FAFC) for flawless anti-aliased edges without white border
                bg_rgb = (248, 250, 252)
                icon_img = Image.open(str(self.icon_72_path)).convert("RGBA")
                composited_header = Image.new("RGB", icon_img.size, bg_rgb)
                composited_header.paste(icon_img, (0, 0), icon_img)
                self.app_icon_photo = ImageTk.PhotoImage(composited_header)

                # Set taskbar/window icon using true alpha PNG
                self.root.iconphoto(True, ImageTk.PhotoImage(icon_img))
            except Exception:
                pass

        if self.ico_path.exists():
            try:
                self.root.iconbitmap(str(self.ico_path))
            except Exception:
                pass

        # Responsive window sizing & screen centering
        window_w = 980
        window_h = 700
        min_w = 750
        min_h = 500
        self.root.minsize(min_w, min_h)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        pos_x = max(0, (sw - window_w) // 2)
        pos_y = max(0, (sh - window_h) // 2)
        self.root.geometry(f"{window_w}x{window_h}+{pos_x}+{pos_y}")

        # Font configuration - Prioritize Microsoft JhengHei UI for sharp, clear CJK & Latin rendering
        self.font_family = "Microsoft JhengHei UI"
        self.font_title = (self.font_family, 15, "bold")
        self.font_subtitle = (self.font_family, 9)
        self.font_body = (self.font_family, 10)
        self.font_body_bold = (self.font_family, 10, "bold")
        self.font_button = (self.font_family, 10, "bold")
        self.font_small = (self.font_family, 9)

        # Style configuration
        self.setup_styles()

        # State
        self.file_list: List[str] = []
        self.file_set: Set[str] = set()
        self.is_converting = False
        self.should_cancel = False
        self.msg_queue = queue.Queue()
        self.last_output_dir = ""

        # UI Layout
        self.create_widgets()

        # Thread-safe UI update poller
        self.root.after(100, self.process_queue)

    def t(self, key: str, **kwargs) -> str:
        """Helper to get translated string for current language."""
        return i18n.t(key, lang=self.lang, **kwargs)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Modern Crisp Palette
        self.bg_color = "#F8FAFC"        # Slate 50
        self.card_bg = "#FFFFFF"         # White
        self.text_color = "#0F172A"      # Slate 900 (High contrast)
        self.text_muted = "#64748B"      # Slate 500
        self.primary_blue = "#2563EB"    # Blue 600
        self.border_gray = "#CBD5E1"     # Slate 300

        self.root.configure(bg=self.bg_color)

        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg)

        # Labels
        style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=self.font_body
        )
        style.configure(
            "Muted.TLabel",
            background=self.bg_color,
            foreground=self.text_muted,
            font=self.font_subtitle
        )
        style.configure(
            "Title.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=self.font_title
        )

        # Buttons
        style.configure(
            "Primary.TButton",
            font=self.font_button,
            padding=(16, 8),
            background=self.primary_blue,
            foreground="#FFFFFF"
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("disabled", "#94A3B8")],
            foreground=[("disabled", "#F1F5F9")]
        )

        style.configure(
            "Secondary.TButton",
            font=self.font_body,
            padding=(10, 6)
        )

        # Treeview (Table) Styling for maximum clarity
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=self.font_body,
            borderwidth=1,
            relief="solid"
        )
        style.configure(
            "Treeview.Heading",
            font=self.font_body_bold,
            foreground="#0F172A",
            background="#F1F5F9",
            padding=(8, 6),
            relief="flat"
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#E2E8F0")]
        )
        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1E40AF")]
        )

        # Progressbar
        style.configure("Horizontal.TProgressbar", thickness=10)

    def create_widgets(self):
        """
        Builds the entire UI with responsive docking:
        1. Top: Header with Brand Icon & Language Switcher
        2. Top: Drop Zone (side=TOP)
        3. Bottom: Action Buttons & Progress (side=BOTTOM)
        4. Bottom: Settings Card (side=BOTTOM)
        5. Center: File List Table (expand=True, fill=BOTH)
        """

        # ----------------------------------------------------------------------
        # 1. Top Section: Header with Brand Icon & Language Selector
        # ----------------------------------------------------------------------
        header_frame = ttk.Frame(self.root, padding="18 14 18 8")
        header_frame.pack(side=tk.TOP, fill=tk.X)

        if self.app_icon_photo:
            icon_lbl = tk.Label(header_frame, image=self.app_icon_photo, bg=self.bg_color)
            icon_lbl.pack(side=tk.LEFT, padx=(0, 14), anchor=tk.CENTER)

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.title_lbl = ttk.Label(title_box, text=self.t("app_title"), style="Title.TLabel")
        self.title_lbl.pack(anchor=tk.W)

        self.sub_lbl = ttk.Label(
            title_box,
            text=self.t("app_subtitle"),
            style="Muted.TLabel"
        )
        self.sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Language Selector (Top Right)
        lang_box = ttk.Frame(header_frame)
        lang_box.pack(side=tk.RIGHT, anchor=tk.E, padx=(10, 0))

        self.lang_box_lbl = ttk.Label(lang_box, text="🌐", font=(self.font_family, 11))
        self.lang_box_lbl.pack(side=tk.LEFT, padx=(0, 4))

        self.lang_var = tk.StringVar(value="繁體中文" if self.lang == "zh" else "English")
        self.lang_combo = ttk.Combobox(
            lang_box,
            textvariable=self.lang_var,
            values=["繁體中文", "English"],
            state="readonly",
            width=9,
            font=self.font_small
        )
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_lang_changed)

        # ----------------------------------------------------------------------
        # 2. Top Section: Drop Zone & Fast Action Buttons
        # ----------------------------------------------------------------------
        drop_container = ttk.Frame(self.root, padding="18 0 18 10")
        drop_container.pack(side=tk.TOP, fill=tk.X)

        self.drop_frame = tk.Frame(
            drop_container,
            bg="#EFF6FF",
            highlightbackground="#93C5FD",
            highlightthickness=2,
            relief="flat",
            cursor="hand2"
        )
        self.drop_frame.pack(fill=tk.X, ipady=8)

        drop_hint = self.t("drop_hint_dnd" if HAS_DND else "drop_hint_nodnd")
        self.drop_lbl = tk.Label(
            self.drop_frame,
            text=drop_hint,
            bg="#EFF6FF",
            fg="#1E40AF",
            font=self.font_body_bold
        )
        self.drop_lbl.pack(pady=(4, 6))

        btn_box = tk.Frame(self.drop_frame, bg="#EFF6FF")
        btn_box.pack(pady=(0, 4))

        self.add_files_btn = ttk.Button(
            btn_box,
            text=self.t("btn_add_files"),
            command=self.choose_files,
            style="Secondary.TButton"
        )
        self.add_files_btn.pack(side=tk.LEFT, padx=6)

        self.add_folder_btn = ttk.Button(
            btn_box,
            text=self.t("btn_add_folder"),
            command=self.choose_folder,
            style="Secondary.TButton"
        )
        self.add_folder_btn.pack(side=tk.LEFT, padx=6)

        self.clear_btn = ttk.Button(
            btn_box,
            text=self.t("btn_clear"),
            command=self.clear_list,
            style="Secondary.TButton"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=6)

        # Drag & drop binding
        if HAS_DND:
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
            self.drop_lbl.drop_target_register(DND_FILES)
            self.drop_lbl.dnd_bind('<<Drop>>', self.on_drop)

        self.drop_frame.bind("<Button-1>", lambda e: self.choose_files())
        self.drop_lbl.bind("<Button-1>", lambda e: self.choose_files())

        # ----------------------------------------------------------------------
        # 3. Bottom Section: Action Bar & Progress (DOCK TO BOTTOM FIRST)
        # ----------------------------------------------------------------------
        action_container = ttk.Frame(self.root, padding="18 8 18 16")
        action_container.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            action_container,
            variable=self.progress_var,
            maximum=100,
            style="Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 8))

        # Bottom row with status on left, buttons on right
        bottom_row = ttk.Frame(action_container)
        bottom_row.pack(fill=tk.X)

        self.status_lbl = ttk.Label(
            bottom_row,
            text=self.t("status_ready"),
            font=self.font_body
        )
        self.status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Right-aligned buttons
        self.format_var = tk.StringVar(value="PNG")

        self.start_btn = ttk.Button(
            bottom_row,
            text=self.t("btn_start", fmt=self.format_var.get()),
            command=self.start_conversion,
            style="Primary.TButton"
        )
        self.start_btn.pack(side=tk.RIGHT, padx=(8, 0))

        self.cancel_btn = ttk.Button(
            bottom_row,
            text=self.t("btn_cancel"),
            command=self.cancel_conversion,
            style="Secondary.TButton",
            state="disabled"
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=(8, 0))

        self.open_output_btn = ttk.Button(
            bottom_row,
            text=self.t("btn_open_output"),
            command=self.open_output_folder,
            style="Secondary.TButton",
            state="disabled"
        )
        self.open_output_btn.pack(side=tk.RIGHT)

        # ----------------------------------------------------------------------
        # 4. Bottom Section: Settings Card (DOCK ABOVE ACTION BAR)
        # ----------------------------------------------------------------------
        settings_container = ttk.Frame(self.root, padding="18 0 18 6")
        settings_container.pack(side=tk.BOTTOM, fill=tk.X)

        self.settings_box = tk.LabelFrame(
            settings_container,
            text=self.t("settings_title"),
            font=self.font_body_bold,
            bg=self.card_bg,
            fg="#1E293B",
            relief="groove",
            bd=1,
            padx=14,
            pady=10
        )
        self.settings_box.pack(fill=tk.X)

        # Row 1: Output Directory configuration
        row1 = tk.Frame(self.settings_box, bg=self.card_bg)
        row1.pack(fill=tk.X, pady=(0, 6))

        self.dest_mode_var = tk.StringVar(value="same")
        self.custom_dir_var = tk.StringVar(value="")

        self.lbl_output_dir = tk.Label(
            row1,
            text=self.t("lbl_output_dir"),
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body_bold
        )
        self.lbl_output_dir.pack(side=tk.LEFT)

        self.rb_same = tk.Radiobutton(
            row1,
            text=self.t("rb_same_dir"),
            variable=self.dest_mode_var,
            value="same",
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body,
            activebackground=self.card_bg,
            command=self.toggle_dest_mode
        )
        self.rb_same.pack(side=tk.LEFT, padx=(4, 16))

        self.rb_custom = tk.Radiobutton(
            row1,
            text=self.t("rb_custom_dir"),
            variable=self.dest_mode_var,
            value="custom",
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body,
            activebackground=self.card_bg,
            command=self.toggle_dest_mode
        )
        self.rb_custom.pack(side=tk.LEFT, padx=(0, 4))

        self.dest_entry = ttk.Entry(
            row1,
            textvariable=self.custom_dir_var,
            state="disabled",
            font=self.font_body
        )
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        self.dest_browse_btn = ttk.Button(
            row1,
            text=self.t("btn_browse"),
            command=self.browse_custom_dir,
            state="disabled",
            style="Secondary.TButton"
        )
        self.dest_browse_btn.pack(side=tk.LEFT, padx=(4, 0))

        # Row 2: Target format and options
        row2 = tk.Frame(self.settings_box, bg=self.card_bg)
        row2.pack(fill=tk.X, pady=(4, 0))

        self.lbl_target_format = tk.Label(
            row2,
            text=self.t("lbl_target_format"),
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body_bold
        )
        self.lbl_target_format.pack(side=tk.LEFT)

        for fmt in ["PNG", "JPG", "WEBP"]:
            rb = tk.Radiobutton(
                row2,
                text=fmt,
                variable=self.format_var,
                value=fmt,
                bg=self.card_bg,
                fg=self.text_color,
                font=self.font_body,
                activebackground=self.card_bg
            )
            rb.pack(side=tk.LEFT, padx=6)

        # EXIF & Auto-rotate checkboxes
        self.exif_var = tk.BooleanVar(value=True)
        self.cb_exif = tk.Checkbutton(
            row2,
            text=self.t("cb_preserve_exif"),
            variable=self.exif_var,
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body,
            activebackground=self.card_bg
        )
        self.cb_exif.pack(side=tk.LEFT, padx=(24, 10))

        self.rotate_var = tk.BooleanVar(value=True)
        self.cb_rotate = tk.Checkbutton(
            row2,
            text=self.t("cb_auto_rotate"),
            variable=self.rotate_var,
            bg=self.card_bg,
            fg=self.text_color,
            font=self.font_body,
            activebackground=self.card_bg
        )
        self.cb_rotate.pack(side=tk.LEFT, padx=10)

        # Update button text on format change
        self.format_var.trace_add("write", lambda *args: self.start_btn.configure(
            text=self.t("btn_start", fmt=self.format_var.get())
        ))

        # ----------------------------------------------------------------------
        # 5. Center Section: File List (Treeview) - Expands flexibly in both X & Y
        # ----------------------------------------------------------------------
        list_container = ttk.Frame(self.root, padding="18 0 18 10")
        list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = ("name", "size", "status", "output")
        self.tree = ttk.Treeview(
            list_container,
            columns=columns,
            show="headings",
            selectmode="extended"
        )
        self.tree.heading("name", text=self.t("col_name"), anchor=tk.W)
        self.tree.heading("size", text=self.t("col_size"), anchor=tk.E)
        self.tree.heading("status", text=self.t("col_status"), anchor=tk.CENTER)
        self.tree.heading("output", text=self.t("col_output"), anchor=tk.W)

        # Columns configured with stretch to adapt to window resizing
        self.tree.column("name", width=260, minwidth=180, stretch=True)
        self.tree.column("size", width=100, minwidth=80, stretch=False, anchor=tk.E)
        self.tree.column("status", width=110, minwidth=90, stretch=False, anchor=tk.CENTER)
        self.tree.column("output", width=440, minwidth=200, stretch=True)

        # Alternating row colors for crisp readability
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("odd", background="#F8FAFC")

        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right click menu
        self.context_menu = tk.Menu(self.root, tearoff=0, font=self.font_body)
        self.context_menu.add_command(label=self.t("menu_remove"), command=self.remove_selected)
        self.context_menu.add_command(label=self.t("menu_open_folder"), command=self.open_selected_folder)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def on_lang_changed(self, event=None):
        val = self.lang_var.get()
        new_lang = "zh" if val == "繁體中文" else "en"
        if new_lang != self.lang:
            self.lang = new_lang
            self.apply_language()

    def apply_language(self):
        """Refreshes all UI text dynamically according to the current language."""
        self.root.title(self.t("app_title"))
        self.title_lbl.configure(text=self.t("app_title"))
        self.sub_lbl.configure(text=self.t("app_subtitle"))

        self.drop_lbl.configure(text=self.t("drop_hint_dnd" if HAS_DND else "drop_hint_nodnd"))
        self.add_files_btn.configure(text=self.t("btn_add_files"))
        self.add_folder_btn.configure(text=self.t("btn_add_folder"))
        self.clear_btn.configure(text=self.t("btn_clear"))

        self.settings_box.configure(text=self.t("settings_title"))
        self.lbl_output_dir.configure(text=self.t("lbl_output_dir"))
        self.rb_same.configure(text=self.t("rb_same_dir"))
        self.rb_custom.configure(text=self.t("rb_custom_dir"))
        self.dest_browse_btn.configure(text=self.t("btn_browse"))
        self.lbl_target_format.configure(text=self.t("lbl_target_format"))
        self.cb_exif.configure(text=self.t("cb_preserve_exif"))
        self.cb_rotate.configure(text=self.t("cb_auto_rotate"))

        self.tree.heading("name", text=self.t("col_name"))
        self.tree.heading("size", text=self.t("col_size"))
        self.tree.heading("status", text=self.t("col_status"))
        self.tree.heading("output", text=self.t("col_output"))

        self.start_btn.configure(text=self.t("btn_start", fmt=self.format_var.get()))
        self.cancel_btn.configure(text=self.t("btn_cancel"))
        self.open_output_btn.configure(text=self.t("btn_open_output"))

        self.context_menu.entryconfigure(0, label=self.t("menu_remove"))
        self.context_menu.entryconfigure(1, label=self.t("menu_open_folder"))

        if not self.is_converting:
            if not self.file_list:
                self.status_lbl.configure(text=self.t("status_ready"))
            else:
                self.status_lbl.configure(text=self.t("status_remaining", count=len(self.file_list)))

    def toggle_dest_mode(self):
        if self.dest_mode_var.get() == "custom":
            self.dest_entry.configure(state="normal")
            self.dest_browse_btn.configure(state="normal")
            if not self.custom_dir_var.get():
                self.dest_entry.focus_set()
        else:
            self.dest_entry.configure(state="disabled")
            self.dest_browse_btn.configure(state="disabled")

    def browse_custom_dir(self):
        d = filedialog.askdirectory(title=self.t("dialog_choose_dest"))
        if d:
            self.custom_dir_var.set(os.path.normpath(d))

    def choose_files(self):
        files = filedialog.askopenfilenames(
            title=self.t("dialog_choose_files"),
            filetypes=[
                (self.t("filter_heic"), "*.heic *.heif *.hif *.HEIC *.HEIF *.HIF"),
                (self.t("filter_all"), "*.*")
            ]
        )
        if files:
            self.add_paths(list(files))

    def choose_folder(self):
        folder = filedialog.askdirectory(title=self.t("dialog_choose_folder"))
        if folder:
            self.add_paths([folder])

    def on_drop(self, event):
        raw_data = event.data
        paths = []
        if "{" in raw_data and "}" in raw_data:
            import re
            matches = re.findall(r'\{([^}]+)\}|(\S+)', raw_data)
            paths = [m[0] or m[1] for m in matches]
        else:
            paths = self.root.tk.splitlist(raw_data)
        self.add_paths(paths)

    def add_paths(self, paths: List[str]):
        collected = converter.collect_heic_files(paths)
        new_count = 0
        for p in collected:
            if p not in self.file_set:
                self.file_set.add(p)
                self.file_list.append(p)
                new_count += 1
                try:
                    size_str = format_size(os.path.getsize(p))
                except Exception:
                    size_str = self.t("size_unknown")

                tag = "even" if len(self.file_list) % 2 == 0 else "odd"
                self.tree.insert(
                    "",
                    tk.END,
                    iid=p,
                    values=(Path(p).name, size_str, self.t("status_waiting"), "-"),
                    tags=(tag,)
                )

        total = len(self.file_list)
        self.status_lbl.configure(text=self.t("status_list_count", total=total, new_count=new_count))

    def clear_list(self):
        if self.is_converting:
            return
        self.tree.delete(*self.tree.get_children())
        self.file_list.clear()
        self.file_set.clear()
        self.progress_var.set(0)
        self.status_lbl.configure(text=self.t("status_cleared"))
        self.open_output_btn.configure(state="disabled")

    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            if row_id not in self.tree.selection():
                self.tree.selection_set(row_id)
            self.context_menu.post(event.x_root, event.y_root)

    def remove_selected(self):
        if self.is_converting:
            return
        selected = self.tree.selection()
        for item in selected:
            if item in self.file_set:
                self.file_set.remove(item)
                self.file_list.remove(item)
            self.tree.delete(item)
        self.status_lbl.configure(text=self.t("status_remaining", count=len(self.file_list)))

    def open_selected_folder(self):
        selected = self.tree.selection()
        if selected:
            first_path = selected[0]
            folder = os.path.dirname(first_path)
            if os.path.exists(folder):
                os.startfile(folder)

    def open_output_folder(self):
        if self.last_output_dir and os.path.exists(self.last_output_dir):
            os.startfile(self.last_output_dir)
        elif self.file_list:
            first = self.file_list[0]
            os.startfile(os.path.dirname(first))

    def cancel_conversion(self):
        if self.is_converting:
            self.should_cancel = True
            self.status_lbl.configure(text=self.t("status_cancelling"))
            self.cancel_btn.configure(state="disabled")

    def start_conversion(self):
        if self.is_converting:
            return

        if not self.file_list:
            messagebox.showwarning(self.t("dialog_tip"), self.t("dialog_no_files"))
            return

        output_dir = None
        if self.dest_mode_var.get() == "custom":
            output_dir = self.custom_dir_var.get().strip()
            if not output_dir:
                messagebox.showwarning(self.t("dialog_tip"), self.t("dialog_no_dest"))
                return
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror(self.t("dialog_error"), self.t("dialog_mkdir_fail", e=e))
                return

        # Prepare UI
        self.is_converting = True
        self.should_cancel = False
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.open_output_btn.configure(state="disabled")
        self.progress_var.set(0)

        # Reset status
        for item in self.file_list:
            vals = list(self.tree.item(item, "values"))
            vals[2] = self.t("status_waiting")
            self.tree.item(item, values=vals)

        # Start thread
        t = threading.Thread(
            target=self.worker_thread,
            args=(
                list(self.file_list),
                output_dir,
                self.format_var.get(),
                self.rotate_var.get(),
                self.exif_var.get()
            ),
            daemon=True
        )
        t.start()

    def worker_thread(self, files, output_dir, fmt, rotate, exif):
        def on_complete(res, completed, total_count):
            self.msg_queue.put(("file_done", res, completed, total_count))

        results = converter.batch_convert(
            files,
            output_dir=output_dir,
            output_format=fmt,
            auto_rotate=rotate,
            preserve_exif=exif,
            max_workers=min(8, os.cpu_count() or 4),
            on_file_complete=on_complete,
            cancel_flag=lambda: self.should_cancel
        )

        success_count = sum(1 for r in results if r["success"])
        failed_count = len(results) - success_count

        self.msg_queue.put(("finished", success_count, failed_count, output_dir))

    def process_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                msg_type = msg[0]

                if msg_type == "file_done":
                    _, res, current, total = msg
                    in_path = res["input_path"]
                    pct = (current / total) * 100
                    self.progress_var.set(pct)

                    if self.tree.exists(in_path):
                        vals = list(self.tree.item(in_path, "values"))
                        if res["success"]:
                            vals[2] = self.t("status_success")
                            vals[3] = res["output_path"]
                            self.last_output_dir = os.path.dirname(res["output_path"])
                        else:
                            vals[2] = self.t("status_failed")
                            vals[3] = f"Error: {res['error']}"
                        self.tree.item(in_path, values=vals)

                    self.status_lbl.configure(text=self.t("status_converting", current=current, total=total, pct=pct, name=Path(in_path).name))

                elif msg_type == "finished":
                    _, sc, fc, out_dir = msg
                    self.is_converting = False
                    self.start_btn.configure(state="normal")
                    self.cancel_btn.configure(state="disabled")
                    self.open_output_btn.configure(state="normal")
                    self.progress_var.set(100)

                    if self.should_cancel:
                        self.status_lbl.configure(text=self.t("status_cancelled", sc=sc, fc=fc))
                        messagebox.showinfo(self.t("dialog_cancelled_title"), self.t("dialog_cancelled_body", sc=sc, fc=fc))
                    else:
                        self.status_lbl.configure(text=self.t("status_all_done", sc=sc, fc=fc))
                        messagebox.showinfo(self.t("dialog_done_title"), self.t("dialog_done_body", sc=sc, fc=fc))

        except queue.Empty:
            pass

        self.root.after(100, self.process_queue)


def launch():
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = HEICConverterApp(root)

    # If launched with arguments (e.g. files dropped onto the .exe)
    if len(sys.argv) > 1:
        root.after(200, lambda: app.add_paths(sys.argv[1:]))

    root.mainloop()


if __name__ == "__main__":
    launch()
