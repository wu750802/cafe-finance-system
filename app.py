import streamlit as st
import pandas as pd
from datetime import date

# 頁面標題與簡單的介面設定
st.set_page_config(page_title="咖啡廳營運管理系統", layout="wide")
st.title("☕ 咖啡廳營運帳務管理")

# 初始化模擬資料庫 (在實際專案中，這裡會連結到 CSV 或資料庫)
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["日期", "類別", "項目", "金額"])

# 側邊欄：新增帳務
with st.sidebar:
    st.header("新增帳目")
    entry_date = st.date_input("日期", date.today())
    category = st.selectbox("類別", ["營業收入", "食材支出", "店租水電", "人力成本", "其他"])
    item_name = st.text_input("項目名稱", placeholder="例如：拿鐵咖啡、鮮乳進貨")
    amount = st.number_input("金額", min_value=0, step=1)
    
    if st.button("儲存帳目"):
        new_data = pd.DataFrame([[entry_date, category, item_name, amount]], 
                                columns=["日期", "類別", "項目", "金額"])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
        st.success("紀錄成功！")

# 主頁面：數據視覺化與報表
col1, col2, col3 = st.columns(3)

# 計算各項數值
income = st.session_state.transactions[st.session_state.transactions["類別"] == "營業收入"]["金額"].sum()
expenses = st.session_state.transactions[st.session_state.transactions["類別"] != "營業收入"]["金額"].sum()
balance = income - expenses

with col1:
    st.metric("總收入", f"${income:,}")
with col2:
    st.metric("總支出", f"${expenses:,}")
with col3:
    st.metric("當前盈餘", f"${balance:,}", delta=float(balance))

st.divider()

# 顯示明細清單
st.subheader("📊 帳務明細報表")
if not st.session_state.transactions.empty:
    st.dataframe(st.session_state.transactions, use_container_width=True)
    
    # 簡單的匯出功能
    csv = st.session_state.transactions.to_csv(index=False).encode('utf-8-sig')
    st.download_button("下載報表 (CSV)", data=csv, file_name=f"cafe_report_{date.today()}.csv", mime="text/csv")
else:
    st.info("目前尚無資料，請從左側新增。")
