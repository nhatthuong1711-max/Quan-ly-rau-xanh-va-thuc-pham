import streamlit as st
import pandas as pd
import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý & Điều Phối Rau Xanh",
    page_icon="🥦",
    layout="wide"
)

# -------------------------------------------------------------------
# KHO TRUY CẬP & PHÂN QUYỀN (SESSION STATE)
# -------------------------------------------------------------------

# Khởi tạo danh sách tài khoản hệ thống
ACCOUNTS = {
    "khotong": {
        "name": "Đại úy Nguyễn Văn Hùng",
        "role": "Quản lý kho",
        "pass": "123456",
        "unit": "Kho Tổng Hậu Cần",
        "icon": "📦"
    },
    "truongbep1": {
        "name": "Thượng úy Trần Quốc Toản",
        "role": "Trưởng bếp",
        "pass": "123456",
        "unit": "Bếp 1 (Đại đội 1)",
        "kitchen_id": "Bếp 1",
        "icon": "👨‍🍳"
    },
    "truongbep2": {
        "name": "Trung úy Lê Văn Nam",
        "role": "Trưởng bếp",
        "pass": "123456",
        "unit": "Bếp 2 (Đại đội 2)",
        "kitchen_id": "Bếp 2",
        "icon": "👨‍🍳"
    }
}

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.current_user = None

# Khởi tạo dữ liệu kho mẫu
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"ID": "R001", "Tên rau": "Rau muống", "Nhóm": "Rau ăn lá", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 120.0, "Chất lượng": "Loại A (Tươi)", "Hao hụt (%)": 2.0, "Ngày nhập": datetime.date(2026, 9, 26), "Hạn dùng (ngày)": 3, "Bếp phân bổ": "Bếp 1"},
        {"ID": "R002", "Tên rau": "Cải ngọt", "Nhóm": "Rau ăn lá", "Nguồn": "Thu mua ngoài", "Khối lượng (kg)": 80.0, "Chất lượng": "Loại B (Trung bình)", "Hao hụt (%)": 5.0, "Ngày nhập": datetime.date(2026, 9, 25), "Hạn dùng (ngày)": 2, "Bếp phân bổ": "Bếp 2"},
        {"ID": "R003", "Tên rau": "Bí đỏ", "Nhóm": "Rau củ quả", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 250.0, "Chất lượng": "Loại A (Tươi)", "Hao hụt (%)": 1.0, "Ngày nhập": datetime.date(2026, 9, 20), "Hạn dùng (ngày)": 30, "Bếp phân bổ": "Kho dự trữ"},
        {"ID": "R004", "Tên rau": "Su su", "Nhóm": "Rau củ quả", "Nguồn": "Thu mua ngoài", "Khối lượng (kg)": 150.0, "Chất lượng": "Loại B (Trung bình)", "Hao hụt (%)": 3.0, "Ngày nhập": datetime.date(2026, 9, 24), "Hạn dùng (ngày)": 10, "Bếp phân bổ": "Bếp 1"},
        {"ID": "R005", "Tên rau": "Rau dền", "Nhóm": "Rau ăn lá", "Nguồn": "Tăng gia nội bộ", "Khối lượng (kg)": 45.0, "Chất lượng": "Loại C (Cần dùng ngay)", "Hao hụt (%)": 8.0, "Ngày nhập": datetime.date(2026, 9, 24), "Hạn dùng (ngày)": 1, "Bếp phân bổ": "Bếp 2"}
    ])

if 'export_history' not in st.session_state:
    st.session_state.export_history = pd.DataFrame([
        {"Mã lô": "R001", "Tên rau": "Rau muống", "Khối lượng xuất (kg)": 30.0, "Bếp nhận": "Bếp 1", "Ngày xuất": datetime.date(2026, 9, 27), "Ghi chú": "Xuất cho bữa trưa", "Xác nhận của bếp": "Đã nhận - Tốt"},
        {"Mã lô": "R002", "Tên rau": "Cải ngọt", "Khối lượng xuất (kg)": 20.0, "Bếp nhận": "Bếp 2", "Ngày xuất": datetime.date(2026, 9, 27), "Ghi chú": "Xuất cho bữa chiều", "Xác nhận của bếp": "Đã nhận - Tốt"}
    ])

