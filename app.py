# -*- coding: utf-8 -*-
# =============================================================================
# app.py — Giao diện ứng dụng Mô phỏng Cây Đỏ Đen (Red-Black Tree Visualizer)
# =============================================================================
# Stack: Python + CustomTkinter + tkinter.Canvas
# Giao diện tối (dark theme), chia 2 panel:
#   - Trái : Control Panel (nhập liệu, nút bấm, trạng thái)
#   - Phải : Canvas — vẽ cây đồ họa với hình tròn + đường nối
# =============================================================================

import math
import re
import tkinter as tk

import customtkinter as ctk

from rbt import RedBlackTree

# ── Cấu hình giao diện toàn cục ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Màu sắc theme ────────────────────────────────────────────────────────────
COLORS = {
    # Nền
    "bg_main":    "#0d1117",
    "bg_panel":   "#161b22",
    "bg_canvas":  "#0d1117",
    "bg_header":  "#161b22",

    # Node: đỏ
    "node_red_fill":    "#c0392b",
    "node_red_outline": "#e74c3c",
    "node_red_text":    "#ffffff",

    # Node: đen
    "node_black_fill":    "#1e1e2e",
    "node_black_outline": "#5a5a8a",
    "node_black_text":    "#e8e8e8",

    # Node: highlighted (tìm thấy)
    "node_hl_fill":    "#d4a017",
    "node_hl_outline": "#ffd700",
    "node_hl_text":    "#000000",

    # Đường nối
    "edge": "#3a3a5a",

    # Trạng thái
    "status_ok":    "#4CAF50",
    "status_warn":  "#FFA500",
    "status_error": "#FF6B6B",
    "status_found": "#FFD700",
    "status_idle":  "#666677",

    # Nút
    "btn_create":  "#1f538d",
    "btn_insert":  "#1a5e39",
    "btn_search":  "#6b2d8b",
    "btn_clear":   "#5a3010",
    "btn_hover_c": "#2a6db8",
    "btn_hover_i": "#22784a",
    "btn_hover_s": "#8b3dab",
    "btn_hover_x": "#7a4010",

    # Separator
    "separator":   "#30363d",
}

# ── Hằng số bố cục cây Canvas ────────────────────────────────────────────────
NODE_R  = 22    # bán kính hình tròn node (px)
H_GAP   = 64    # khoảng cách ngang giữa các node in-order liên tiếp (px)
V_GAP   = 76    # khoảng cách dọc giữa các cấp (px)
MARGIN  = 56    # lề xung quanh canvas (px)


