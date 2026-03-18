# -*- coding: utf-8 -*-
# =============================================================================
# rbt.py — Red-Black Tree Logic
# =============================================================================
# Tách biệt hoàn toàn phần logic cấu trúc dữ liệu khỏi phần giao diện.
#
# Quy tắc Cây Đỏ Đen (Red-Black Tree Invariants):
#  1. Mỗi node có màu ĐỎ hoặc ĐEN.
#  2. Gốc (root) luôn là màu ĐEN.
#  3. Mỗi lá NIL (sentinel) là màu ĐEN.
#  4. Nếu một node là ĐỎ thì cả 2 con của nó phải là ĐEN (không có 2 node đỏ liên tiếp).
#  5. Mọi đường đi từ bất kỳ node nào xuống lá đều có cùng số node ĐEN (black-height).
# =============================================================================

RED = "RED"
BLACK = "BLACK"


class Node:
    """Đại diện cho một node trong cây đỏ đen."""

    def __init__(self, key):
        self.key = key
        self.color = RED          # Node mới tạo luôn là ĐỎ (trước khi fix)
        self.left: "Node" = None
        self.right: "Node" = None
        self.parent: "Node" = None

    def __repr__(self):
        return f"Node(key={self.key}, color={self.color})"


class RedBlackTree:
    """
    Cây Đỏ Đen với các thao tác: insert, search, display.
    Sử dụng node sentinel NIL dùng chung cho tất cả các lá.
    """

    def __init__(self):
        # Node NIL sentinel — đại diện cho tất cả các lá NULL (màu ĐEN)
        self.NIL = Node(None)
        self.NIL.color = BLACK
        self.NIL.left = None
        self.NIL.right = None
        self.NIL.parent = None

        self.root = self.NIL

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------

    def insert(self, key: int) -> tuple[bool, str]:
        """
        Chèn khóa vào cây theo chuẩn Red-Black Tree.
        Trả về (True, thông báo) nếu thành công.
        Trả về (False, thông báo) nếu khóa đã tồn tại.
        """
        # Kiểm tra trùng khóa
        if self.search(key) is not None:
            return False, f"Khóa {key} đã tồn tại trong cây"

        # Tạo node mới (luôn ĐỎ)
        z = Node(key)
        z.left = self.NIL
        z.right = self.NIL
        z.parent = None
        z.color = RED

        # --- Bước 1: Chèn như BST thông thường ---
        y = None          # y sẽ là cha của z sau khi chèn
        x = self.root

        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y is None:
            # Cây rỗng — z trở thành root
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        # --- Bước 2: Sửa các vi phạm Red-Black ---
        self._fix_insert(z)
        return True, "Thêm khóa thành công"

    def _fix_insert(self, z: Node) -> None:
        """
        Sửa vi phạm sau khi chèn node z (màu ĐỎ).

        Bất biến vòng lặp: z là node ĐỎ có cha ĐỎ (vi phạm quy tắc 4).

        Có 3 trường hợp (và 3 trường hợp đối xứng khi cha nằm bên phải):
          - Case 1: Chú (uncle) của z là ĐỎ
                → Đổi màu cha, chú → ĐEN; ông nội → ĐỎ; nhảy z lên ông nội.
          - Case 2: Chú là ĐEN, z là "inner" child (cha là left child, z là right child, hoặc ngược lại)
                → Xoay cha về phía z để đưa về Case 3.
          - Case 3: Chú là ĐEN, z là "outer" child (cùng hướng với cha)
                → Xoay ông nội; đổi màu cha → ĐEN, ông nội → ĐỎ.
        """
        while z.parent is not None and z.parent.color == RED:
            gp = z.parent.parent  # Ông nội (grandparent)

            if z.parent == gp.left:
                # ======= Cha là CÁC CON BÊN TRÁI của ông nội =======
                uncle = gp.right

                if uncle.color == RED:
                    # ── Case 1: Chú là ĐỎ → Chỉ cần đổi màu (recolor) ──
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    gp.color = RED
                    z = gp               # Nhảy z lên ông nội, tiếp tục kiểm tra

                else:
                    # Chú là ĐEN
                    if z == z.parent.right:
                        # ── Case 2: z là right child (inner) → Xoay trái tại cha ──
                        # Sau xoay, z cũ sẽ trở thành cha, z.parent cũ trở thành z mới
                        z = z.parent
                        self._rotate_left(z)

                    # ── Case 3: z là left child (outer) → Xoay phải tại ông nội ──
                    z.parent.color = BLACK
                    gp.color = RED
                    self._rotate_right(gp)

            else:
                # ======= Cha là CON BÊN PHẢI của ông nội (đối xứng) =======
                uncle = gp.left

                if uncle.color == RED:
                    # ── Case 1 (đối xứng): Chú là ĐỎ → Đổi màu ──
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    gp.color = RED
                    z = gp

                else:
                    if z == z.parent.left:
                        # ── Case 2 (đối xứng): z là left child (inner) → Xoay phải tại cha ──
                        z = z.parent
                        self._rotate_right(z)

                    # ── Case 3 (đối xứng): z là right child (outer) → Xoay trái tại ông nội ──
                    z.parent.color = BLACK
                    gp.color = RED
                    self._rotate_left(gp)

        # Quy tắc 2: Root luôn phải là ĐEN
        self.root.color = BLACK

    # ------------------------------------------------------------------
    # ROTATIONS
    # ------------------------------------------------------------------

    def _rotate_left(self, x: Node) -> None:
        """
        Xoay trái (Left Rotation) tại node x.

        Trước:           Sau:
             x               y
            / \\            / \\
           A   y    →      x   C
              / \\        / \\
             B   C      A   B

        Con phải của x (y) được đẩy lên thay vị trí x;
        x trở thành con trái của y;
        cây con B (con trái cũ của y) chuyển thành con phải của x.
        """
        y = x.right           # y là con phải của x
        x.right = y.left      # Cây con B của y thành con phải x

        if y.left != self.NIL:
            y.left.parent = x  # Cập nhật cha cho cây con B

        y.parent = x.parent   # y kế thừa cha của x

        if x.parent is None:
            self.root = y                  # x là root → y thành root mới
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x             # x trở thành con trái của y
        x.parent = y

    def _rotate_right(self, y: Node) -> None:
        """
        Xoay phải (Right Rotation) tại node y.

        Trước:           Sau:
              y               x
             / \\            / \\
            x   C    →     A   y
           / \\               / \\
          A   B             B   C

        Con trái của y (x) được đẩy lên thay vị trí y;
        y trở thành con phải của x;
        cây con B (con phải cũ của x) chuyển thành con trái của y.
        """
        x = y.left            # x là con trái của y
        y.left = x.right      # Cây con B của x thành con trái y

        if x.right != self.NIL:
            x.right.parent = y  # Cập nhật cha cho cây con B

        x.parent = y.parent   # x kế thừa cha của y

        if y.parent is None:
            self.root = x                  # y là root → x thành root mới
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y           # y trở thành con phải của x
        y.parent = x

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------

    def search(self, key: int) -> Node | None:
        """Tìm kiếm khóa trong cây. Trả về Node nếu tìm thấy, None nếu không."""
        current = self.root
        while current != self.NIL:
            if current.key == key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def search_with_info(self, key: int) -> tuple[Node | None, list[str], int]:
        """
        Tìm kiếm khóa và trả về thêm thông tin về đường đi.

        Returns:
            (node, path_list, depth)
            - node: Node tìm thấy hoặc None
            - path_list: Danh sách các khóa đã đi qua (dạng chuỗi)
            - depth: Độ sâu của node (root = 0)
        """
        current = self.root
        path = []
        depth = 0

        while current != self.NIL:
            path.append(str(current.key))
            if key == current.key:
                return current, path, depth
            elif key < current.key:
                current = current.left
            else:
                current = current.right
            depth += 1

        return None, path, depth

    # ------------------------------------------------------------------
    # DISPLAY (tạo dữ liệu hiển thị)
    # ------------------------------------------------------------------

    def get_display_segments(self, highlighted_key: int | None = None) -> list[tuple[str, str]]:
        """
        Xây dựng danh sách các đoạn văn bản để hiển thị cây dạng thư mục.

        Mỗi phần tử là tuple (text, tag) với các tag:
          - 'red_node'    : node màu ĐỎ
          - 'black_node'  : node màu ĐEN
          - 'highlighted' : node được tìm thấy (highlight)
          - 'structure'   : ký tự cấu trúc cây (├── │ └── )
          - 'empty'       : thông báo cây rỗng

        Returns:
            Danh sách (text, tag)
        """
        if self.root == self.NIL:
            return [("  (Cây rỗng — chưa có dữ liệu)\n", "empty")]

        segments: list[tuple[str, str]] = []
        self._build_segments(
            node=self.root,
            prefix="",
            is_last=True,
            segments=segments,
            highlighted_key=highlighted_key,
            is_root=True,
        )
        return segments

    def _build_segments(
        self,
        node: Node,
        prefix: str,
        is_last: bool,
        segments: list,
        highlighted_key: int | None,
        is_root: bool = False,
    ) -> None:
        """Đệ quy xây dựng các đoạn text cho từng node."""
        if node == self.NIL:
            return

        if is_root:
            # Root không có connector, không có prefix
            child_prefix = ""
        else:
            connector = "└── " if is_last else "├── "
            child_prefix = prefix + ("    " if is_last else "│   ")
            # Thêm phần cấu trúc (prefix + connector)
            if prefix:
                segments.append((prefix, "structure"))
            segments.append((connector, "structure"))

        # Xác định tag màu cho node
        is_highlighted = (highlighted_key is not None and node.key == highlighted_key)
        if is_highlighted:
            tag = "highlighted"
        elif node.color == RED:
            tag = "red_node"
        else:
            tag = "black_node"

        # Thêm icon + khóa node
        icon = "● "
        segments.append((f"{icon}{node.key}\n", tag))

        # Đệ quy cho các con
        has_left = node.left != self.NIL
        has_right = node.right != self.NIL

        if has_left and has_right:
            self._build_segments(node.left,  child_prefix, False, segments, highlighted_key)
            self._build_segments(node.right, child_prefix, True,  segments, highlighted_key)
        elif has_left:
            self._build_segments(node.left,  child_prefix, True, segments, highlighted_key)
        elif has_right:
            self._build_segments(node.right, child_prefix, True, segments, highlighted_key)

    def is_empty(self) -> bool:
        return self.root == self.NIL
