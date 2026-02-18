import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="UKC Analysis Dashboard",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# MARITIME DARK THEME (Custom CSS)
# =============================================================================
st.markdown("""
<style>
/* === GOOGLE FONTS === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === MAIN BACKGROUND === */
.stApp {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 40%, #0a1a30 100%);
    font-family: 'Inter', sans-serif;
}

/* === HEADER === */
.main-header {
    background: linear-gradient(135deg, #0d2137 0%, #132d4a 50%, #0d2137 100%);
    border: 1px solid rgba(0, 212, 170, 0.15);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4aa, #0099ff, #00d4aa);
}
.main-header h1 {
    color: #e8f4f8;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.main-header .subtitle {
    color: #7eb8c9;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* === STATUS BANNER === */
.status-safe {
    background: linear-gradient(135deg, rgba(0, 212, 170, 0.12) 0%, rgba(0, 180, 140, 0.08) 100%);
    border: 1px solid rgba(0, 212, 170, 0.3);
    border-radius: 12px;
    padding: 14px 20px;
    color: #00d4aa;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 20px;
}
.status-danger {
    background: linear-gradient(135deg, rgba(255, 82, 82, 0.12) 0%, rgba(200, 50, 50, 0.08) 100%);
    border: 1px solid rgba(255, 82, 82, 0.3);
    border-radius: 12px;
    padding: 14px 20px;
    color: #ff5252;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 20px;
}

/* === METRIC CARDS === */
.metric-card {
    background: linear-gradient(135deg, #112240 0%, #0d1b2e 100%);
    border: 1px solid rgba(0, 153, 255, 0.15);
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: rgba(0, 212, 170, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 170, 0.1);
}
.metric-card .label {
    color: #5a8a9e;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.metric-card .value {
    color: #e8f4f8;
    font-size: 26px;
    font-weight: 700;
}
.metric-card .value.safe { color: #00d4aa; }
.metric-card .value.danger { color: #ff5252; }
.metric-card .value.info { color: #0099ff; }

/* === CHART SECTION === */
.chart-section {
    background: linear-gradient(135deg, #0d1e33 0%, #0a1628 100%);
    border: 1px solid rgba(0, 153, 255, 0.1);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.chart-title {
    color: #b8d4e3;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    padding-left: 4px;
    border-left: 3px solid #0099ff;
    padding-left: 12px;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0d1f3c 50%, #0a1628 100%);
    border-right: 1px solid rgba(0, 153, 255, 0.15);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #7eb8c9 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    background: rgba(13, 31, 60, 0.6) !important;
    border: 1px solid rgba(0, 153, 255, 0.15) !important;
    border-radius: 10px !important;
    color: #b8d4e3 !important;
}

/* === DATA TABLE === */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* === DIVIDER === */
hr {
    border-color: rgba(0, 153, 255, 0.1) !important;
    margin: 24px 0 !important;
}

/* === FOOTER === */
.footer-info {
    background: rgba(13, 31, 60, 0.5);
    border: 1px solid rgba(0, 153, 255, 0.1);
    border-radius: 10px;
    padding: 14px 20px;
    color: #5a8a9e;
    font-size: 13px;
    text-align: center;
}

/* Hide default Streamlit elements for cleaner look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Streamlit native metrics styling */
[data-testid="stMetricValue"] {
    color: #e8f4f8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMetricLabel"] {
    color: #5a8a9e !important;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MARITIME COLOR PALETTE (for charts)
# =============================================================================
COLORS = {
    "ocean":       "#0099ff",   # Xanh biển chính
    "teal":        "#00d4aa",   # Xanh ngọc (safe/positive)
    "coral":       "#ff5252",   # Đỏ san hô (danger)
    "amber":       "#ffb74d",   # Cam hổ phách (warning/required)
    "navy_bg":     "#0a1628",   # Nền tối navy
    "navy_card":   "#0d1e33",   # Nền card
    "navy_light":  "#132d4a",   # Navy nhạt
    "text_primary":"#e8f4f8",   # Chữ chính
    "text_muted":  "#5a8a9e",   # Chữ phụ
    "grid":        "rgba(0, 153, 255, 0.06)",  # Grid lines
    "gridline":    "rgba(0, 153, 255, 0.08)",
}

# Plotly chart template
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(10, 22, 40, 0.5)',
    font=dict(family='Inter', color=COLORS["text_muted"], size=12),
    margin=dict(l=50, r=20, t=10, b=45),
    legend=dict(
        bgcolor='rgba(13, 30, 51, 0.8)',
        bordercolor='rgba(0, 153, 255, 0.15)',
        borderwidth=1,
        font=dict(color=COLORS["text_primary"], size=11),
        x=0.01, y=0.99
    ),
    xaxis=dict(
        gridcolor=COLORS["gridline"],
        zerolinecolor=COLORS["gridline"],
        title_font=dict(color=COLORS["text_muted"], size=12),
        tickfont=dict(color=COLORS["text_muted"], size=10),
    ),
    yaxis=dict(
        gridcolor=COLORS["gridline"],
        zerolinecolor=COLORS["gridline"],
        title_font=dict(color=COLORS["text_muted"], size=12),
        tickfont=dict(color=COLORS["text_muted"], size=10),
    ),
    hoverlabel=dict(
        bgcolor=COLORS["navy_light"],
        font_size=13,
        font_family='Inter',
        bordercolor=COLORS["ocean"]
    ),
)

# =============================================================================
# DEFAULTS (từ Excel gốc)
# =============================================================================
DEFAULTS = {
    "vessel_name": "NORDSPRING", "imo": "9625346",
    "port": "Namdinhvu Port", "cargo_type": "Container",
    "loa": 208.0, "bt": 29.8, "tkt1": 9.5, "tkt2": 9.0, "dwt": 34800,
    "import_cont": 350, "export_cont": 364,
    "crane_rate": 28, "cranes": 2, "spare_cranes": 1,
    "aux_time": 1.0, "wait_time": 2.25, "draft_change_rate": 0.28,
    "bottom_elevation": -9.50, "op_water_level": 2.25, "total_hours": 48,
}

DEFAULT_TIDE = [
    2.8, 3.1, 3.3, 3.5, 3.5, 3.4, 3.2, 2.9, 2.6, 2.2,
    1.8, 1.5, 1.2, 1.0, 0.8, 0.7, 0.6, 0.5, 0.6, 0.8,
    1.0, 1.4, 1.8, 2.2, 2.6, 2.9, 3.2, 3.4, 3.5, 3.4,
    3.3, 3.1, 2.8, 2.5, 2.1, 1.8, 1.6, 1.3, 1.2, 1.0,
    0.9, 0.7, 0.6, 0.6, 0.7, 0.8, 0.9, 1.2,
]

# =============================================================================
# CALCULATION ENGINE
# =============================================================================
def calculate_tkt_series(tkt1, unload_time, load_time, wait_time, aux_time,
                          draft_change_rate, total_hours, berth_time):
    tkt = []
    t_phase_a_end = wait_time + aux_time / 2
    t_phase_b_end = t_phase_a_end + unload_time
    t_phase_c_start = t_phase_b_end
    t_phase_c_end = t_phase_c_start + load_time
    tkt_min = tkt1 - (unload_time * draft_change_rate)
    
    for h in range(total_hours):
        t = float(h)
        if t < t_phase_a_end:
            tkt.append(round(tkt1, 2))
        elif t < t_phase_b_end:
            elapsed = t - t_phase_a_end
            tkt.append(round(tkt1 - (elapsed * draft_change_rate), 2))
        elif t < t_phase_c_end:
            elapsed = t - t_phase_c_start
            tkt.append(round(tkt_min + (elapsed * draft_change_rate), 2))
        else:
            tkt_final = tkt_min + (load_time * draft_change_rate)
            tkt.append(round(tkt_final, 2))
    return tkt

def calculate_ukc(tide_list, tkt_list, bottom):
    return [round((w + abs(bottom)) - t, 2) for w, t in zip(tide_list, tkt_list)]

def calculate_ukc_required(tide_list, tkt_list, bottom, berth_time, total_hours):
    ukc_req = []
    for h in range(total_hours):
        req = 0.1 * tkt_list[h] if h < berth_time else 0.2 * tkt_list[h]
        ukc_req.append(round(req, 2))
    return ukc_req

# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.title("⚙️ Thông số đầu vào")

st.sidebar.header("🚢 I. Thông tin Tàu")
vessel_name = st.sidebar.text_input("Tên tàu", DEFAULTS["vessel_name"])
imo_number  = st.sidebar.text_input("Số IMO", DEFAULTS["imo"])
cargo_type  = st.sidebar.text_input("Loại hàng", DEFAULTS["cargo_type"])
col_v1, col_v2 = st.sidebar.columns(2)
with col_v1:
    tkt1 = st.sidebar.number_input("Tkt đến (m)", value=DEFAULTS["tkt1"], step=0.1, format="%.2f",
                                    help="Mớn nước tàu khi đến cảng")
with col_v2:
    loa = st.sidebar.number_input("LOA (m)", value=DEFAULTS["loa"], step=1.0, format="%.0f")

st.sidebar.markdown("---")
st.sidebar.header("📦 II. Hàng hóa")
col_c1, col_c2 = st.sidebar.columns(2)
with col_c1:
    import_cont = st.sidebar.number_input("Import (cont)", value=DEFAULTS["import_cont"], step=10,
                                           help="Số container dỡ → ảnh hưởng thời gian dỡ & mớn nước")
with col_c2:
    export_cont = st.sidebar.number_input("Export (cont)", value=DEFAULTS["export_cont"], step=10,
                                           help="Số container xếp → ảnh hưởng thời gian xếp & mớn nước")

st.sidebar.markdown("---")
st.sidebar.header("⏱️ III. Khai thác")
col_o1, col_o2 = st.sidebar.columns(2)
with col_o1:
    crane_rate = st.sidebar.number_input("Công suất/cẩu (cont/h)", value=DEFAULTS["crane_rate"], step=1)
with col_o2:
    cranes = st.sidebar.number_input("Số cẩu", value=DEFAULTS["cranes"], step=1, min_value=1)

throughput = crane_rate * cranes
unload_time = round(import_cont / throughput, 2) if throughput > 0 else 0
load_time = round(export_cont / throughput, 2) if throughput > 0 else 0

aux_time = st.sidebar.number_input("Thao tác phụ (h)", value=DEFAULTS["aux_time"], step=0.25)
wait_time = st.sidebar.number_input("Thời gian chờ (h)", value=DEFAULTS["wait_time"], step=0.25)
draft_change = st.sidebar.number_input("ΔTkt /h (m)", value=DEFAULTS["draft_change_rate"], step=0.01, format="%.4f",
                                        help="Mớn nước khai thác thay đổi mỗi giờ")

berth_time = round(wait_time + aux_time + unload_time + load_time, 2)

st.sidebar.markdown("---")
st.sidebar.markdown("📐 **Kết quả tính toán:**")
st.sidebar.markdown(f"""
| Thông số | Giá trị |
|----------|--------:|
| Công suất tổng | **{throughput}** cont/h |
| TG dỡ hàng | **{unload_time:.2f}** h |
| TG xếp hàng | **{load_time:.2f}** h |
| TG tại cầu | **{berth_time:.2f}** h |
| ΔTkt dỡ | **{unload_time * draft_change:.2f}** m |
| ΔTkt xếp | **{load_time * draft_change:.2f}** m |
""")

st.sidebar.markdown("---")
st.sidebar.header("🌊 IV. Cảng & Luồng")
bottom = st.sidebar.number_input("Cao độ đáy (m, HĐ)", value=DEFAULTS["bottom_elevation"], step=0.1, format="%.2f")
op_water = st.sidebar.number_input("MN khai thác (m)", value=DEFAULTS["op_water_level"], step=0.1, format="%.2f")
total_hours = st.sidebar.number_input("Tổng giờ mô phỏng", value=DEFAULTS["total_hours"], step=1, min_value=10, max_value=96)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset tất cả về mặc định", use_container_width=True):
    st.rerun()

# =============================================================================
# CALCULATIONS
# =============================================================================
hours = list(range(total_hours))

tide_data = DEFAULT_TIDE.copy()
while len(tide_data) < total_hours:
    tide_data.extend(DEFAULT_TIDE)
tide_data = tide_data[:total_hours]

tkt_series = calculate_tkt_series(tkt1, unload_time, load_time, wait_time, aux_time,
                                   draft_change, total_hours, berth_time)
ukc_actual = calculate_ukc(tide_data, tkt_series, bottom)
ukc_req = calculate_ukc_required(tide_data, tkt_series, bottom, berth_time, total_hours)
cd_ukc_actual = [bottom + u for u in ukc_actual]
keel_line = [w - t for w, t in zip(tide_data, tkt_series)]

min_ukc = min(ukc_actual)
max_ukc = max(ukc_actual)
violations = sum(1 for a, r in zip(ukc_actual, ukc_req) if a < r)

# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"""
<div class="main-header">
    <h1>⚓ UKC Analysis Dashboard</h1>
    <div class="subtitle">
        Tàu: <strong>{vessel_name}</strong> &nbsp;|&nbsp; IMO: {imo_number} &nbsp;|&nbsp;
        DWT: {DEFAULTS['dwt']:,} MT &nbsp;|&nbsp; Hàng: {cargo_type} &nbsp;|&nbsp;
        Cảng: Nam Đình Vũ &nbsp;|&nbsp; LOA: {loa:.0f}m
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# STATUS BANNER
# =============================================================================
if violations == 0:
    st.markdown(f"""
    <div class="status-safe">
        ✅ AN TOÀN — UKC min ({min_ukc:.2f}m) luôn ≥ UKC yêu cầu trong toàn bộ {total_hours} giờ
        &nbsp;&nbsp;|&nbsp;&nbsp; Tổng hàng: {import_cont + export_cont} cont
        &nbsp;&nbsp;|&nbsp;&nbsp; Thời gian tại cầu: {berth_time:.1f}h
    </div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-danger">
        ❌ CẢNH BÁO — Có {violations}/{total_hours} giờ UKC thực tế < UKC yêu cầu!
        &nbsp;&nbsp;|&nbsp;&nbsp; UKC min: {min_ukc:.2f}m
        &nbsp;&nbsp;|&nbsp;&nbsp; Cần kiểm tra lại thông số!
    </div>""", unsafe_allow_html=True)

# =============================================================================
# METRIC CARDS
# =============================================================================
cols = st.columns(5)
metrics = [
    ("UKC MIN", f"{min_ukc:.2f} m", "danger" if violations > 0 else "safe"),
    ("UKC MAX", f"{max_ukc:.2f} m", "safe"),
    ("CAO ĐỘ ĐÁY", f"{bottom:.2f} m", "info"),
    ("CÔNG SUẤT", f"{throughput} c/h", "info"),
    ("VI PHẠM", f"{violations}/{total_hours}", "danger" if violations > 0 else "safe"),
]
for col, (label, value, style) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value {style}">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# DATA TABLE (Expandable)
# =============================================================================
with st.expander("📝 Xem bảng dữ liệu chi tiết", expanded=False):
    table_df = pd.DataFrame({
        "Giờ": hours, "Mực nước (m)": tide_data, "Tkt (m)": tkt_series,
        "UKC thực tế (m)": ukc_actual, "UKC yêu cầu (m)": ukc_req,
    })
    st.dataframe(table_df, use_container_width=True, hide_index=True)

# =============================================================================
# CHART 1: UKC ACTUAL AREA
# =============================================================================
st.markdown('<div class="chart-section"><div class="chart-title">📈 BIỂU ĐỒ 1 — Vùng Dự Phòng An Toàn (UKC Area)</div>', unsafe_allow_html=True)

fig1 = go.Figure()

# Danger zone (below required)
fig1.add_trace(go.Scatter(x=hours, y=ukc_req, mode='lines', name='Vùng nguy hiểm',
    line=dict(width=0), showlegend=False))
fig1.add_trace(go.Scatter(x=hours, y=[0]*total_hours, mode='lines', name='Vùng nguy hiểm',
    line=dict(width=0), fill='tonexty',
    fillcolor='rgba(255, 82, 82, 0.08)', showlegend=False))

# Safe zone (UKC actual)
fig1.add_trace(go.Scatter(x=hours, y=ukc_actual, mode='lines', name='UKC Thực tế',
    line=dict(color=COLORS["teal"], width=2.5, shape='spline'),
    fill='tozeroy', fillcolor='rgba(0, 212, 170, 0.1)'))

# Required line
fig1.add_trace(go.Scatter(x=hours, y=ukc_req, mode='lines', name='UKC Yêu cầu',
    line=dict(color=COLORS["amber"], width=2, dash='dash')))

# Annotations for min/max
min_idx = ukc_actual.index(min_ukc)
fig1.add_annotation(x=min_idx, y=min_ukc, text=f"Min: {min_ukc:.2f}m",
    showarrow=True, arrowhead=2, arrowcolor=COLORS["coral"],
    font=dict(color=COLORS["coral"], size=11), bgcolor=COLORS["navy_card"],
    bordercolor=COLORS["coral"], borderwidth=1)

fig1.update_layout(**CHART_LAYOUT, height=320,
    xaxis_title="Thời gian (giờ)", yaxis_title="UKC (m)")
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# CHART 2: OVERVIEW (Water Level - Keel - Bottom)
# =============================================================================
st.markdown('<div class="chart-section"><div class="chart-title">🌊 BIỂU ĐỒ 2 — Tổng Quát (Thủy Triều – Keel – Đáy)</div>', unsafe_allow_html=True)

fig2 = go.Figure()

# Water surface area
fig2.add_trace(go.Scatter(x=hours, y=tide_data, mode='lines', name='Mực nước',
    line=dict(color=COLORS["ocean"], width=2, shape='spline'),
    fill='tozeroy', fillcolor='rgba(0, 153, 255, 0.08)'))

# Keel line
fig2.add_trace(go.Scatter(x=hours, y=keel_line, mode='lines', name='Keel tàu',
    line=dict(color=COLORS["coral"], width=2, shape='spline')))

# Seabed
fig2.add_trace(go.Scatter(x=hours, y=[bottom]*total_hours, mode='lines',
    name=f'Đáy biển ({bottom:.2f}m)',
    line=dict(color='#8B6914', width=2.5),
    fill='tozeroy', fillcolor='rgba(139, 105, 20, 0.1)'))

fig2.update_layout(**CHART_LAYOUT, height=320,
    xaxis_title="Thời gian (giờ)", yaxis_title="Cao độ (m, HĐ)",
    yaxis_range=[-12, 5])
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# CHARTS 3 & 4 SIDE BY SIDE
# =============================================================================
col_left, col_right = st.columns(2)

# --- CHART 3: BAR CHART ---
with col_left:
    st.markdown('<div class="chart-section"><div class="chart-title">📊 BIỂU ĐỒ 3 — UKC Theo Giờ</div>', unsafe_allow_html=True)
    
    bar_colors = [COLORS["coral"] if u < r else COLORS["teal"] for u, r in zip(ukc_actual, ukc_req)]
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=hours, y=ukc_actual, name='UKC',
        marker_color=bar_colors, marker_line_width=0, opacity=0.85))
    fig3.add_trace(go.Scatter(x=hours, y=ukc_req, mode='lines', name='Required',
        line=dict(color=COLORS["amber"], width=2.5, dash='dash')))
    
    fig3.update_layout(**CHART_LAYOUT, height=350,
        xaxis_title="Giờ", yaxis_title="UKC (m)", bargap=0.12)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHART 4: TKT + UKC ---
