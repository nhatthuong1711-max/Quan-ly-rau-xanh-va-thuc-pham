import streamlit as st
import pandas as pd
import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Điều Phối Rau Xanh Liên Đơn Vị",
    page_icon="🥦",
    layout="wide"
)

# -------------------------------------------------------------------
# KHO TRUY CẬP & PHÂN QUYỀN (SESSION STATE)
# -------------------------------------------------------------------

# Khởi tạo danh sách tài khoản hệ thống trong Session State
if 'accounts' not in st.session_state:
    st.session_state.accounts = {
        "name": "Trung tá Nguyễn Thiên Vương",
            "role": "Chủ nhiệm Hậu Cần Kỹ Thuật",
            "pass": "123456",
            "unit": "Phòng Hậu Cần Kỹ Thuật",
            "icon": "👑"
     
            "name": "Trung uý Trần Hoài Nam",
            "role": "Trợ lý hậu cần",
            "pass": "123456",
            "unit": "Đơn vị 1 (Tiểu đoàn 1)",
            "unit_id": "Đơn vị 1",
            "icon": "🏢"

            "name": "Trung úy Lâm Đình Thưởng",
            "role": "Trợ lý hậu cần",
            "pass": "123456",
            "unit": "Đơn vị 2 (Tiểu đoàn 2)",
            "unit_id": "Đơn vị 2",
            "icon": "🏢"
     
            "name": "Thiếu úy Lê Văn Bằng",
            "role": "Trợ lý hậu cần",
            "pass": "123456",
            "unit": "Đơn vị 3 (Tiểu đoàn 3)",
            "unit_id": "Đơn vị 3",
            "icon": "🏢"
        }
    }

ACCOUNTS = st.session_state.accounts

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.current_user = None

# Khởi tạo dữ liệu kho mẫu theo từng Đơn vị
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"ID": "R001", "Đơn vị quản lý": "Đơn vị 1", "Tên rau": "Rau muống", "Nhóm": "Rau ăn lá", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 150.0, "Chất lượng": "Loại A (Tươi)", "Trạng thái": "Thừa 40kg (Sẵn sàng điều phối)", "Ngày nhập": datetime.date(2026, 9, 26), "Hạn dùng (ngày)": 3},
        {"ID": "R002", "Đơn vị quản lý": "Đơn vị 1", "Tên rau": "Bí đỏ", "Nhóm": "Rau củ quả", "Nguồn": "Thu mua ngoài", "Khối lượng (kg)": 80.0, "Chất lượng": "Loại A (Tươi)", "Trạng thái": "Vừa đủ", "Ngày nhập": datetime.date(2026, 9, 25), "Hạn dùng (ngày)": 20},
        {"ID": "R003", "Đơn vị quản lý": "Đơn vị 2", "Tên rau": "Cải ngọt", "Nhóm": "Rau ăn lá", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 30.0, "Chất lượng": "Loại B (Trung bình)", "Trạng thái": "Thiếu 50kg (Cần chi viện)", "Ngày nhập": datetime.date(2026, 9, 25), "Hạn dùng (ngày)": 2},
        {"ID": "R004", "Đơn vị quản lý": "Đơn vị 2", "Tên rau": "Su su", "Nhóm": "Rau củ quả", "Nguồn": "Thu mua ngoài", "Khối lượng (kg)": 120.0, "Chất lượng": "Loại A (Tươi)", "Trạng thái": "Vừa đủ", "Ngày nhập": datetime.date(2026, 9, 24), "Hạn dùng (ngày)": 10},
        {"ID": "R005", "Đơn vị quản lý": "Đơn vị 3", "Tên rau": "Rau dền", "Nhóm": "Rau ăn lá", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 25.0, "Chất lượng": "Loại C (Cần dùng ngay)", "Trạng thái": "Thiếu 30kg (Cần chi viện)", "Ngày nhập": datetime.date(2026, 9, 24), "Hạn dùng (ngày)": 1},
        {"ID": "R006", "Đơn vị quản lý": "Đơn vị 3", "Tên rau": "Bắp cải", "Nhóm": "Rau ăn lá", "Nguồn": "Thu mua ngoài", "Khối lượng (kg)": 200.0, "Chất lượng": "Loại A (Tươi)", "Trạng thái": "Thừa 60kg (Sẵn sàng điều phối)", "Ngày nhập": datetime.date(2026, 9, 26), "Hạn dùng (ngày)": 7}
    ])

