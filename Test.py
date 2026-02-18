import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

# =============================================================================
# 1. KHỞI TẠO DỮ LIỆU TỪ FILE EXCEL
# =============================================================================
# Thời gian (47 giờ - trích xuất từ Excel)
hours = list(range(47))

# Mực nước thủy triều (MN thủy triều)
tide_level = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    7.52, 7.8, 8.08, 8.37, 8.65, 8.93, 9.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0
]

# Các tham số cố định
operational_water_level = 2.25  # Mực nước khai thác (m)
bottom_elevation = -8.55         # Cao độ đáy (m) - cập nhật từ Excel

# UKC thực tế (tính từ dữ liệu)
ukc_actual = [
    6.4, 6.2, 6.0, 6.0, 6.1, 6.3, 6.6, 6.9, 7.3, 7.42, 7.43, 7.45, 7.37, 7.28, 
    7.1, 6.92, 7.3, 7.48, 7.57, 7.65, 7.53, 7.42, 7.02, 6.62, 6.32, 6.02, 5.82, 
    5.72, 5.82, 5.92, 6.12, 6.42, 6.72, 7.12, 7.42, 7.62, 7.92, 8.02, 8.22, 8.32, 
    8.52, 8.62, 8.62, 8.52, 8.42, 8.32, 8.02
]

# [UKC] - Yêu cầu tối thiểu
ukc_required = [
    7.6, 7.6, 7.6, 7.6, 7.6, 7.6, 7.6, 8.55, 8.55, 8.58, 8.61, 8.63, 8.66, 8.69, 
    8.72, 8.75, 8.72, 8.69, 8.66, 8.63, 8.61, 8.58, 7.66, 7.66, 7.66, 7.66, 7.66, 
    7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 
    7.66, 7.66, 7.66, 7.66, 7.66, 7.66, 7.66
]

# =============================================================================
# 2. THIẾT LẬP BIỂU ĐỒ
# =============================================================================
fig = plt.figure(figsize=(16, 10), dpi=100, facecolor='white')
gs = GridSpec(2, 1, height_ratios=[1.2, 1], hspace=0.08)

# --- PANEL 1: MỰC NƯỚC THỦY TRIỀU (TRÊN) ---
ax1 = fig.add_subplot(gs[0])

# Đường SIN: Mực nước thủy triều
ax1.plot(hours, tide_level, color='#1f77b4', linewidth=2.5, label='Mực nước thủy triều', zorder=3)
ax1.fill_between(hours, tide_level, alpha=0.15, color='#1f77b4')

# Đường thẳng: Mực nước khai thác
ax1.axhline(y=operational_water_level, color='#ff7f0e', linestyle='--', linewidth=1.5, 
            label=f'Mực nước khai thác ({operational_water_level}m)', zorder=2)

# Config Panel 1
ax1.set_ylabel('Mực nước (m)', fontsize=11, fontweight='bold')
ax1.set_title('BIỂU ĐỒ VẬN HÀNH TÀU - NORDSPRING | Namdinhvu Port', 
              fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.set_axisbelow(True)
ax1.set_ylim(0, 12)  # Cập nhật giới hạn Y cho thủy triều thực tế
ax1.set_xlim(0, 46)  # 47 mốc thời gian (0-46)
ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax1.tick_params(labelbottom=False)  # Ẩn label x ở panel trên

# Highlight vùng an toàn/không an toàn
for i, (t, req) in enumerate(zip(tide_level, ukc_required)):
    if t - 9.5 < req:  # UKC thực tế < yêu cầu
        ax1.axvspan(i-0.5, i+0.5, alpha=0.1, color='red')

# --- PANEL 2: UKC (DƯỚI) ---
ax2 = fig.add_subplot(gs[1], sharex=ax1)

# Đường UKC thực tế
ax2.plot(hours, ukc_actual, color='#2ca02c', linewidth=2.5, label='UKC thực tế', zorder=3)
ax2.fill_between(hours, ukc_actual, alpha=0.15, color='#2ca02c')

# Đường thẳng: [UKC] yêu cầu tối thiểu
ax2.plot(hours, ukc_required, color='#d62728', linestyle='-.', linewidth=2, 
         label='[UKC] yêu cầu', zorder=2)

# Đường thẳng: Cao độ đáy (reference)
ax2.axhline(y=0, color='gray', linestyle=':', linewidth=0.5, alpha=0.3)

# Config Panel 2
ax2.set_xlabel('Thời gian (giờ)', fontsize=11, fontweight='bold')
ax2.set_ylabel('UKC (m)', fontsize=11, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.set_axisbelow(True)
ax2.set_ylim(0, 10)  # Cập nhật giới hạn Y cho UKC thực tế
ax2.legend(loc='upper right', fontsize=9, framealpha=0.9)

# Highlight vùng cảnh báo UKC
for i, (actual, req) in enumerate(zip(ukc_actual, ukc_required)):
    if actual < req:
        ax2.axvspan(i-0.5, i+0.5, alpha=0.2, color='red', label='Cảnh báo' if i==0 else "")

# =============================================================================
# 3. HOÀN THIỆN & XUẤT FILE
# =============================================================================
# Thêm annotation thông tin tàu
fig.text(0.5, 0.96, 
         f'Tàu: NORDSPRING | IMO: 9625346 | DWT: 34,800 MT | Hàng: Container',
         ha='center', fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Thêm legend cho đường đáy ở panel dưới
ax2.text(45, 0.3, f'Cao độ đáy: {bottom_elevation}m', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

plt.tight_layout()
plt.savefig('vessel_operation_chart.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Biểu đồ đã được tạo thành công! File lưu tại: vessel_operation_chart.png")