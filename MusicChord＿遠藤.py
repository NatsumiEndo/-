import streamlit as st

st.title("数値計算アプリ")

# 入力
a = st.number_input("Aの値", value=0)
b = st.number_input("Bの値", value=0)
c = st.number_input("Cの値", value=1)

# 実行ボタン
if st.button("計算する"):
    result = (a + b) * c
    st.success(f"結果: {result}")