class RBTApp(ctk.CTk):
    """Cửa sổ chính của ứng dụng."""

    def __init__(self):
        super().__init__()

        self.title("Red-Black Tree Visualizer")
        self.geometry("1280x760")
        self.minsize(960, 600)
        self.configure(fg_color=COLORS["bg_main"])

        self.rbt = RedBlackTree()
        self.highlighted_key: int | None = None

        self._build_layout()
        self._refresh_display()

    # ==========================================================================
    # Xây dựng giao diện
    # ==========================================================================

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=0, minsize=310)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_control_panel()
        self._build_display_panel()

    # ── Panel điều khiển (trái) ────────────────────────────────────────────────

    def _build_control_panel(self) -> None:
        self.ctrl = ctk.CTkFrame(
            self, width=310,
            fg_color=COLORS["bg_panel"],
            corner_radius=0,
        )
        self.ctrl.grid(row=0, column=0, sticky="nsew")
        self.ctrl.grid_propagate(False)
        self.ctrl.grid_columnconfigure(0, weight=1)

        row = 0

        # Tiêu đề
        tf = ctk.CTkFrame(self.ctrl, fg_color="transparent")
        tf.grid(row=row, column=0, sticky="ew", pady=(24, 0), padx=24)
        ctk.CTkLabel(tf, text="Red-Black Tree",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color="#E8E8E8").pack(anchor="w")
        ctk.CTkLabel(tf, text="Mô phỏng cây đỏ đen tương tác",
                     font=ctk.CTkFont("Segoe UI", 11),
                     text_color=COLORS["status_idle"]).pack(anchor="w", pady=(2, 0))
        row += 1

        self._sep(row); row += 1
        row = self._build_create_section(row)
        self._sep(row); row += 1
        row = self._build_insert_section(row)
        self._sep(row); row += 1
        row = self._build_search_section(row)
        self._sep(row); row += 1
        row = self._build_status_box(row)

        # Spacer co giãn
        self.ctrl.grid_rowconfigure(row, weight=1); row += 1

        # Nút xóa cây
        ctk.CTkButton(
            self.ctrl, text="Xóa Cây (Reset)",
            command=self._on_clear, height=34,
            fg_color=COLORS["btn_clear"], hover_color=COLORS["btn_hover_x"],
            font=ctk.CTkFont(size=12),
        ).grid(row=row, column=0, sticky="ew", padx=24, pady=(0, 20))

    def _sep(self, row: int) -> None:
        ctk.CTkFrame(self.ctrl, height=1, fg_color=COLORS["separator"]).grid(
            row=row, column=0, sticky="ew", padx=24, pady=(6, 0))

    def _build_create_section(self, r: int) -> int:
        f = ctk.CTkFrame(self.ctrl, fg_color="transparent")
        f.grid(row=r, column=0, sticky="ew", padx=24, pady=(16, 0))

        ctk.CTkLabel(f, text="Tạo Cây Mới",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#C8C8FF").pack(anchor="w")
        ctk.CTkLabel(f,
                     text="Nhập các số nguyên, cách nhau bằng dấu phẩy hoặc khoảng trắng:",
                     font=ctk.CTkFont(size=10), text_color=COLORS["status_idle"],
                     wraplength=265, justify="left").pack(anchor="w", pady=(3, 8))

        self.create_entry = ctk.CTkEntry(
            f, placeholder_text="Ví dụ: 10, 20, 5, 15, 30, 25",
            height=38, font=ctk.CTkFont(size=12))
        self.create_entry.pack(fill="x", pady=(0, 8))
        self.create_entry.bind("<Return>", lambda _: self._on_create())

        ctk.CTkButton(f, text="Tạo Cây Mới", command=self._on_create,
                      height=38, fg_color=COLORS["btn_create"],
                      hover_color=COLORS["btn_hover_c"],
                      font=ctk.CTkFont(size=12, weight="bold")).pack(fill="x")
        return r + 1

    def _build_insert_section(self, r: int) -> int:
        f = ctk.CTkFrame(self.ctrl, fg_color="transparent")
        f.grid(row=r, column=0, sticky="ew", padx=24, pady=(16, 0))

        ctk.CTkLabel(f, text="Thêm Khóa",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#90EE90").pack(anchor="w")
        ctk.CTkLabel(f, text="Nhập một số nguyên để chèn vào cây:",
                     font=ctk.CTkFont(size=10), text_color=COLORS["status_idle"]
                     ).pack(anchor="w", pady=(3, 8))

        self.insert_entry = ctk.CTkEntry(
            f, placeholder_text="Ví dụ: 42",
            height=38, font=ctk.CTkFont(size=12))
        self.insert_entry.pack(fill="x", pady=(0, 8))
        self.insert_entry.bind("<Return>", lambda _: self._on_insert())

        ctk.CTkButton(f, text="Thêm Khóa", command=self._on_insert,
                      height=38, fg_color=COLORS["btn_insert"],
                      hover_color=COLORS["btn_hover_i"],
                      font=ctk.CTkFont(size=12, weight="bold")).pack(fill="x")
        return r + 1

    def _build_search_section(self, r: int) -> int:
        f = ctk.CTkFrame(self.ctrl, fg_color="transparent")
        f.grid(row=r, column=0, sticky="ew", padx=24, pady=(16, 0))

        ctk.CTkLabel(f, text="Tìm Kiếm",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#DEB887").pack(anchor="w")
        ctk.CTkLabel(f, text="Nhập số nguyên cần tìm trong cây:",
                     font=ctk.CTkFont(size=10), text_color=COLORS["status_idle"]
                     ).pack(anchor="w", pady=(3, 8))

        self.search_entry = ctk.CTkEntry(
            f, placeholder_text="Ví dụ: 15",
            height=38, font=ctk.CTkFont(size=12))
        self.search_entry.pack(fill="x", pady=(0, 8))
        self.search_entry.bind("<Return>", lambda _: self._on_search())

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")
        btn_row.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(btn_row, text="Tìm Kiếm", command=self._on_search,
                      height=38, fg_color=COLORS["btn_search"],
                      hover_color=COLORS["btn_hover_s"],
                      font=ctk.CTkFont(size=12, weight="bold")
                      ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(btn_row, text="Bỏ chọn", command=self._on_clear_highlight,
                      height=38, width=80,
                      fg_color="#333344", hover_color="#444455",
                      font=ctk.CTkFont(size=11)
                      ).grid(row=0, column=1)
        return r + 1

    def _build_status_box(self, r: int) -> int:
        f = ctk.CTkFrame(self.ctrl, fg_color="#1a1a2e", corner_radius=8)
        f.grid(row=r, column=0, sticky="ew", padx=24, pady=(16, 6))

        ctk.CTkLabel(f, text="Trạng thái",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#555577").pack(anchor="w", padx=12, pady=(10, 2))

        self.status_label = ctk.CTkLabel(
            f, text="Sẵn sàng. Nhập dữ liệu để bắt đầu.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["status_idle"],
            wraplength=258, justify="left")
        self.status_label.pack(anchor="w", padx=12, pady=(0, 12))
        return r + 1

    # ── Panel hiển thị Canvas (phải) ──────────────────────────────────────────

    def _build_display_panel(self) -> None:
        self.disp = ctk.CTkFrame(self, fg_color=COLORS["bg_canvas"], corner_radius=0)
        self.disp.grid(row=0, column=1, sticky="nsew")
        self.disp.grid_rowconfigure(1, weight=1)
        self.disp.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self.disp, fg_color=COLORS["bg_header"],
                               corner_radius=0, height=52)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(header, text="Cấu trúc Cây Đỏ Đen",
                     font=ctk.CTkFont("Segoe UI", 14, "bold"),
                     text_color="#C8C8FF").pack(side="left", padx=20, pady=14)

        legend = ctk.CTkFrame(header, fg_color="transparent")
        legend.pack(side="right", padx=16, pady=10)
        self._legend_item(legend, "● Node Đỏ",   COLORS["node_red_outline"])
        self._legend_item(legend, "● Node Đen",  COLORS["node_black_outline"])
        self._legend_item(legend, "★ Tìm thấy", COLORS["node_hl_outline"])

        # Canvas container (tk.Frame để đặt scrollbar)
        container = tk.Frame(self.disp, bg=COLORS["bg_canvas"])
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            container,
            bg=COLORS["bg_canvas"],
            highlightthickness=0,
        )
        h_scroll = tk.Scrollbar(container, orient="horizontal",
                                command=self.canvas.xview,
                                bg=COLORS["bg_panel"])
        v_scroll = tk.Scrollbar(container, orient="vertical",
                                command=self.canvas.yview,
                                bg=COLORS["bg_panel"])
        self.canvas.configure(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scroll.grid(row=1, column=0, sticky="ew")
        v_scroll.grid(row=0, column=1, sticky="ns")

        # Kéo canvas bằng chuột
        self.canvas.bind("<ButtonPress-1>",   self._on_canvas_drag_start)
        self.canvas.bind("<B1-Motion>",        self._on_canvas_drag)
        self.canvas.bind("<MouseWheel>",       self._on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self._on_mousewheel_h)

        self._drag_x = 0
        self._drag_y = 0

    @staticmethod
    def _legend_item(parent: ctk.CTkFrame, text: str, color: str) -> None:
        ctk.CTkLabel(parent, text=text,
                     font=ctk.CTkFont(size=12),
                     text_color=color).pack(side="left", padx=8)

    # ==========================================================================
    # Canvas drag & scroll helpers
    # ==========================================================================

    def _on_canvas_drag_start(self, event: tk.Event) -> None:
        self.canvas.scan_mark(event.x, event.y)

    def _on_canvas_drag(self, event: tk.Event) -> None:
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_h(self, event: tk.Event) -> None:
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    # ==========================================================================
    # Layout Algorithm — tính toán tọa độ (x, y) cho mỗi node
    # ==========================================================================

    def _compute_layout(self) -> dict[int, tuple[float, float]]:
        """
        Sử dụng duyệt in-order để gán vị trí x (thứ tự xuất hiện từ trái sang phải).
        Vị trí y được tính theo độ sâu (depth) của node.

        Kết quả: dict mapping key -> (x, y) pixel
        """
        positions: dict[int, tuple[float, float]] = {}
        counter = [0]   # counter dùng chung qua closure (tránh nonlocal)

        def in_order(node, depth: int) -> None:
            if node == self.rbt.NIL:
                return
            in_order(node.left, depth + 1)

            x = MARGIN + counter[0] * H_GAP
            y = MARGIN + depth * V_GAP
            positions[node.key] = (x, y)
            counter[0] += 1

            in_order(node.right, depth + 1)

        in_order(self.rbt.root, 0)
        return positions

    # ==========================================================================
    # Vẽ cây lên Canvas
    # ==========================================================================

    def _refresh_display(self) -> None:
        """Xóa canvas và vẽ lại toàn bộ cây."""
        self.canvas.delete("all")

        if self.rbt.is_empty():
            # Hiển thị thông báo cây rỗng
            self.canvas.update_idletasks()
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            cx = max(w // 2, 200)
            cy = max(h // 2, 150)
            self.canvas.create_text(
                cx, cy,
                text="Cây rỗng — nhập số và nhấn 'Tạo Cây Mới'",
                fill="#444466",
                font=("Segoe UI", 13, "italic"),
            )
            return

        positions = self._compute_layout()

        # 1. Vẽ cạnh (edges) trước — node sẽ che phủ đầu đường kẻ
        self._draw_edges(self.rbt.root, positions)

        # 2. Vẽ node (circles + text) lên trên
        self._draw_nodes(self.rbt.root, positions)

        # Cập nhật scrollregion để canvas có thể scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _draw_edges(self, node, positions: dict) -> None:
        """
        Vẽ đường nối từ node cha đến node con.
        Đường kẻ xuất phát từ mép dưới hình tròn cha
        và kết thúc tại mép trên hình tròn con, nhờ vào toán học vector.
        """
        if node == self.rbt.NIL:
            return

        px, py = positions[node.key]

        for child in (node.left, node.right):
            if child == self.rbt.NIL:
                continue

            cx, cy = positions[child.key]

            # Tính góc hướng từ cha → con
            angle = math.atan2(cy - py, cx - px)

            # Điểm xuất phát: mép hình tròn cha (hướng về phía con)
            sx = px + NODE_R * math.cos(angle)
            sy = py + NODE_R * math.sin(angle)

            # Điểm kết thúc: mép hình tròn con (hướng từ phía cha vào)
            ex = cx - NODE_R * math.cos(angle)
            ey = cy - NODE_R * math.sin(angle)

            self.canvas.create_line(
                sx, sy, ex, ey,
                fill=COLORS["edge"],
                width=2,
                smooth=True,
            )
            self._draw_edges(child, positions)

    def _draw_nodes(self, node, positions: dict) -> None:
        """Vẽ hình tròn + số cho từng node, với màu tương ứng màu RBT."""
        if node == self.rbt.NIL:
            return

        x, y = positions[node.key]
        r = NODE_R

        is_hl = (self.highlighted_key is not None
                 and node.key == self.highlighted_key)

        if is_hl:
            fill    = COLORS["node_hl_fill"]
            outline = COLORS["node_hl_outline"]
            text_c  = COLORS["node_hl_text"]
            width   = 3
        elif node.color == "RED":
            fill    = COLORS["node_red_fill"]
            outline = COLORS["node_red_outline"]
            text_c  = COLORS["node_red_text"]
            width   = 1
        else:   # BLACK
            fill    = COLORS["node_black_fill"]
            outline = COLORS["node_black_outline"]
            text_c  = COLORS["node_black_text"]
            width   = 1

        # Hình tròn node
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=fill,
            outline=outline,
            width=width,
        )

        # Số khóa bên trong — căn giữa
        label = str(node.key)
        font_size = 10 if len(label) >= 3 else 11
        self.canvas.create_text(
            x, y,
            text=label,
            fill=text_c,
            font=("Courier New", font_size, "bold"),
        )

        self._draw_nodes(node.left,  positions)
        self._draw_nodes(node.right, positions)

    # ==========================================================================
    # Trạng thái
    # ==========================================================================

    def _set_status(self, message: str, color: str = "") -> None:
        self.status_label.configure(
            text=message,
            text_color=color or COLORS["status_idle"],
        )

    # ==========================================================================
    # Event Handlers
    # ==========================================================================

    def _on_create(self) -> None:
        raw = self.create_entry.get().strip()
        if not raw:
            self._set_status("Lỗi: Ô nhập liệu đang trống!", COLORS["status_error"])
            self.create_entry.focus(); return

        tokens = re.split(r"[,\s]+", raw)
        keys: list[int] = []
        invalid: list[str] = []

        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            try:
                keys.append(int(tok))
            except ValueError:
                invalid.append(tok)

        if invalid:
            self._set_status(
                f"Lỗi: Giá trị không hợp lệ — {', '.join(invalid)}",
                COLORS["status_error"]); return
        if not keys:
            self._set_status("Lỗi: Không tìm thấy khóa hợp lệ nào!",
                             COLORS["status_error"]); return

        self.rbt = RedBlackTree()
        self.highlighted_key = None
        inserted, duplicates = [], []

        for k in keys:
            ok, _ = self.rbt.insert(k)
            (inserted if ok else duplicates).append(k)

        self._refresh_display()
        msg = f"Tạo cây thành công với {len(inserted)} khóa."
        if duplicates:
            msg += f"  (Bỏ qua trùng: {duplicates})"
        self._set_status(msg, COLORS["status_ok"])

    def _on_insert(self) -> None:
        raw = self.insert_entry.get().strip()
        if not raw:
            self._set_status("Lỗi: Ô nhập liệu đang trống!", COLORS["status_error"])
            self.insert_entry.focus(); return

        try:
            key = int(raw)
        except ValueError:
            self._set_status(f"Lỗi: '{raw}' không phải số nguyên!",
                             COLORS["status_error"]); return

        self.highlighted_key = None
        ok, message = self.rbt.insert(key)
        self._refresh_display()

        if ok:
            self._set_status(f"✓ {message}: {key}", COLORS["status_ok"])
            self.insert_entry.delete(0, "end")
        else:
            self._set_status(f"⚠ {message}", COLORS["status_warn"])

    def _on_search(self) -> None:
        raw = self.search_entry.get().strip()
        if not raw:
            self._set_status("Lỗi: Ô nhập liệu đang trống!", COLORS["status_error"])
            self.search_entry.focus(); return

        try:
            key = int(raw)
        except ValueError:
            self._set_status(f"Lỗi: '{raw}' không phải số nguyên!",
                             COLORS["status_error"]); return

        if self.rbt.is_empty():
            self._set_status("Lỗi: Cây đang rỗng!", COLORS["status_error"]); return

        node, path, depth = self.rbt.search_with_info(key)

        if node is not None:
            self.highlighted_key = key
            self._refresh_display()
            color_str = "Đỏ (RED)" if node.color == "RED" else "Đen (BLACK)"
            self._set_status(
                f"✓ Tìm thấy khóa {key}!\n"
                f"Màu node: {color_str}\n"
                f"Độ sâu: {depth}\n"
                f"Đường đi: {' → '.join(path)}",
                COLORS["status_found"],
            )
        else:
            self.highlighted_key = None
            self._refresh_display()
            self._set_status(f"✗ Khóa {key} không tồn tại trong cây!",
                             COLORS["status_error"])

    def _on_clear_highlight(self) -> None:
        self.highlighted_key = None
        self._refresh_display()
        self._set_status("Đã bỏ highlight.", COLORS["status_idle"])

    def _on_clear(self) -> None:
        self.rbt = RedBlackTree()
        self.highlighted_key = None
        for entry in (self.create_entry, self.insert_entry, self.search_entry):
            entry.delete(0, "end")
        self._refresh_display()
        self._set_status("Đã xóa cây. Sẵn sàng tạo cây mới.", COLORS["status_idle"])


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    app = RBTApp()
    app.mainloop()
