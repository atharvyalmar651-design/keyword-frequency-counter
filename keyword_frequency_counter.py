
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import csv

# ---------------- COLORS ----------------
BG = "#F3F6FC"
WHITE = "#FFFFFF"
NAVY = "#14213D"
NAVY_LIGHT = "#243657"
BLUE = "#5277F7"
BLUE_LIGHT = "#EAF0FF"
TEAL = "#13A58B"
PURPLE = "#8957E5"
ORANGE = "#F09A38"
TEXT = "#18243B"
MUTED = "#74819A"
BORDER = "#E1E8F3"


class KeywordFrequencyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("KeyCount | Keyword Frequency Counter")
        self.root.geometry("1200x780")
        self.root.minsize(850, 620)
        self.root.configure(bg=BG)

        self.hash_table = {}
        self.total_words = 0

        self.setup_styles()
        self.create_interface()
        self.load_sample()

    # ---------- TABLE STYLING ----------

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=32,
            fieldbackground=WHITE,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#EDF1F9",
            foreground=NAVY,
            font=("Segoe UI", 9, "bold"),
            padding=10,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", BLUE_LIGHT)],
            foreground=[("selected", TEXT)]
        )

    # ---------- MAIN INTERFACE ----------

    def create_interface(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = tk.Frame(self.root, bg=NAVY, width=215)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="◆  KeyCount",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", padx=20, pady=(30, 5))

        tk.Label(
            sidebar,
            text="TEXT ANALYTICS",
            bg=NAVY,
            fg="#9EAFD0",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=23, pady=(0, 35))

        tk.Label(
            sidebar,
            text="WORKSPACE",
            bg=NAVY,
            fg="#8295B9",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 12))

        self.sidebar_item(sidebar, "▦   Overview", True)
        self.sidebar_item(sidebar, "⌕   Keyword Analysis")
        self.sidebar_item(sidebar, "▤   Hash Table")
        self.sidebar_item(sidebar, "⇩   Export Results")

        tk.Frame(sidebar, bg="#354665", height=1).pack(
            fill="x", padx=18, pady=25
        )

        tk.Label(
            sidebar,
            text="DSA MINI PROJECT",
            bg=NAVY,
            fg="#9EAFD0",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=22)

        tk.Label(
            sidebar,
            text="Hash Table\nImplementation",
            bg=NAVY,
            fg=WHITE,
            justify="left",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=22, pady=10)

        tk.Label(
            sidebar,
            text="Built with Python + Tkinter",
            bg=NAVY,
            fg="#9EAFD0",
            font=("Segoe UI", 9)
        ).pack(side="bottom", anchor="w", padx=20, pady=20)

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)

        # Top bar
        topbar = tk.Frame(
            main, bg=WHITE, padx=25, pady=18
        )
        topbar.grid(row=0, column=0, sticky="ew")

        tk.Label(
            topbar,
            text="Keyword Frequency Analyzer",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(side="left")

        tk.Label(
            topbar,
            text="● READY",
            bg="#E2F8F0",
            fg="#087F67",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        ).pack(side="right")

        # Content heading
        content = tk.Frame(main, bg=BG, padx=24, pady=18)
        content.grid(row=1, column=0, sticky="ew")

        tk.Label(
            content,
            text="Your text, decoded.",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Analyze repeated words and discover useful patterns.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 15))

        # Statistic cards
        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x")

        self.total_label = self.stat_card(
            cards, "TOTAL WORDS", "0", "All word occurrences", BLUE
        )

        self.unique_label = self.stat_card(
            cards, "UNIQUE KEYWORDS", "0", "Distinct words", TEAL
        )

        self.top_label = self.stat_card(
            cards, "TOP KEYWORD", "—", "Most frequent word", PURPLE
        )

        self.count_label = self.stat_card(
            cards, "TOP FREQUENCY", "0", "Highest occurrence", ORANGE
        )

        # Input card
        input_card = self.make_card(content)
        input_card.pack(fill="x", pady=(15, 0))

        tk.Label(
            input_card,
            text="01  /  INPUT TEXT",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            input_card,
            text="Paste or type your text below",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 8))

        self.text_box = tk.Text(
            input_card,
            height=4,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#F8FAFF",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            padx=12,
            pady=10
        )
        self.text_box.pack(fill="x", pady=(0, 12))

        buttons = tk.Frame(input_card, bg=WHITE)
        buttons.pack(fill="x")

        self.make_button(
            buttons, "Analyze Text", self.analyze, BLUE, WHITE
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            buttons, "Load Sample", self.load_sample,
            BLUE_LIGHT, NAVY
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            buttons, "Clear", self.clear_all,
            "#FDECEC", "#B42332"
        ).pack(side="left")

        # Results card
        results = self.make_card(main)
        results.grid(
            row=3, column=0, sticky="nsew",
            padx=24, pady=(0, 22)
        )
        results.grid_columnconfigure(0, weight=1)
        results.grid_rowconfigure(2, weight=1)

        heading = tk.Frame(results, bg=WHITE)
        heading.grid(row=0, column=0, sticky="ew")

        tk.Label(
            heading,
            text="02  /  FREQUENCY RESULTS",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.result_count = tk.Label(
            heading,
            text="0 keywords",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.result_count.pack(side="right")

        # Search and sorting
        controls = tk.Frame(results, bg=WHITE)
        controls.grid(row=1, column=0, sticky="ew", pady=12)

        tk.Label(
            controls, text="Search:",
            bg=WHITE, fg=MUTED
        ).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        search = ttk.Entry(
            controls, textvariable=self.search_var, width=20
        )
        search.pack(side="left", ipady=5)

        self.search_var.trace_add(
            "write", lambda *_: self.refresh_table()
        )

        tk.Label(
            controls, text="Sort:",
            bg=WHITE, fg=MUTED
        ).pack(side="left", padx=(12, 6))

        self.sort_var = tk.StringVar(value="Most frequent")

        sort_box = ttk.Combobox(
            controls,
            textvariable=self.sort_var,
            state="readonly",
            width=17,
            values=[
                "Most frequent",
                "Least frequent",
                "Keyword A-Z",
                "Keyword Z-A"
            ]
        )
        sort_box.pack(side="left", ipady=3)

        sort_box.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.refresh_table()
        )

        self.make_button(
            controls, "View Hash Table",
            self.show_hash_table, "#F0EAFE", "#6941C6"
        ).pack(side="right")

        self.make_button(
            controls, "Export CSV",
            self.export_csv, "#E2F8F0", "#087F67"
        ).pack(side="right", padx=(0, 8))

        # Results table
        table_frame = tk.Frame(results, bg=WHITE)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("keyword", "frequency", "percentage", "bar"),
            show="headings"
        )

        self.tree.heading("keyword", text="KEYWORD")
        self.tree.heading("frequency", text="COUNT")
        self.tree.heading("percentage", text="SHARE OF TEXT")
        self.tree.heading("bar", text="FREQUENCY BAR")

        self.tree.column("keyword", width=180)
        self.tree.column("frequency", width=80, anchor="center")
        self.tree.column("percentage", width=120, anchor="center")
        self.tree.column("bar", width=180, anchor="w")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.tag_configure("even", background=WHITE)
        self.tree.tag_configure("odd", background="#F7F9FD")

        # Footer
        footer = tk.Frame(results, bg=WHITE)
        footer.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        self.status_label = tk.Label(
            footer,
            text="Ready to analyze text.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="left")

        tk.Label(
            footer,
            text="HASH TABLE  |  AVERAGE O(n)",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

    # ---------- REUSABLE UI COMPONENTS ----------

    def sidebar_item(self, parent, text, active=False):
        bg = NAVY_LIGHT if active else NAVY
        fg = WHITE if active else "#B3C1DC"

        tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 10, "bold" if active else "normal"),
            anchor="w",
            padx=16,
            pady=12
        ).pack(fill="x", padx=12, pady=3)

    def stat_card(self, parent, title, value, caption, accent):
        outer = tk.Frame(parent, bg=BG)
        outer.pack(side="left", fill="x", expand=True, padx=(0, 8))

        card = tk.Frame(
            outer, bg=WHITE, padx=12, pady=12,
            highlightbackground=BORDER, highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=accent, height=4).pack(fill="x", pady=(0, 9))

        tk.Label(
            card, text=title,
            bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        value_label = tk.Label(
            card, text=value,
            bg=WHITE, fg=TEXT,
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        )
        value_label.pack(anchor="w", pady=(6, 2))

        tk.Label(
            card, text=caption,
            bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        return value_label

    def make_card(self, parent):
        return tk.Frame(
            parent,
            bg=WHITE,
            padx=16,
            pady=14,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def make_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=13,
            pady=8,
            cursor="hand2"
        )

    # ---------- HASH TABLE LOGIC ----------

    def analyze(self):
        text = self.text_box.get("1.0", "end").strip()

        if not text:
            messagebox.showwarning(
                "No Text", "Please enter some text first."
            )
            return

        # Extract words and normalize to lowercase
        words = re.findall(
            r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*",
            text.lower()
        )

        # Hash table: word -> frequency
        self.hash_table = {}

        for word in words:
            self.hash_table[word] = (
                self.hash_table.get(word, 0) + 1
            )

        self.total_words = len(words)

        # Summary statistics
        self.total_label.config(text=str(self.total_words))
        self.unique_label.config(text=str(len(self.hash_table)))

        if self.hash_table:
            top_word, top_count = min(
                self.hash_table.items(),
                key=lambda item: (-item[1], item[0])
            )
            self.top_label.config(text=top_word)
            self.count_label.config(text=str(top_count))
        else:
            self.top_label.config(text="—")
            self.count_label.config(text="0")

        self.refresh_table()

        self.status_label.config(
            text=f"Analyzed {self.total_words} words successfully."
        )

    # ---------- TABLE, SEARCH AND SORT ----------

    def refresh_table(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().lower().strip()

        rows = [
            (word, count)
            for word, count in self.hash_table.items()
            if query in word
        ]

        mode = self.sort_var.get()

        if mode == "Least frequent":
            rows.sort(key=lambda item: (item[1], item[0]))
        elif mode == "Keyword A-Z":
            rows.sort(key=lambda item: item[0])
        elif mode == "Keyword Z-A":
            rows.sort(key=lambda item: item[0], reverse=True)
        else:
            rows.sort(key=lambda item: (-item[1], item[0]))

        max_count = max(
            (count for _, count in rows), default=1
        )

        for index, (word, count) in enumerate(rows):
            percentage = (
                count / self.total_words * 100
                if self.total_words else 0
            )

            bar_length = round(count / max_count * 12)
            bar = "■" * bar_length

            tag = "even" if index % 2 == 0 else "odd"

            self.tree.insert(
                "",
                "end",
                values=(
                    word,
                    count,
                    f"{percentage:.1f}%",
                    bar
                ),
                tags=(tag,)
            )

        self.result_count.config(text=f"{len(rows)} keywords")

    # ---------- LOAD SAMPLE AND CLEAR ----------

    def load_sample(self):
        sample = (
            "Python is easy to learn. Python is powerful and Python "
            "is popular. A hash table stores data using keys. "
            "This keyword frequency counter uses a hash table "
            "to count every keyword."
        )

        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", sample)
        self.analyze()

    def clear_all(self):
        self.text_box.delete("1.0", "end")
        self.hash_table = {}
        self.total_words = 0

        self.total_label.config(text="0")
        self.unique_label.config(text="0")
        self.top_label.config(text="—")
        self.count_label.config(text="0")

        self.refresh_table()
        self.status_label.config(text="Input and results cleared.")

    # ---------- HASH TABLE VIEWER ----------

    def show_hash_table(self):
        if not self.hash_table:
            messagebox.showinfo(
                "Empty Hash Table",
                "Analyze some text first."
            )
            return

        window = tk.Toplevel(self.root)
        window.title("Hash Table Inspector")
        window.geometry("480x520")
        window.configure(bg=BG)

        header = tk.Frame(window, bg=NAVY, padx=18, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Hash Table Inspector",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="KEY  →  VALUE  (word → frequency)",
            bg=NAVY,
            fg="#C6D5F5",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(5, 0))

        box = tk.Text(
            window,
            font=("Consolas", 11),
            bg=WHITE,
            fg=TEXT,
            relief="flat",
            padx=15,
            pady=12
        )
        box.pack(fill="both", expand=True, padx=15, pady=15)

        for word, count in sorted(self.hash_table.items()):
            box.insert("end", f"{word:<25} -> {count}\n")

        box.config(state="disabled")

    # ---------- CSV EXPORT ----------

    def export_csv(self):
        if not self.hash_table:
            messagebox.showinfo(
                "No Results",
                "Analyze some text before exporting."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Keyword Results",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not path:
            return

        rows = [
            (word, count)
            for word, count in self.hash_table.items()
            if self.search_var.get().strip().lower() in word
        ]

        mode = self.sort_var.get()

        if mode == "Least frequent":
            rows.sort(key=lambda item: (item[1], item[0]))
        elif mode == "Keyword A-Z":
            rows.sort(key=lambda item: item[0])
        elif mode == "Keyword Z-A":
            rows.sort(key=lambda item: item[0], reverse=True)
        else:
            rows.sort(key=lambda item: (-item[1], item[0]))

        try:
            with open(
                path, "w", newline="", encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Keyword", "Frequency", "Share of Text (%)"
                ])

                for word, count in rows:
                    percentage = (
                        count / self.total_words * 100
                        if self.total_words else 0
                    )
                    writer.writerow([
                        word, count, f"{percentage:.2f}"
                    ])

            messagebox.showinfo(
                "Export Successful",
                "Your CSV file has been saved."
            )

        except OSError as error:
            messagebox.showerror("Export Error", str(error))


# ---------- START APPLICATION ----------

if __name__ == "__main__":
    root = tk.Tk()
    app = KeywordFrequencyApp(root)
    root.mainloop()