# Khởi tạo lịch sử điều phối liên đơn vị
if 'transfer_history' not in st.session_state:
    st.session_state.transfer_history = pd.DataFrame([
        {
            "Mã ĐP": "DP001",
            "Đơn vị xuất": "Đơn vị 1",
            "Đơn vị nhận": "Đơn vị 2",
            "Tên rau": "Rau muống",
            "Khối lượng (kg)": 30.0, "Người duyệt": "Thượng tá Nguyễn Văn Hùng",
            "Ngày điều phối": datetime.date(2026, 9, 27),
            "Trạng thái": "Đã hoàn thành",
            "Đánh giá chất lượng": "Chất lượng tốt (Loại A)"
        }
    ])

# Khởi tạo danh sách đề xuất điều phối từ các đơn vị
if 'transfer_requests' not in st.session_state:
    st.session_state.transfer_requests = pd.DataFrame([
        {
            "Mã YC": "DX001",
            "Đơn vị đề xuất": "Đơn vị 2",
            "Loại yêu cầu": "Xin chi viện (Thiếu)",
            "Tên rau": "Rau ăn lá (Cải / Muống)",
            "Khối lượng (kg)": 50.0,
            "Lý do": "Tăng gia đợt này bị ảnh hưởng do mưa lớn",
            "Ngày gửi": datetime.date(2026, 9, 27),
            "Trạng thái": "Chờ Tổng Quản Lý duyệt"
        }
    ])

# Khởi tạo Trung tâm Thông báo Nội bộ
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {
            "id": 1,
            "sender": "Thượng tá Nguyễn Văn Hùng (Tổng Quản Lý)",
            "target": "Tất cả đơn vị",
            "content": "Yêu cầu các Đơn vị 1, 2, 3 rà soát ngay lượng rau ăn lá tồn kho để sẵn sàng điều phối hỗ trợ lẫn nhau.",
            "time": "2026-09-27 08:30",
            "read_by": []
        }
    ]

# -------------------------------------------------------------------
# GIAO DIỆN ĐĂNG NHẬP / PHÂN QUYỀN
# -------------------------------------------------------------------
if not st.session_state.authenticated:
    st.title("🥦 HỆ THỐNG ĐIỀU PHỐI RAU XANH LIÊN ĐƠN VỊ")
    st.markdown("### 🔑 Đăng Nhập Quản Lý & Điều Phối 3 Đơn Vị")
    
    col_login, col_demo = st.columns([1.2, 1])
    
    with col_login:
        with st.form("login_form"):
            st.subheader("Đăng Nhập Tài Khoản")
            username = st.text_input("Tên đăng nhập", value="admin")
            password = st.text_input("Mật khẩu", type="password", value="123456")
            submit_login = st.form_submit_button("🔓 Đăng Nhập")
            
            if submit_login:
                if username in ACCOUNTS and ACCOUNTS[username]["pass"] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.success(f"Đăng nhập thành công! Chào mừng {ACCOUNTS[username]['name']}")
                    st.rerun()
                else:
                    st.error("Mật khẩu hoặc tên đăng nhập không đúng!")

    with col_demo:
        st.subheader("⚡ Đăng Nhập Nhanh (Demo Vai Trò)")
        st.info("Chọn vai trò điều phối để trải nghiệm giao diện:")
        
        for acc_id, acc_info in ACCOUNTS.items():
            btn_label = f"{acc_info['icon']} {acc_info['role'].upper()}: {acc_info['name']} ({acc_info['unit']})"
            if st.button(btn_label, key=f"btn_demo_{acc_id}"):
                st.session_state.authenticated = True
                st.session_state.current_user = acc_id
                st.rerun()

    st.stop()

# -------------------------------------------------------------------
# XỬ LÝ KHI ĐÃ ĐĂNG NHẬP
# -------------------------------------------------------------------
user_data = ACCOUNTS[st.session_state.current_user]
user_role = user_data["role"]
user_name = user_data["name"]
user_unit = user_data["unit"]
user_unit_id = user_data.get("unit_id", "Tổng")

