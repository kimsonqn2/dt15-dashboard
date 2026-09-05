"""
HỆ THỐNG GIÁM SÁT CÁC CHỈ SỐ MÔ PHỎNG ĐÔ THỊ (URBAN SIMULATION DASHBOARD)
Xây dựng bằng: Python (Streamlit), Plotly, Pandas, NumPy
Mục tiêu giám sát:
1. Tiến độ số hóa hồ sơ địa chính
2. Lưu lượng dữ liệu dự án DT15 (Hạ tầng dữ liệu số & cảm biến đô thị)
3. Tình trạng hoạt động của sàn giao dịch dữ liệu đô thị

Cách chạy:
    pip install streamlit plotly pandas numpy
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ thống Giám sát Mô phỏng Đô thị",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy chỉnh CSS để giao diện trực quan, đậm chất điều hành đô thị
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    .column-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        padding-bottom: 8px;
        border-bottom: 2px solid #cbd5e1;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar - Bộ lọc thời gian và điều khiển mô phỏng
st.sidebar.title("🎛️ Bảng Điều Khiển")
st.sidebar.markdown("---")

st.sidebar.subheader("⏳ Bộ lọc Thời gian")
time_filter = st.sidebar.selectbox(
    "Khoảng thời gian giám sát:",
    options=["Hôm nay (Thời gian thực)", "7 ngày qua", "30 ngày qua", "Quý III / 2026", "Tùy chỉnh khoảng ngày"],
    index=0
)

# Nếu người dùng chọn tùy chỉnh
if time_filter == "Tùy chỉnh khoảng ngày":
    col_d1, col_d2 = st.sidebar.columns(2)
    start_date = col_d1.date_input("Từ ngày", datetime.now() - timedelta(days=14))
    end_date = col_d2.date_input("Đến ngày", datetime.now())

district_filter = st.sidebar.selectbox(
    "Khu vực / Phân vùng mô phỏng:",
    options=["Toàn thành phố (Tổng hợp)", "TP. Thủ Đức", "Quận 1", "Quận Bình Thạnh", "Quận 7", "Huyện Bình Chánh"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Tham số Mô phỏng")
sim_speed = st.sidebar.select_slider(
    "Tốc độ luồng mô phỏng:",
    options=["0.5x", "1.0x (Chuẩn)", "2.0x", "5.0x"],
    value="1.0x (Chuẩn)"
)

refresh_rate = st.sidebar.selectbox(
    "Tự động làm mới dữ liệu:",
    options=["5 giây", "15 giây", "30 giây", "Thủ công"],
    index=1
)

if st.sidebar.button("🔄 Làm mới dữ liệu ngay", use_container_width=True):
    st.sidebar.success("Đã đồng bộ dữ liệu vi mô mới nhất!")

st.sidebar.markdown("---")
st.sidebar.caption("Hệ thống Mô phỏng Đô thị Thông minh v3.4 | Trung tâm Điều hành Dữ liệu Tập trung")

# 3. Tiêu đề và Thanh chỉ số tổng quan (Overview Metrics)
st.title("🏙️ HỆ THỐNG GIÁM SÁT CHỈ SỐ MÔ PHỎNG ĐÔ THỊ")
st.caption(f"Trạng thái: **Thời gian thực** | Phân vùng: **{district_filter}** | Khoảng thời gian: **{time_filter}**")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="📄 Tiến độ Số hóa Địa chính", value="84.6%", delta="+2.4% so với kỳ trước")
with kpi2:
    st.metric(label="📶 Thông lượng Dự án DT15", value="428.5 MB/s", delta="+34.2 MB/s cao điểm")
with kpi3:
    st.metric(label="🔄 Giao dịch Sàn Dữ liệu", value="14,892 lượt", delta="+12.8% trong ngày")
with kpi4:
    st.metric(label="🛡️ Tỷ lệ Sẵn sàng (SLA)", value="99.98%", delta="Bình thường (Healthy)")

st.write("")

# 4. BỐ CỤC 3 CỘT (3 COLUMNS LAYOUT THEO YÊU CẦU)
col1, col2, col3 = st.columns([1, 1, 1])

# =====================================================================
# CỘT 1: TIẾN ĐỘ SỐ HÓA HỒ SƠ ĐỊA CHÍNH
# =====================================================================
with col1:
    st.markdown('<div class="column-header">📂 1. Tiến độ Số hóa Hồ sơ Địa chính</div>', unsafe_allow_html=True)
    
    total_records = 1500000
    digitized_records = 1269000
    st.progress(digitized_records / total_records)
    st.caption(f"Đã xử lý: **{digitized_records:,} / {total_records:,}** thửa đất & hồ sơ (84.6%)")
    
    timeline_days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    scanned_data = [12400, 14200, 15800, 15100, 17200, 13400, 16900]
    verified_data = [11200, 13100, 14900, 14200, 16300, 12800, 15900]
    
    df_cadastral = pd.DataFrame({
        "Thời gian": timeline_days,
        "Đã quét & OCR": scanned_data,
        "Đã kiểm định pháp lý": verified_data
    })
    
    fig_cad = go.Figure()
    fig_cad.add_trace(go.Bar(x=df_cadastral["Thời gian"], y=df_cadastral["Đã quét & OCR"], name="Quét & OCR", marker_color="#3b82f6"))
    fig_cad.add_trace(go.Bar(x=df_cadastral["Thời gian"], y=df_cadastral["Đã kiểm định pháp lý"], name="Kiểm định pháp lý", marker_color="#10b981"))
    fig_cad.update_layout(
        title="Sản lượng số hóa hàng ngày (Hồ sơ)",
        barmode='group',
        height=280,
        margin=dict(l=10, r=10, t=35, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_cad, use_container_width=True)
    
    pie_labels = ["Đất ở đô thị", "Đất nông nghiệp", "Đất thương mại/dịch vụ", "Hạ tầng & công cộng"]
    pie_values = [520000, 410000, 219000, 120000]
    fig_pie = px.pie(
        values=pie_values,
        names=pie_labels,
        hole=0.45,
        color_discrete_sequence=["#2563eb", "#10b981", "#f59e0b", "#64748b"],
        title="Cơ cấu phân loại đất đã số hóa"
    )
    fig_pie.update_layout(height=240, margin=dict(l=10, r=10, t=35, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("**Tiến độ theo phân vùng trọng điểm:**")
    district_df = pd.DataFrame({
        "Quận/Huyện": ["TP. Thủ Đức", "Quận 1", "Q. Bình Thạnh", "Quận 7", "H. Bình Chánh"],
        "Tổng HS": ["420,000", "150,000", "210,000", "180,000", "320,000"],
        "Tỷ lệ": ["91.5%", "98.2%", "88.4%", "83.1%", "71.6%"]
    })
    st.dataframe(district_df, use_container_width=True, hide_index=True)


# =====================================================================
# CỘT 2: LƯU LƯỢNG DỮ LIỆU DỰ ÁN DT15
# =====================================================================
with col2:
    st.markdown('<div class="column-header">🌐 2. Lưu lượng Dữ liệu Dự án DT15</div>', unsafe_allow_html=True)
    
    hours = [f"{h:02d}:00" for h in range(0, 24, 2)]
    iot_traffic = [120, 95, 80, 75, 110, 180, 240, 265, 230, 210, 190, 150]
    gis_traffic = [50, 45, 40, 40, 60, 90, 120, 135, 110, 95, 80, 65]
    camera_traffic = [30, 25, 20, 20, 40, 85, 110, 120, 105, 90, 75, 50]
    
    df_dt15 = pd.DataFrame({
        "Giờ": hours,
        "IoT Sensors (Môi trường & Ngập)": iot_traffic,
        "Lớp dữ liệu GIS 3D / Không gian": gis_traffic,
        "Camera AI Giao thông": camera_traffic
    })
    
    fig_dt15 = go.Figure()
    fig_dt15.add_trace(go.Scatter(x=df_dt15["Giờ"], y=df_dt15["IoT Sensors (Môi trường & Ngập)"], mode='lines+markers', name='Cảm biến IoT', line=dict(color='#0284c7', width=2)))
    fig_dt15.add_trace(go.Scatter(x=df_dt15["Giờ"], y=df_dt15["Lớp dữ liệu GIS 3D / Không gian"], mode='lines+markers', name='Dữ liệu GIS 3D', line=dict(color='#8b5cf6', width=2)))
    fig_dt15.add_trace(go.Scatter(x=df_dt15["Giờ"], y=df_dt15["Camera AI Giao thông"], mode='lines+markers', name='Video AI', line=dict(color='#f97316', width=2)))
    fig_dt15.update_layout(
        title="Lưu lượng truyền tải DT15 (MB/s)",
        height=280,
        margin=dict(l=10, r=10, t=35, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_dt15, use_container_width=True)
    
    latency_values = [14.2, 12.8, 11.5, 11.0, 13.6, 19.4, 24.1, 26.5, 22.8, 18.2, 16.5, 15.0]
    fig_lat = px.area(
        x=hours,
        y=latency_values,
        labels={"x": "Khung giờ", "y": "Độ trễ (ms)"},
        title="Độ trễ truyền nhận vi mô (ms)",
        color_discrete_sequence=["#06b6d4"]
    )
    fig_lat.update_layout(height=240, margin=dict(l=10, r=10, t=35, b=10))
    st.plotly_chart(fig_lat, use_container_width=True)
    
    st.markdown("**Trạng thái các Gateway DT15:**")
    gateways_df = pd.DataFrame({
        "Trạm Gateway": ["DT15-Trung tâm", "DT15-Phía Đông", "DT15-Phía Nam", "DT15-Phía Bắc"],
        "Băng thông": ["182 MB/s", "114 MB/s", "86 MB/s", "46 MB/s"],
        "Tải CPU": ["54%", "41%", "33%", "26%"],
        "Trạng thái": ["🟢 Online", "🟢 Online", "🟢 Online", "🟢 Online"]
    })
    st.dataframe(gateways_df, use_container_width=True, hide_index=True)


# =====================================================================
# CỘT 3: TÌNH TRẠNG HOẠT ĐỘNG SÀN GIAO DỊCH DỮ LIỆU
# =====================================================================
with col3:
    st.markdown('<div class="column-header">📊 3. Hoạt động Sàn Giao dịch Dữ liệu</div>', unsafe_allow_html=True)
    
    tx_hours = [f"{h:02d}:00" for h in range(8, 20)]
    tx_counts = [420, 890, 1420, 1650, 1310, 1100, 1580, 1820, 1750, 1490, 980, 482]
    tx_volume = [12.4, 28.5, 45.1, 52.0, 39.8, 33.2, 49.5, 58.2, 54.0, 44.1, 29.6, 15.2]
    
    df_exchange = pd.DataFrame({
        "Giờ": tx_hours,
        "Số giao dịch (Khớp lệnh)": tx_counts,
        "Khối lượng dữ liệu (GB)": tx_volume
    })
    
    fig_tx = go.Figure()
    fig_tx.add_trace(go.Bar(x=df_exchange["Giờ"], y=df_exchange["Số giao dịch (Khớp lệnh)"], name="Giao dịch / Giờ", marker_color="#8b5cf6"))
    fig_tx.add_trace(go.Scatter(x=df_exchange["Giờ"], y=df_exchange["Khối lượng dữ liệu (GB)"], name="Khối lượng (GB)", yaxis="y2", line=dict(color="#f43f5e", width=2)))
    fig_tx.update_layout(
        title="Khối lượng giao dịch & Trao đổi dữ liệu",
        height=280,
        margin=dict(l=10, r=10, t=35, b=20),
        yaxis=dict(title="Lượt giao dịch"),
        yaxis2=dict(title="GB trao đổi", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_tx, use_container_width=True)
    
    st.markdown("**Chỉ số SLA & Sức khỏe dịch vụ Sàn:**")
    st.markdown("""
    - 🟢 **API Gateway:** Uptime **99.99%** | 22ms latency
    - 🟢 **Matching Engine:** Hoạt động bình thường
    - 🟢 **Smart Contract & Tokenizer:** 14,892 giao dịch hợp lệ
    - 🟢 **Sandbox Kiểm duyệt:** An toàn tuyệt đối
    """)
    
    st.markdown("**Top tập dữ liệu giao dịch sôi động:**")
    datasets_df = pd.DataFrame({
        "Tập Dữ Liệu": [
            "Bản đồ Quy hoạch 1/2000",
            "Mạng lưới Giao thông thời gian thực",
            "Vi khí hậu & Cảm biến Ngập lụt",
            "Mật độ Dân cư & Di động",
            "Hiện trạng Cấp thoát nước"
        ],
        "Lượt tải": ["4,120", "3,890", "2,940", "2,150", "1,792"],
        "Dung lượng": ["840 GB", "1.4 TB", "290 GB", "450 GB", "310 GB"]
    })
    st.dataframe(datasets_df, use_container_width=True, hide_index=True)
