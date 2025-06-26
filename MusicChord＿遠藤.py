import streamlit as st

st.title("数値計算アプリ")

# 入力
f1 = st.number_input("Aの値", value=0)
f2 = st.number_input("Bの値", value=0)
f3 = st.number_input("Cの値", value=1)
v1 = st.number_input("v1の値", value=1)
v2 = st.number_input("v2の値", value=1)
v3 = st.number_input("v3の値", value=1)

# 実行ボタン
if st.button("計算する"):
    result = (f1 + f2) * f3 + v1
    st.success(f"結果: {result}")