# Thông báo chưa đọc của user hiện tại
my_unread_count = sum(1 for note in st.session_state.notifications if (note["target"] == "Tất cả đơn vị" or note["target"] == user_unit_id or user_role == "Tổng Quản Lý") and st.session_state.current_user not in note["read_by"])

# Sidebar Thông tin Tài khoản & Đăng xuất
st.sidebar.markdown(f"### {user_data['icon']} ĐANG ĐĂNG NHẬP")
st.sidebar.success(f"**{user_name}**\n\n📌 **Vai trò**: {user_role}\n\n🏢 **Cơ quan**: {user_unit}")

if my_unread_count > 0:
    st.sidebar.warning(f"🔔 Bạn có **{my_unread_count}** thông báo mới chưa đọc!")

if st.sidebar.button("🚪 Đăng Xuất"):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

st.sidebar.divider()

# Tiêu đề chung
st.title("🥦 HỆ THỐNG QUẢN LÝ & ĐIỀU PHỐI RAU XANH LIÊN ĐƠN VỊ")
st.caption(f"Mô hình điều phối 3 Đơn vị | Tài khoản: **{user_name}** ({user_role} - {user_unit})")

# -------------------------------------------------------------------
# MENU THEO VAI TRÒ
# -------------------------------------------------------------------
if user_role == "Tổng Quản Lý":
    menu_options = [
        "📊 Dashboard Tổng Quan 3 Đơn Vị", 
        "🔄 Lập Lệnh Điều Phối Liên Đơn Vị", 
        "📋 Duyệt Đề Xuất Thừa / Thiếu Rau",
        "📦 Quản Lý Kho Rau Toàn Hệ Thống",
        "🔔 Trung Tâm Thông Báo Chỉ Đạo",
        "⚙️ Quản Lý Cài Đặt Tài Khoản 3 Đơn Vị"
    ]
else: # Quản lý Đơn vị
    menu_options = [
        "📊 Bảng Theo Dõi Kho Rau Đơn Vị", 
        "📥 Nhập Rau Tăng Gia / Thu Mua Kho Đơn Vị",
        "📢 Khai Báo Thừa / Thiếu & Đề Xuất Điều Phối",
        "🚚 Tiếp Nhận Rau Điều Chuyển & Đánh Giá",
        "🔔 Thông Báo Nội Bộ",
        "⚙️ Cài Đặt Tài Khoản Đơn Vị"
    ]

menu = st.sidebar.radio("📌 TÍNH NĂNG ĐIỀU PHỐI:", menu_options)