if 'kitchen_requests' not in st.session_state:
    st.session_state.kitchen_requests = pd.DataFrame([
        {"Mã YC": "YC001", "Bếp yêu cầu": "Bếp 1", "Loại rau": "Rau muống", "Khối lượng (kg)": 25.0, "Ngày cần": datetime.date(2026, 9, 28), "Bữa ăn": "Bữa trưa", "Trạng thái": "Đã duyệt"}
    ])

# -------------------------------------------------------------------
# GIAO DIỆN ĐĂNG NHẬP / PHÂN QUYỀN TÀI KHOẢN
# -------------------------------------------------------------------
if not st.session_state.authenticated:
    st.title("🥦 HỆ THỐNG QUẢN LÝ SỐ LƯỢNG & CHẤT LƯỢNG RAU XANH")
    st.markdown("### 🔑 Đăng Nhập Hệ Thống & Phân Quyền Vận Hành")
    
    col_login, col_demo = st.columns([1.2, 1])
    
    with col_login:
        with st.form("login_form"):
            st.subheader("Đăng Nhập Tài Khoản")
            username = st.text_input("Tên đăng nhập", value="khotong")
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
        st.subheader("⚡ Đăng Nhập Nhanh (Dành Cho Demo)")
        st.info("Bấm chọn vai trò bên dưới để trải nghiệm ngay giao diện phân quyền:")
        
        if st.button("📦 Đăng nhập Vai trò: QUẢN LÝ KHO (Full Quyền)"):
            st.session_state.authenticated = True
            st.session_state.current_user = "khotong"
            st.rerun()
            
        if st.button("👨‍🍳 Đăng nhập Vai trò: TRƯỞNG BẾP (Bếp 1)"):
            st.session_state.authenticated = True
            st.session_state.current_user = "truongbep1"
            st.rerun()

        if st.button("👨‍🍳 Đăng nhập Vai trò: TRƯỞNG BẾP (Bếp 2)"):
            st.session_state.authenticated = True
            st.session_state.current_user = "truongbep2"
            st.rerun()

    st.stop()

# -------------------------------------------------------------------
# XỬ LÝ KHI ĐÃ ĐĂNG NHẬP
# -------------------------------------------------------------------
user_data = ACCOUNTS[st.session_state.current_user]
user_role = user_data["role"]
user_name = user_data["name"]
user_unit = user_data["unit"]

# Sidebar Thông tin Tài khoản & Đăng xuất
st.sidebar.markdown(f"### {user_data['icon']} ĐANG ĐĂNG NHẬP")
st.sidebar.success(f"**{user_name}**\n\n📌 **Vai trò**: {user_role}\n\n🏢 **Đơn vị**: {user_unit}")

if st.sidebar.button("🚪 Đăng Xuất"):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

st.sidebar.divider()

# Tiêu đề chung
st.title("🥦 HỆ THỐNG QUẢN LÝ SỐ LƯỢNG & CHẤT LƯỢNG RAU XANH")
st.caption(f"Phiên bản phân quyền vai trò | Tài khoản: **{user_name}** ({user_role})")

# -------------------------------------------------------------------
# MENU THEO VAI TRÒ (ROLE-BASED NAVIGATION)
# -------------------------------------------------------------------
if user_role == "Quản lý kho":
    menu_options = [
        "📊 Bảng Điều Khiển Tổng Kho", 
        "📥 Nhập Kho & Phân Loại Chất Lượng", 
        "📤 Lập Lệnh Xuất Kho & Điều Phối", 
        "📋 Duyệt Đơn Đặt Rau Từ Bếp Ăn",
        "🧮 Dự Báo & Cân Đối Định Mức Kho"
    ]