with col_right:
    st.markdown('<div class="chart-section"><div class="chart-title">⚓ BIỂU ĐỒ 4 — Mớn Nước & UKC</div>', unsafe_allow_html=True)
    
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=hours, y=tkt_series, mode='lines+markers',
        name='Tkt Thực Tế', line=dict(color=COLORS["ocean"], width=2.5, shape='spline'),
        marker=dict(size=4, color=COLORS["ocean"])))
    fig4.add_trace(go.Scatter(x=hours, y=ukc_actual, mode='lines',
        name='UKC Thực Tế', line=dict(color=COLORS["teal"], width=2, shape='spline')))
    fig4.add_trace(go.Scatter(x=hours, y=ukc_req, mode='lines',
        name='UKC Required', line=dict(color=COLORS["coral"], width=2, dash='dash')))
    
    fig4.update_layout(**CHART_LAYOUT, height=350,
        xaxis_title="Thời gian (giờ)", yaxis_title="Tkt(m) / UKC(m)",
        yaxis_range=[0, max(tkt_series) + 1])
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown(f"""
<div class="footer-info">
    💡 Thay đổi thông số ở thanh bên trái → biểu đồ cập nhật ngay lập tức
    &nbsp;&nbsp;|&nbsp;&nbsp;
    📊 Dữ liệu gốc: 260217_3. Bai toan van chuyen -xep do.xlsx
    &nbsp;&nbsp;|&nbsp;&nbsp;
    ⚓ UKC Analysis Dashboard v2.0
</div>
""", unsafe_allow_html=True)