# -------------------------------------------------------------------
# 1. GIAO DIỆN TỔNG QUẢN LÝ (SUPER ADMIN)
# -------------------------------------------------------------------
if user_role == "Tổng Quản Lý":

    # --- DASHBOARD TỔNG QUAN 3 ĐƠN VỊ ---
    if menu == "📊 Dashboard Tổng Quan 3 Đơn Vị":
        st.subheader("📊 Bảng Điều Khiển & Cân Đối Rau Xanh Toàn Bộ 3 Đơn Vị")
        
        df = st.session_state.inventory
        
        # Chỉ số tổng
        total_all = df["Khối lượng (kg)"].sum()
        dv1_qty = df[df["Đơn vị quản lý"] == "Đơn vị 1"]["Khối lượng (kg)"].sum()
        dv2_qty = df[df["Đơn vị quản lý"] == "Đơn vị 2"]["Khối lượng (kg)"].sum()
        dv3_qty = df[df["Đơn vị quản lý"] == "Đơn vị 3"]["Khối lượng (kg)"].sum()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Tổng Tồn Kho 3 Đơn Vị", f"{total_all:.1f} kg")
        c2.metric("🏢 Tồn Kho Đơn Vị 1", f"{dv1_qty:.1f} kg")
        c3.metric("🏢 Tồn Kho Đơn Vị 2", f"{dv2_qty:.1f} kg")
        c4.metric("🏢 Tồn Kho Đơn Vị 3", f"{dv3_qty:.1f} kg")
        
        st.divider()
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.markdown("### 📊 So Sánh Khối Lượng Rau Giữa 3 Đơn Vị")
            unit_summary = df.groupby("Đơn vị quản lý")["Khối lượng (kg)"].sum().reset_index()
            st.bar_chart(unit_summary, x="Đơn vị quản lý", y="Khối lượng (kg)", use_container_width=True)
            
        with col_m2:
            st.markdown("### 🥗 Cơ Cấu Nhóm Rau Toàn Hệ Thống")
            group_summary = df.groupby("Nhóm")["Khối lượng (kg)"].sum().reset_index()
            st.dataframe(group_summary, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### 🚨 CANH BÁO ĐƠN VỊ THỪA / THIẾU CẦN ĐIỀU PHỐI GẤP")
        
        col_surplus, col_deficit = st.columns(2)
        
        with col_surplus:
            st.success("🟢 **CÁC ĐƠN VỊ ĐANG DƯ THỪA RAU (Có thể điều chuyển):**")
            surplus_df = df[df["Trạng thái"].str.contains("Thừa")]
            if not surplus_df.empty:
                st.dataframe(surplus_df[["Đơn vị quản lý", "Tên rau", "Khối lượng (kg)", "Chất lượng", "Trạng thái"]], use_container_width=True, hide_index=True)
            else:
                st.info("Hiện không có đơn vị nào báo thừa rau.")

        with col_deficit:
            st.error("🔴 **CÁC ĐƠN VỊ ĐANG THIẾU RAU (Cần chi viện khẩn cấp):**")
            deficit_df = df[df["Trạng thái"].str.contains("Thiếu")]
            if not deficit_df.empty:
                st.dataframe(deficit_df[["Đơn vị quản lý", "Tên rau", "Khối lượng (kg)", "Chất lượng", "Trạng thái"]], use_container_width=True, hide_index=True)
            else:
                st.success("Tất cả 3 đơn vị đều đảm bảo đủ định lượng rau xanh.")

    # --- LẬP LỆNH ĐIỀU PHỐI LIÊN ĐƠN VỊ ---
    elif menu == "🔄 Lập Lệnh Điều Phối Liên Đơn Vị":
        st.subheader("🔄 Tổng Quản Lý: Điều Phối Rau Trực Tiếp Giữa Các Đơn Vị")
        st.info("Tính năng cho phép Tổng Quản Lý chủ động san sẻ nguồn rau từ đơn vị thừa sang đơn vị thiếu.")
        
        df_inv = st.session_state.inventory
        st.markdown("### 📋 Danh Sách Tất Cả Lô Rau Tại Các Đơn Vị")
        st.dataframe(df_inv, use_container_width=True, hide_index=True)
        
        st.divider()
        st.markdown("### 📝 Lập Lệnh Điều Chuyển Rau")
        
        with st.form("transfer_form"):
            c_tr1, c_tr2, c_tr3 = st.columns(3)
            from_unit = c_tr1.selectbox("1. Nguồn điều động (Đơn vị xuất)", ["Đơn vị 1", "Đơn vị 2", "Đơn vị 3"])
            
            # Lọc lô rau thuộc đơn vị xuất
            avail_items = df_inv[df_inv["Đơn vị quản lý"] == from_unit]
            selected_veg_id = c_tr2.selectbox("2. Chọn lô rau điều chuyển", avail_items["ID"].tolist() if not avail_items.empty else ["-- Không có rau --"])
            
            to_unit = c_tr3.selectbox("3. Đơn vị nhận chi viện", [u for u in ["Đơn vị 1", "Đơn vị 2", "Đơn vị 3"] if u != from_unit])
            
            c_tr4, c_tr5 = st.columns(2)
            if selected_veg_id != "-- Không có rau --" and not avail_items.empty:
                sel_row = avail_items[avail_items["ID"] == selected_veg_id].iloc[0]
                max_tr_qty = float(sel_row["Khối lượng (kg)"])
                st.info(f"👉 Rau đã chọn: **{sel_row['Tên rau']}** ({sel_row['Nhóm']}) | Tồn kho tại {from_unit}: **{max_tr_qty} kg** | Chất lượng: **{sel_row['Chất lượng']}**")
            else:
                max_tr_qty = 10.0
                
            tr_qty = c_tr4.number_input("Khối lượng điều chuyển (kg)", min_value=0.5, max_value=max_tr_qty, value=min(20.0, max_tr_qty), step=1.0)
            tr_reason = c_tr5.text_input("Lý do / Mệnh lệnh điều phối", "Cân đối định mức rau xanh tuần")
            
            btn_execute_transfer = st.form_submit_button("🚀 Phát Lệnh Điều Phối Liên Đơn Vị")
            
            if btn_execute_transfer:
                if selected_veg_id == "-- Không có rau --" or avail_items.empty:
                    st.error("Vui lòng chọn lô rau hợp lệ để điều chuyển!")
                else:
                    # Trừ khối lượng ở đơn vị xuất
                    idx = df_inv[df_inv["ID"] == selected_veg_id].index[0]
                    st.session_state.inventory.loc[idx, "Khối lượng (kg)"] -= tr_qty
                    
                    # Thêm hoặc cập nhật lô rau ở đơn vị nhận
                    new_item = {
                        "ID": f"R00{len(st.session_state.inventory)+1}",
                        "Đơn vị quản lý": to_unit,
                        "Tên rau": sel_row['Tên rau'],
                        "Nhóm": sel_row['Nhóm'],
                        "Nguồn": f"Điều chuyển từ {from_unit}",
                        "Khối lượng (kg)": tr_qty,
                        "Chất lượng": sel_row['Chất lượng'],
                        "Trạng thái": "Vừa đủ (Nhận điều phối)",
                        "Ngày nhập": datetime.date.today(),
                        "Hạn dùng (ngày)": sel_row['Hạn dùng (ngày)']
                    }
                    st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
                    
                    # Lưu lịch sử điều phối
                    new_history = {
                        "Mã ĐP": f"DP00{len(st.session_state.transfer_history)+1}",
                        "Đơn vị xuất": from_unit,
                        "Đơn vị nhận": to_unit,
                        "Tên rau": sel_row['Tên rau'],
                        "Khối lượng (kg)": tr_qty,
                        "Người duyệt": user_name,
                        "Ngày điều phối": datetime.date.today(),
                        "Trạng thái": "Đã điều động (Chờ đơn vị nhận xác nhận)",
                        "Đánh giá chất lượng": "Chờ nghiệm thu"
                    }
                    st.session_state.transfer_history = pd.concat([st.session_state.transfer_history, pd.DataFrame([new_history])], ignore_index=True)
                    
                    # Gửi thông báo tự động tới 2 đơn vị
                    note_msg = f"🚀 [LỆNH ĐIỀU PHỐI KHẨN] Điều chuyển {tr_qty} kg rau '{sel_row['Tên rau']}' từ {from_unit} sang {to_unit}. Lý do: {tr_reason}"
                    st.session_state.notifications.append({
                        "id": len(st.session_state.notifications) + 1,
                        "sender": f"{user_name} (Tổng Quản Lý)",
                        "target": "Tất cả đơn vị",
                        "content": note_msg,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "read_by": []
                    })
                    
                    st.success(f"Đã phát lệnh điều chuyển {tr_qty} kg rau **{sel_row['Tên rau']}** từ **{from_unit}** sang **{to_unit}** thành công!")
                    st.toast("🔔 Đã phát thông báo chỉ đạo tới các đơn vị!", icon="🚀")
                    st.rerun()

        st.divider()
        st.markdown("### 📜 Lịch Sử Điều Phối Giữa 3 Đơn Vị")
        st.dataframe(st.session_state.transfer_history, use_container_width=True, hide_index=True)

    # --- DUYỆT ĐỀ XUẤT ---
    elif menu == "📋 Duyệt Đề Xuất Thừa / Thiếu Rau":
        st.subheader("📋 Danh Sách Đề Xuất Chi Viện & Điều Phối Từ 3 Đơn Vị")
        req_df = st.session_state.transfer_requests
        st.dataframe(req_df, use_container_width=True, hide_index=True)

    # --- QUẢN LÝ KHO ---
    elif menu == "📦 Quản Lý Kho Rau Toàn Hệ Thống":
        st.subheader("📦 Toàn Bộ Kho Rau 3 Đơn Vị")
        st.dataframe(st.session_state.inventory, use_container_width=True, hide_index=True)

    # --- TRUNG TÂM THÔNG BÁO ---
    elif menu == "🔔 Trung Tâm Thông Báo Chỉ Đạo":
        st.subheader("🔔 Phát Thông Báo & Mệnh Lệnh Chỉ Đạo Tới 3 Đơn Vị")
        
        with st.form("admin_notice_form"):
            target_u = st.selectbox("Gửi tới đơn vị", ["Tất cả đơn vị", "Đơn vị 1", "Đơn vị 2", "Đơn vị 3"])
            notice_content = st.text_area("Nội dung chỉ đạo điều phối rau xanh", "Yêu cầu Đơn vị 1 chuẩn bị 50kg rau muống để chuyển sang Đơn vị 2 vào ngày mai.")
            btn_send_notice = st.form_submit_button("📢 Phát Thông Báo Trực Tiếp")
            
            if btn_send_notice:
                st.session_state.notifications.append({
                    "id": len(st.session_state.notifications) + 1,
                    "sender": f"{user_name} (Tổng Quản Lý)",
                    "target": target_u,
                    "content": notice_content,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "read_by": []
                })
                st.success("Đã phát thông báo chỉ đạo tới các đơn vị thành công!")
                st.rerun()
                
        st.divider()
        st.markdown("### 📜 Lịch Sử Thông Báo Trong Hệ Thống")
        for n in reversed(st.session_state.notifications):
            st.info(f"📌 **Từ**: {n['sender']} ➔ **Đến**: {n['target']} ({n['time']})\n\n💬 {n['content']}")

    # --- QUẢN LÝ TÀI KHOẢN ---
    elif menu == "⚙️ Quản Lý Cài Đặt Tài Khoản 3 Đơn Vị":
        st.subheader("⚙️ Quản Lý Cài Đặt Tài Khoản & Phân Quyền 3 Đơn Vị")
        acc_df = pd.DataFrame([{"Tên ĐN": k, "Họ và Tên": v["name"], "Vai trò": v["role"], "Đơn vị": v["unit"], "Mật khẩu": v["pass"]} for k, v in st.session_state.accounts.items()])
        st.dataframe(acc_df, use_container_width=True, hide_index=True)

# -------------------------------------------------------------------
# 2. GIAO DIỆN QUẢN LÝ ĐƠN VỊ (ĐƠN VỊ 1, 2, 3)
# -------------------------------------------------------------------
else:
    unit_id = user_data.get("unit_id", "Đơn vị 1")
    
    # --- DASHBOARD ĐƠN VỊ ---
    if menu == "📊 Bảng Theo Dõi Kho Rau Đơn Vị":
        st.subheader(f"📊 Kho Rau & Nhu Cầu Điều Phối Tại {user_unit}")
        
        my_inventory = st.session_state.inventory[st.session_state.inventory["Đơn vị quản lý"] == unit_id]
        
        my_total = my_inventory["Khối lượng (kg)"].sum()
        my_type_a = my_inventory[my_inventory["Chất lượng"].str.contains("Loại A")]["Khối lượng (kg)"].sum()
        
        c_u1, c_u2 = st.columns(2)
        c_u1.metric("📦 Tồn Kho Rau Đơn Vị", f"{my_total:.1f} kg")
        c_u2.metric("🌟 Rau Loại A Tươi Tốt", f"{my_type_a:.1f} kg")
        
        st.divider()
        st.markdown(f"### 📋 Danh Mục Các Lô Rau Tại {unit_id}")
        if not my_inventory.empty:
            st.dataframe(my_inventory, use_container_width=True, hide_index=True)
        else:
            st.info("Kho đơn vị hiện chưa có rau.")

    # --- NHẬP KHO ĐƠN VỊ ---
    elif menu == "📥 Nhập Rau Tăng Gia / Thu Mua Kho Đơn Vị":
        st.subheader(f"📥 Tiếp Nhận & Khai Báo Rau Nhập Cho Kho {unit_id}")
        
        with st.form("unit_import_form"):
            c1, c2, c3 = st.columns(3)
            item_id = c1.text_input("Mã lô rau", f"R00{len(st.session_state.inventory)+1}")
            item_name = c2.text_input("Tên loại rau", "Rau cải cúc")
            group_type = c3.selectbox("Nhóm rau", ["Rau ăn lá", "Rau củ quả", "Rau gia vị"])
            
            c4, c5, c6 = st.columns(3)
            source = c4.selectbox("Nguồn gốc", ["Tăng gia nội bộ đơn vị", "Thu mua ngoài", "Đơn vị bạn hỗ trợ"])
            qty = c5.number_input("Khối lượng nhập (kg)", min_value=1.0, value=50.0, step=5.0)
            quality = c6.selectbox("Đánh giá chất lượng", ["Loại A (Tươi)", "Loại B (Trung bình)", "Loại C (Cần dùng ngay)"])
            
            status_option = st.selectbox("Tình trạng lượng rau", ["Vừa đủ", "Thừa (Có thể chia sẻ cho đơn vị bạn)", "Thiếu (Cần xin chi viện)"])
            exp_days = st.number_input("Hạn dùng tối đa (ngày)", min_value=1, value=3)
            
            submit = st.form_submit_button("💾 Khai Báo Nhập Kho Đơn Vị")
            
            if submit:
                new_row = {
                    "ID": item_id,
                    "Đơn vị quản lý": unit_id,
                    "Tên rau": item_name,
                    "Nhóm": group_type,
                    "Nguồn": source,
                    "Khối lượng (kg)": qty,
                    "Chất lượng": quality,
                    "Trạng thái": status_option,
                    "Ngày nhập": datetime.date.today(),
                    "Hạn dùng (ngày)": exp_days
                }
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Đã thêm lô rau **{item_name}** ({qty} kg) vào kho {unit_id}!")
                st.rerun()

    # --- KHAI BÁO THỪA THIẾU ---
    elif menu == "📢 Khai Báo Thừa / Thiếu & Đề Xuất Điều Phối":
        st.subheader(f"📢 Đề Xuất Chi Viện Hoặc San Sẻ Rau Của {unit_id}")
        
        with st.form("request_transfer_form"):
            req_type = st.selectbox("Loại đề xuất", ["Xin chi viện (Đơn vị đang thiếu rau)", "Báo thừa rau (Đơn vị sẵn sàng chuyển giao)"])
            veg_type_req = st.text_input("Tên loại rau", "Rau ăn lá (Muống / Cải)")
            req_qty = st.number_input("Khối lượng (kg)", min_value=1.0, value=30.0, step=5.0)
            reason = st.text_area("Lý do / Tình hình thực tế tại đơn vị", "Sản lượng tăng gia thu hoạch vượt chỉ tiêu")
            
            btn_sub_req = st.form_submit_button("📤 Gửi Đề Xuất Cho Tổng Quản Lý")
            
            if btn_sub_req:
                new_req = {
                    "Mã YC": f"DX00{len(st.session_state.transfer_requests)+1}",
                    "Đơn vị đề xuất": unit_id,
                    "Loại yêu cầu": req_type,
                    "Tên rau": veg_type_req,
                    "Khối lượng (kg)": req_qty,
                    "Lý do": reason,
                    "Ngày gửi": datetime.date.today(),
                    "Trạng thái": "Chờ Tổng Quản Lý duyệt"
                }
                st.session_state.transfer_requests = pd.concat([st.session_state.transfer_requests, pd.DataFrame([new_req])], ignore_index=True)
                
                # Báo thông báo cho Admin
                st.session_state.notifications.append({
                    "id": len(st.session_state.notifications) + 1,
                    "sender": f"{user_name} ({unit_id})",
                    "target": "Tổng Quản Lý",
                    "content": f"📢 [{req_type.upper()}] {unit_id} vừa gửi đề xuất: {req_qty} kg {veg_type_req}. Lý do: {reason}",
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "read_by": []
                })
                
                st.success("Đã gửi đề xuất điều phối thành công tới Ban Hậu Cần Tổng!")
                st.rerun()

    # --- TIẾP NHẬN RAU ĐIỀU CHUYỂN ---
    elif menu == "🚚 Tiếp Nhận Rau Điều Chuyển & Đánh Giá":
        st.subheader(f"🚚 Tiếp Nhận & Nghiệm Thu Rau Điều Chuyển Đến {unit_id}")
        
        # Lọc các đợt điều phối chuyển đến đơn vị này
        incoming = st.session_state.transfer_history[st.session_state.transfer_history["Đơn vị nhận"] == unit_id]
        
        if incoming.empty:
            st.info("Chưa có lệnh điều chuyển rau nào tới đơn vị của bạn.")
        else:
            st.dataframe(incoming, use_container_width=True, hide_index=True)
            st.divider()
            
            st.markdown("### ✍️ Phản Hồi Chất Lượng Rau Nhận Điều Chuyển")
            selected_idx = st.selectbox("Chọn mã điều phối để nghiệm thu", incoming.index)
            
            if selected_idx is not None:
                row_tr = incoming.loc[selected_idx]
                st.info(f"Đợt nhận: **{row_tr['Tên rau']}** ({row_tr['Khối lượng (kg)']} kg) - Từ: **{row_tr['Đơn vị xuất']}**")
                
                eval_quality = st.selectbox("Chất lượng thực tế khi nhận rau:", [
                    "Đã nhận đủ - Chất lượng tươi tốt (Loại A)",
                    "Đã nhận - Rau dập nát nhẹ (Loại B)",
                    "Đã nhận - Hao hụt/hư hỏng nhiều (Loại C)"
                ])
                
                if st.button("💾 Xác Nhận Đã Nhận Rau & Lưu Nghiệm Thu"):
                    st.session_state.transfer_history.loc[selected_idx, "Trạng thái"] = "Đã hoàn thành"
                    st.session_state.transfer_history.loc[selected_idx, "Đánh giá chất lượng"] = eval_quality
                    
                    # Gửi thông báo lại cho Admin
                    st.session_state.notifications.append({
                        "id": len(st.session_state.notifications) + 1,
                        "sender": f"{user_name} ({unit_id})",
                        "target": "Tổng Quản Lý",
                        "content": f"✅ {unit_id} đã tiếp nhận và nghiệm thu đợt điều phối {row_tr['Tên rau']} ({row_tr['Khối lượng (kg)']} kg). Đánh giá: {eval_quality}",
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "read_by": []
                    })
                    
                    st.success("Đã hoàn tất xác nhận nhận rau!")
                    st.rerun()

    # --- THÔNG BÁO NỘI BỘ ---
    elif menu == "🔔 Thông Báo Nội Bộ":
        st.subheader("🔔 Hòm Thư & Thông Báo Chỉ Đạo Nội Bộ")
        
        # Đánh dấu đã đọc
        for n in st.session_state.notifications:
            if st.session_state.current_user not in n["read_by"]:
                n["read_by"].append(st.session_state.current_user)
                
        my_notices = [n for n in st.session_state.notifications if n["target"] == "Tất cả đơn vị" or n["target"] == unit_id]
        
        for n in reversed(my_notices):
            st.info(f"📌 **Từ**: {n['sender']} ➔ **Đến**: {n['target']} ({n['time']})\n\n💬 {n['content']}")

    # --- CÀI ĐẶT TÀI KHOẢN ---
    elif menu == "⚙️ Cài Đặt Tài Khoản Đơn Vị":
        st.subheader("⚙️ Cài Đặt Thông Tin Tài Khoản Đơn Vị")
        curr_acc = st.session_state.accounts[st.session_state.current_user]
        
        with st.form("unit_acc_form"):
            new_name = st.text_input("Họ và Tên cán bộ quản lý", value=curr_acc["name"])
            new_pass = st.text_input("Mật khẩu mới", type="password", value=curr_acc["pass"])
            btn_save = st.form_submit_button("💾 Cập Nhật Thông Tin")
            
            if btn_save:
                st.session_state.accounts[st.session_state.current_user]["name"] = new_name
                st.session_state.accounts[st.session_state.current_user]["pass"] = new_pass
                st.success("Đã cập nhật thông tin thành công!")
                st.rerun()