else: # Trưởng bếp
    menu_options = [
        "📊 Bảng Theo Dõi Nhu Cầu Bếp Ăn", 
        "📝 Đặt Rau & Đề Xuất Điều Phối", 
        "🍽️ Xử Lý Rau Nhận Bếp & Đánh Giá Chất Lượng", 
        "🧮 Tra Cứu Định Mức Khẩu Phần Bữa Ăn"
    ]

menu = st.sidebar.radio("📌 TÍNH NĂNG VẬN HÀNH:", menu_options)

# -------------------------------------------------------------------
# 1. GIAO DIỆN QUẢN LÝ KHO
# -------------------------------------------------------------------
if user_role == "Quản lý kho":
    
    # --- DASHBOARD KHO ---
    if menu == "📊 Bảng Điều Khiển Tổng Kho":
        st.subheader("📊 Bảng Điều Khiển Tổng Kho & Cảnh Báo Chất Lượng")
        
        df = st.session_state.inventory
        total_qty = df["Khối lượng (kg)"].sum()
        type_a_qty = df[df["Chất lượng"].str.contains("Loại A")]["Khối lượng (kg)"].sum()
        urgent_qty = df[df["Chất lượng"].str.contains("Loại C")]["Khối lượng (kg)"].sum()
        leaf_veg_qty = df[df["Nhóm"] == "Rau ăn lá"]["Khối lượng (kg)"].sum()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Tổng Tồn Kho", f"{total_qty:.1f} kg")
        c2.metric("🌟 Rau Loại A (Tươi Tốt)", f"{type_a_qty:.1f} kg", f"{(type_a_qty/total_qty*100 if total_qty>0 else 0):.1f}%")
        c3.metric("⚠️ Rau Cần Dùng Ngay (Loại C)", f"{urgent_qty:.1f} kg", delta="-Ưu tiên điều phối", delta_color="inverse")
        c4.metric("🥬 Rau Ăn Lá Tươi", f"{leaf_veg_qty:.1f} kg")
        
        st.divider()
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("### 🥗 Tồn Kho Theo Nhóm Rau")
            group_df = df.groupby("Nhóm")["Khối lượng (kg)"].sum().reset_index()
            st.bar_chart(group_df, x="Nhóm", y="Khối lượng (kg)", use_container_width=True)
            
        with col_c2:
            st.markdown("### 🏢 Tồn Kho Theo Bếp Phân Bổ")
            kitchen_df = df.groupby("Bếp phân bổ")["Khối lượng (kg)"].sum().reset_index()
            st.dataframe(kitchen_df, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### 🚨 LÔ RAU CẦN ĐIỀU PHỐI GẤP TRONG 24H")
        urgent_items = df[(df["Chất lượng"].str.contains("Loại C")) | (df["Hạn dùng (ngày)"] <= 1)]
        if not urgent_items.empty:
            st.warning("Các lô rau dưới đây cần ưu tiên xuất kho ngay để tránh dập nát / hư hỏng:")
            st.dataframe(urgent_items, use_container_width=True, hide_index=True)
        else:
            st.success("Tất cả lô rau trong kho đều đạt điều kiện bảo quản an toàn.")

    # --- NHẬP KHO ---
    elif menu == "📥 Nhập Kho & Phân Loại Chất Lượng":
        st.subheader("📥 Quyền Quản Lý Kho: Tiếp Nhận & Phân Loại Rau")
        
        with st.form("import_form"):
            c1, c2, c3 = st.columns(3)
            item_id = c1.text_input("Mã lô rau", f"R00{len(st.session_state.inventory)+1}")
            item_name = c2.text_input("Tên loại rau", "Bắp cải")
            group_type = c3.selectbox("Nhóm rau", ["Rau ăn lá", "Rau củ quả", "Rau gia vị"])
            
            c4, c5, c6 = st.columns(3)
            source = c4.selectbox("Nguồn gốc", ["Tăng gia nội bộ", "Thu mua ngoài", "Đơn vị bạn hỗ trợ"])
            qty = c5.number_input("Khối lượng nhập (kg)", min_value=1.0, value=60.0, step=5.0)
            quality = c6.selectbox("Phân loại chất lượng", [
                "Loại A (Tươi, không dập nát)", 
                "Loại B (Trung bình, dập nát nhẹ)", 
                "Loại C (Cần dùng ngay trong 24h)"
            ])
            
            c7, c8, c9 = st.columns(3)
            loss_pct = c7.number_input("Hao hụt dự kiến (%)", min_value=0.0, max_value=50.0, value=2.0)
            exp_days = c8.number_input("Hạn bảo quản (ngày)", min_value=1, max_value=60, value=4)
            assign_kitchen = c9.selectbox("Bếp phân bổ", ["Bếp 1", "Bếp 2", "Kho dự trữ"])
            
            submit = st.form_submit_button("💾 Xác Nhận Nhập Kho")
            
            if submit:
                new_row = {
                    "ID": item_id,
                    "Tên rau": item_name,
                    "Nhóm": group_type,
                    "Nguồn": source,
                    "Khối lượng (kg)": qty,
                    "Chất lượng": quality,
                    "Hao hụt (%)": loss_pct,
                    "Ngày nhập": datetime.date.today(),
                    "Hạn dùng (ngày)": exp_days,
                    "Bếp phân bổ": assign_kitchen
                }
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Đã cập nhật lô rau **{item_name}** ({qty} kg) vào kho tổng!")

        st.divider()
        st.markdown("### 📋 Toàn Bộ Danh Mục Lô Rau Trong Kho")
        st.dataframe(st.session_state.inventory, use_container_width=True, hide_index=True)

    # --- XUẤT KHO ---
    elif menu == "📤 Lập Lệnh Xuất Kho & Điều Phối":
        st.subheader("📤 Quyền Quản Lý Kho: Lập Lệnh Xuất & Điều Phối Rau")
        
        df_inv = st.session_state.inventory
        st.markdown("### 💡 Gợi Ý Xuất Kho Theo Thuật Toán FEFO (Hạn ngắn xuất trước)")
        df_sorted = df_inv.sort_values(by=["Hạn dùng (ngày)"], ascending=True)
        st.dataframe(df_sorted[["ID", "Tên rau", "Khối lượng (kg)", "Chất lượng", "Hạn dùng (ngày)", "Bếp phân bổ"]], use_container_width=True, hide_index=True)
        
        st.divider()
        selected_id = st.selectbox("Chọn mã lô rau để xuất", df_inv["ID"].tolist() + ["-- Chọn --"])
        
        if selected_id != "-- Chọn --":
            selected_row = df_inv[df_inv["ID"] == selected_id].iloc[0]
            max_qty = float(selected_row["Khối lượng (kg)"])
            
            with st.form("export_form"):
                st.info(f"Đang xuất: **{selected_row['Tên rau']}** (Còn tồn: {max_qty} kg)")
                export_qty = st.number_input("Khối lượng xuất (kg)", min_value=0.5, max_value=max_qty, value=min(15.0, max_qty))
                target_kitchen = st.selectbox("Bếp ăn nhận rau", ["Bếp 1", "Bếp 2", "Bếp 3"])
                note = st.text_input("Ghi chú lệnh xuất", "Phục vụ bữa ăn cán bộ chiến sĩ")
                
                btn_export = st.form_submit_button("🚀 Phát Lệnh Xuất Kho")
                
                if btn_export:
                    idx = df_inv[df_inv["ID"] == selected_id].index[0]
                    st.session_state.inventory.loc[idx, "Khối lượng (kg)"] -= export_qty
                    if st.session_state.inventory.loc[idx, "Khối lượng (kg)"] <= 0:
                        st.session_state.inventory = st.session_state.inventory.drop(idx).reset_index(drop=True)
                    
                    new_exp = {
                        "Mã lô": selected_id,
                        "Tên rau": selected_row['Tên rau'],
                        "Khối lượng xuất (kg)": export_qty,
                        "Bếp nhận": target_kitchen,
                        "Ngày xuất": datetime.date.today(),
                        "Ghi chú": note,
                        "Xác nhận của bếp": "Chờ bếp nhận"
                    }
                    st.session_state.export_history = pd.concat([st.session_state.export_history, pd.DataFrame([new_exp])], ignore_index=True)
                    st.success(f"Đã lập lệnh xuất {export_qty} kg rau **{selected_row['Tên rau']}** gửi cho **{target_kitchen}**!")
                    st.rerun()

    # --- DUYỆT ĐƠN YÊU CẦU ---
    elif menu == "📋 Duyệt Đơn Đặt Rau Từ Bếp Ăn":
        st.subheader("📋 Danh Sách Yêu Cầu Đặt Rau Từ Các Bếp Ăn")
        req_df = st.session_state.kitchen_requests
        st.dataframe(req_df, use_container_width=True, hide_index=True)

    # --- DỰ BÁO DỊNH MỨC ---
    elif menu == "🧮 Dự Báo & Cân Đối Định Mức Kho":
        st.subheader("🧮 Lập Kế Hoạch Cân Đối Nhu Cầu Rau Xanh Toàn Đơn Vị")
        headcount = st.number_input("Tổng quân số đơn vị", min_value=10, value=300, step=10)
        quota = st.number_input("Định mức rau (gam/người/ngày)", min_value=100, value=350, step=10)
        days = st.number_input("Số ngày lập kế hoạch", min_value=1, value=7, step=1)
        
        total_need = (headcount * quota * days) / 1000.0
        curr_stock = st.session_state.inventory["Khối lượng (kg)"].sum()
        
        st.info(f"🎯 Nhu cầu tổng: **{total_need:.1f} kg** | 📦 Kho hiện có: **{curr_stock:.1f} kg**")
        if curr_stock >= total_need:
            st.success("Kho đảm bảo tự chủ đủ lượng rau theo kế hoạch!")
        else:
            st.error(f"Kho đang thiếu **{total_need - curr_stock:.1f} kg** rau xanh. Cần lập kế hoạch thu mua bổ sung.")

# -------------------------------------------------------------------
# 2. GIAO DIỆN TRƯỞNG BẾP
# -------------------------------------------------------------------
else:
    kitchen_id = user_data.get("kitchen_id", "Bếp 1")
    
    # --- DASHBOARD TRƯỞNG BẾP ---
    if menu == "📊 Bảng Theo Dõi Nhu Cầu Bếp Ăn":
        st.subheader(f"📊 Bảng Theo Dõi Nhu Cầu & Tồn Rau Tại {user_unit}")
        
        # Lọc danh sách rau phân bổ cho bếp này
        my_kitchen_veg = st.session_state.inventory[st.session_state.inventory["Bếp phân bổ"] == kitchen_id]
        
        st.markdown(f"### 🥬 Các Lô Rau Kho Đã Dự Kiến Phân Bổ Cho {kitchen_id}")
        if not my_kitchen_veg.empty:
            st.dataframe(my_kitchen_veg, use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có lô rau nào được gắn phân bổ riêng cho bếp của bạn.")
            
        st.divider()
        st.markdown("### 🚨 RAU CÓ CHẤT LƯỢNG CẦN DÙNG NGAY TRONG NGÀY")
        urgent_for_chef = st.session_state.inventory[(st.session_state.inventory["Chất lượng"].str.contains("Loại C")) | (st.session_state.inventory["Hạn dùng (ngày)"] <= 1)]
        st.dataframe(urgent_for_chef, use_container_width=True, hide_index=True)

    # --- ĐẶT RAU / ĐỀ XUẤT ---
    elif menu == "📝 Đặt Rau & Đề Xuất Điều Phối":
        st.subheader(f"📝 Quyền Trưởng Bếp: Gửi Phiếu Đặt Rau Cho {kitchen_id}")
        
        with st.form("request_form"):
            c1, c2 = st.columns(2)
            veg_name = c1.selectbox("Chọn loại rau cần đặt", ["Rau muống", "Cải ngọt", "Bắp cải", "Bí đỏ", "Su su", "Chủng loại khác"])
            req_qty = c2.number_input("Khối lượng đăng ký (kg)", min_value=1.0, value=20.0, step=1.0)
            
            c3, c4 = st.columns(2)
            req_date = c3.date_input("Ngày cần nhận", datetime.date.today() + datetime.timedelta(days=1))
            meal_type = c4.selectbox("Phục vụ bữa ăn", ["Bữa sáng", "Bữa trưa", "Bữa chiều"])
            
            btn_submit_req = st.form_submit_button("📩 Gửi Yêu Cầu Cho Quản Lý Kho")
            
            if btn_submit_req:
                new_req = {
                    "Mã YC": f"YC00{len(st.session_state.kitchen_requests)+1}",
                    "Bếp yêu cầu": kitchen_id,
                    "Loại rau": veg_name,
                    "Khối lượng (kg)": req_qty,
                    "Ngày cần": req_date,
                    "Bữa ăn": meal_type,
                    "Trạng thái": "Chờ kho duyệt"
                }
                st.session_state.kitchen_requests = pd.concat([st.session_state.kitchen_requests, pd.DataFrame([new_req])], ignore_index=True)
                st.success(f"Đã gửi phiếu đặt {req_qty} kg rau **{veg_name}** tới Quản lý kho!")

        st.divider()
        st.markdown("### 📜 Lịch Sử Đặt Rau Của Bếp")
        my_reqs = st.session_state.kitchen_requests[st.session_state.kitchen_requests["Bếp yêu cầu"] == kitchen_id]
        st.dataframe(my_reqs, use_container_width=True, hide_index=True)

    # --- TIẾP NHẬN & ĐÁNH GIÁ CHẤT LƯỢNG ---
    elif menu == "🍽️ Xử Lý Rau Nhận Bếp & Đánh Giá Chất Lượng":
        st.subheader(f"🍽️ Xác Nhận Nhận Rau & Đánh Giá Thực Tế Tại Nhà Bếp")
        
        # Danh sách xuất kho dành cho bếp này
        my_exports = st.session_state.export_history[st.session_state.export_history["Bếp nhận"] == kitchen_id]
        
        if my_exports.empty:
            st.info("Chưa có lệnh xuất rau nào từ kho tới bếp của bạn.")
        else:
            st.dataframe(my_exports, use_container_width=True, hide_index=True)
            st.divider()
            
            st.markdown("### ✍️ Phản Hồi Chất Lượng Rau Nhận Được")
            selected_exp_idx = st.selectbox("Chọn đợt nhận rau để phản hồi", my_exports.index)
            
            if selected_exp_idx is not None:
                exp_row = my_exports.loc[selected_exp_idx]
                st.info(f"Đợt nhận: **{exp_row['Tên rau']}** ({exp_row['Khối lượng xuất (kg)']} kg) - Ngày xuất: {exp_row['Ngày xuất']}")
                
                feedback = st.selectbox("Đánh giá thực tế của Trưởng bếp:", [
                    "Đã nhận - Chất lượng tốt (Loại A)",
                    "Đã nhận - Rau dập nát nhẹ (Cần sơ chế kỹ)",
                    "Đã nhận - Hư hỏng nhiều (Đề nghị hoàn kho/đổi)"
                ])
                
                if st.button("💾 Lưu Phản Hồi Chất Lượng"):
                    st.session_state.export_history.loc[selected_exp_idx, "Xác nhận của bếp"] = feedback
                    st.success("Đã ghi nhận phản hồi chất lượng rau về hệ thống kho tổng!")
                    st.rerun()

    # --- TRA CỨU ĐỊNH MỨC ---
    elif menu == "🧮 Tra Cứu Định Mức Khẩu Phần Bữa Ăn":
        st.subheader("🧮 Tính Định Mức Bữa Ăn Cho Bếp")
        diners = st.number_input("Số lượng cán bộ/chiến sĩ ăn tại bếp", min_value=1, value=100)
        quota_meal = st.number_input("Định mức rau/người/bữa (gam)", min_value=50, value=120)
        
        needed_meal_kg = (diners * quota_meal) / 1000.0
        st.info(f"👉 Nhu cầu rau xanh thực tế cho bữa ăn này: **{needed_meal_kg:.1f} kg**")
