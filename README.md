# Dự Án Mô Phỏng 3 Vật Thể Chuyển Động Trong Không Gian

Hoàn thiện dự án mô phỏng 3 vật thể với kiến trúc chuyên nghiệp (PyQt6 + ModernGL + NumPy), chúng ta sẽ hệ thống lại thành một quy trình phát triển chuẩn (Software Development Lifecycle). Dưới đây là bản lộ trình chi tiết từ thiết kế đến đóng gói.

## 1. Thiết Lập Cấu Trúc Thư Mục Dự Án

Một dự án chuyên nghiệp cần sự ngăn nắp để dễ bảo trì và mở rộng.

```
ThreeBodySim/
├── assets/              # Chứa Texture (hành tinh, skybox), Icons UI
├── shaders/             # Các file GLSL (.vert, .frag)
├── src/
│   ├── core/            # Lõi tính toán vật lý (RK4, Vector math)
│   ├── ui/              # Các class giao diện PyQt6
│   ├── renderer/        # Xử lý ModernGL (VBO, VAO, Shaders)
│   └── main.py          # Điểm khởi chạy chương trình
├── requirements.txt     # Danh sách thư viện
└── README.md
```

## 2. Xây Dựng Lõi Vật Lý (Physics Engine)

Để đạt độ chính xác cao và tương tác mượt mà, bạn cần tập trung vào:

- **Sử Dụng NumPy**: Tính toán toàn bộ lực hấp dẫn dưới dạng ma trận. Thay vì dùng vòng lặp for, hãy dùng các phép toán Vector trên mảng NumPy để tận dụng tốc độ của C chạy dưới nền.
- **Thuật Toán RK4 (Runge-Kutta Bậc 4)**: Chia mỗi bước thời gian \(dt\) thành 4 bước nhỏ để ước tính độ dốc. Điều này cực kỳ quan trọng: Nó giúp các vật thể không bị "văng" khỏi quỹ đạo một cách vô lý sau 1-2 phút mô phỏng.

## 3. Quy Trình Rendering Chuyên Nghiệp (ModernGL)

Thay vì vẽ trực tiếp, bạn sẽ làm việc với luồng dữ liệu của GPU:

- **Buffer Management**: Tạo các Vertex Buffer để lưu tọa độ. Trong mô phỏng 3 vật thể, tọa độ này thay đổi liên tục, vì vậy bạn cần dùng `dynamic=True` khi khởi tạo buffer.
- **Shaders Custom**:
  - **Vertex Shader**: Tính toán vị trí của từng hành tinh trong không gian 3D dựa trên ma trận Camera (Model-View-Projection).
  - **Fragment Shader**: Đây là nơi tạo nên vẻ chuyên nghiệp. Bạn có thể viết code để tạo hiệu ứng Phong Lighting (độ bóng) hoặc Fresnel Effect (viền sáng quanh hành tinh).
- **Skybox Rendering**: Vẽ một khối hộp khổng lồ bao quanh hệ thống với texture dải ngân hà để tạo cảm giác vô tận.

## 4. Giao Diện Và Tương Tác (PyQt6 Bridge)

Đây là phần "giao tiếp" với người dùng:

- **QDockWidget**: Sử dụng loại widget này cho bảng điều khiển bên cạnh. Người dùng có thể tháo rời hoặc ghim nó vào các cạnh màn hình tùy ý.
- **Signals & Slots**: Khi người dùng thay đổi giá trị trên Slider (khối lượng, tốc độ), phát một `pyqtSignal`. GLWidget sẽ "nghe" tín hiệu này và cập nhật biến số vào vòng lặp vật lý ngay lập tức.
- **Cơ Chế Click-to-Select**: Sử dụng kỹ thuật Raycasting: Bắn một tia từ vị trí chuột qua ống kính camera vào không gian 3D. Nếu tia này cắt qua vùng va chạm của vật thể, hiển thị khung bao quanh (Selection Outline) và mở bảng thuộc tính của vật thể đó.

## 5. Danh Sách Kiểm Tra Hoàn Thiện (Final Checklist)

### Yêu Cầu Về UI/UX:
- [ ] Có nút Reset Simulation để đưa 3 vật thể về vị trí ban đầu.
- [ ] Có tính năng Time Scale (điều chỉnh vận tốc thời gian).
- [ ] Hiển thị thông số thời gian thực (FPS, Tọa độ \(x,y,z\)).
- [ ] Chế độ Full Screen để trình diễn.

### Yêu Cầu Về Đồ Họa:
- [ ] Có hiệu ứng Orbital Trails (đường mòn quỹ đạo) để thấy được hình dáng chuyển động.
- [ ] Ánh sáng có độ tương phản cao (Dark space theme).
- [ ] Texture hành tinh sắc nét (2K trở lên).

## 6. Hướng Dẫn Đóng Gói

Để phần mềm của bạn trông giống một sản phẩm thương mại:

- **Sử Dụng PyInstaller**: Đóng gói toàn bộ code và thư viện thành một file .exe duy nhất.
- **Tạo Icon**: Thiết kế file .ico chuyên nghiệp cho phần mềm.
- **Resource Compilation**: Sử dụng file .qrc của Qt để nén toàn bộ Shader và hình ảnh vào trong file thực thi, tránh việc người dùng vô tình xóa mất file assets.

## Bước Tiếp Theo

Bạn muốn bắt đầu xây dựng module nào đầu tiên? Tôi có thể hướng dẫn chi tiết cách thiết lập Lõi vật lý RK4 với NumPy hoặc cách cấu trúc GLWidget trong PyQt6 để bắt đầu vẽ những điểm đầu tiên lên màn hình.