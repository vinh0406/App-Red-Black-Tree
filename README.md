# Hướng dẫn cài đặt, chạy App và Demo các chức năng của App 

## I. Hướng Dẫn Cài Đặt và Chạy App

### Yêu Cầu Hệ Thống
- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows, macOS, hoặc Linux

### Các Bước Cài Đặt

#### 1. Clone hoặc Tải Dự Án
```bash
cd app-red-black-tree
```

#### 2. Cài Đặt Các Thư Viện Phụ Thuộc
```bash
pip install -r requirements.txt
```

Hoặc nếu sử dụng `pip3`:
```bash
pip3 install -r requirements.txt
```

**Thư viện chính:**
- `customtkinter>=5.2.0` - Giao diện cho GUI

#### 3. Chạy Ứng Dụng
```bash
python app.py
```

Hoặc:
```bash
py app.py
```

Hoặc sử dụng `python3`:
```bash
python3 app.py
```
---

## II. Demo App

### 1. Giao Diện Tổng Quan

Giao diện tổng quan của app, cây Đỏ-Đen sẽ được minh hoạ trực quan và các node được minh hoạ màu, level và quan hệ cha con tương ứng. Thanh công cụ bên trái có các nút chức năng gồm **Nút tạo cây**, **Nút thêm khoá** và **Nút tìm kiếm**:

![Giao diện tổng quan](./imageDemo/Screenshot%202026-03-18%20213825.png)

---

### 2. Tạo Cây từ Tập Khóa và in cây trực quan

Thực hiện tạo cây từ tập khóa và cây được in ra trực quan:

![Tạo cây từ tập khóa](./imageDemo/Screenshot%202026-03-18%20213011.png)

---

### 3. Thêm Khóa Mới vào Cây và in cây trực quan

Thực hiện thêm khóa mới vào cây, cây được cập nhật ngay và in ra trực quan. Dòng thông báo trạng thái **"Đã thêm khoá thành công"** được hiển thị ở góc dưới bên trái:

![Thêm khóa mới](./imageDemo/Screenshot%202026-03-18%20213159.png)

---

### 4. Tìm Kiếm Khóa trên Cây và hiển thị trực quan

Thực hiện tìm kiếm khóa trên cây, khóa được tìm thấy sẽ được tô màu vàng. Đồng thời có thông báo trạng thái ở góc dưới bên trái gồm:
- Thông báo tìm thấy khóa
- Màu của node tìm thấy
- Độ sâu của node tìm thấy
- Đường đi từ node gốc đến node tìm thấy

![Tìm kiếm khóa](./imageDemo/Screenshot%202026-03-18%20213301.png)

---

## Chức Năng Chính

| Chức Năng | Mô Tả |
|-----------|-------|
| **Tạo Cây** | Tạo cây đỏ-đen từ một tập hợp khóa nhập vào |
| **Trực Quan Hóa** | Hiển thị cây với màu sắc phù hợp cho nodes đỏ/đen |
| **Thêm Khóa** | Chèn khóa mới vào cây với tự động cân bằng |
| **Tìm Kiếm** | Tìm kiếm khóa trên cây và hiển thị đường đi |

---