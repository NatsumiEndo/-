import streamlit as st
import numpy as np
import pandas as pd
import itertools

st.title("数値計算アプリ")

#定数
a=0.7
b=1.4
c=4.0
d=1.33
e=0.6
h=1.56
g=0.88
N = 5   #倍音数

#ピアノの鍵盤に対応した周波数のリストを作成
fa = 27.5
fb = 55
fc = 110
fd = 220
fe = 440
ff = 880
fg = 1760
fh = 3520

#音名番号に対応した周波数の設定
kenban0=[fa*(2**(1/12))**(i-1) for i in range(1,13)]
kenban1=[fb*(2**(1/12))**(i-1) for i in range(1,13)]
kenban2=[fc*(2**(1/12))**(i-1) for i in range(1,13)]
kenban3=[fd*(2**(1/12))**(i-1) for i in range(1,13)]
kenban4=[fe*(2**(1/12))**(i-1) for i in range(1,13)]
kenban5=[ff*(2**(1/12))**(i-1) for i in range(1,13)]
kenban6=[fg*(2**(1/12))**(i-1) for i in range(1,13)]
kenban7=[fh*(2**(1/12))**(i-1) for i in range(1,5)]
kenban_list=kenban0+kenban1+kenban2+kenban3+kenban4+kenban5+kenban6+kenban7

#使用頻度の高い和音(展開系を含む)の設定
Cmaj_0=[kenban_list[39],kenban_list[43],kenban_list[46]] #[4C,4E,4G]
Cmaj_1=[kenban_list[43],kenban_list[46],kenban_list[51]]
Cmaj_2=[kenban_list[46],kenban_list[51],kenban_list[55]]
Cmin_0=[kenban_list[39],kenban_list[42],kenban_list[46]] #[4C,4E♭,4G]
Cmin_1=[kenban_list[42],kenban_list[46],kenban_list[51]]
Cmin_2=[kenban_list[46],kenban_list[51],kenban_list[54]]
Caug_0=[kenban_list[39],kenban_list[43],kenban_list[47]] #[4C,4E,4G#]
Caug_1=[kenban_list[43],kenban_list[47],kenban_list[51]]
Caug_2=[kenban_list[47],kenban_list[51],kenban_list[55]]
Csus4_0=[kenban_list[39],kenban_list[44],kenban_list[46]] #[4C,4F,4G]
Csus4_1=[kenban_list[44],kenban_list[46],kenban_list[51]]
Csus4_2=[kenban_list[46],kenban_list[51],kenban_list[56]]
Cflat5_0=[kenban_list[39],kenban_list[43],kenban_list[45]] #[4C,4E,4G♭]
Cflat5_1=[kenban_list[43],kenban_list[45],kenban_list[51]]
Cflat5_2=[kenban_list[45],kenban_list[51],kenban_list[55]]
Cdim_0=[kenban_list[39],kenban_list[42],kenban_list[45]] #[4C,4E♭,4G♭]
Cdim_1=[kenban_list[42],kenban_list[45],kenban_list[51]]
Cdim_2=[kenban_list[45],kenban_list[51],kenban_list[54]]
C_chord_list=[Cmaj_0,Cmaj_1,Cmaj_2,Cmin_0,Cmin_1,Cmin_2,Caug_0,Caug_1,Caug_2,Csus4_0,Csus4_1,Csus4_2,Cflat5_0,Cflat5_1,Cflat5_2,Cdim_0,Cdim_1,Cdim_2]
C_name_list=["Cmaj_0","Cmaj_1","Cmaj_2","Cmin_0","Cmin_1","Cmin_2","Caug_0","Caug_1","Caug_2","Csus4_0","Csus4_1","Csus4_2","Cflat5_0","Cflat5_1","Cflat5_2","Cdim_0","Cdim_1","Cdim_2"]

#音量比(v1+v2+v3=1)のリストを作成
v_com=[]
for i in np.arange(1,9):
  for j in np.arange(1,10-i):
    v_com.append([round(i*0.1,2),round(j*0.1,2),round(1-i*0.1-j*0.1,2)])

#音量比（重複なし）
v_com_unique = []
for i in v_com:
    if i not in v_com_unique:
        v_com_unique.append(i)

#3和音の不協和度モジュール
def D(f1,f2,f3,v1,v2,v3,N,a,b,c,d,g):
   #倍音の周波数
    R = range(1,N+1)
    fot1=[f1*i for i in R]
    fot2=[f2*i for i in R]
    fot3=[f3*i for i in R]
    #倍音を考慮した不協和度の計算
    D=0
    D1=0
    D2=0
    D3=0
    for j in range(N):
      for k in range(N):

        x12 = abs(12*np.log2(fot2[j]/fot1[k]))
        x23 = abs(12*np.log2(fot3[j]/fot2[k]))
        x13 = abs(12*np.log2(fot3[j]/fot1[k]))

        A = -a*(x12**d)
        B = -b*(x12**d)
        v12 = np.sqrt((v1 * v2 * (g ** (j+k))))
        d12 = c*v12*(np.exp(A)-np.exp(B))
        D1 = D1 + d12

        A = -a*(x23**d)
        B = -b*(x23**d)
        v23 = np.sqrt((v2 * v3 * (g ** (j+k))))
        d23 = c*v23*(np.exp(A)-np.exp(B))
        D2 = D2 + d23

        A = -a*(x13**d)
        B = -b*(x13**d)
        v13 = np.sqrt((v3 * v1 * (g ** (j+k))))
        d13 = c*v13*(np.exp(A)-np.exp(B))
        D3 = D3 + d13
    D = (D1 + D2 + D3)/3
    return D

#3和音の緊張度・モダリティモジュール
def TM(f1,f2,f3,v1,v2,v3,N,e,h,g):
    #倍音の周波数
    T=0
    M=0
    R = range(1,N+1)
    fot1=[f1*i for i in R]
    fot2=[f2*i for i in R]
    fot3=[f3*i for i in R]
    #倍音を考慮した緊張度の計算
    f_list = []
    v_list = []
    for j in range(N):
      for k in range(N):
        for l in range(N):
          f = [fot1[j], fot2[k], fot3[l]]
          f_list.append(sorted(f))
          v_list.append((v1 * v2 * v3 * (g ** (j+k+l)))**(1/3))
    #音程差
    for l in range(N**3):
      x12 = (12*np.log2(f_list[l][1]/f_list[l][0]))
      x23 = (12*np.log2(f_list[l][2]/f_list[l][1]))
      #緊張度
      t = v_list[l]*np.exp(-((x23-x12)/e)**2)
      T += t
      #モダリティ
      m = -v_list[l]*(2*(x23-x12)/h)*np.exp(-(((x23-x12)**4)/4))
      M += m
    return [T,M]

def I_0(D,T,lam):#初期ver (本来はlamはいらないけど、他のIと合わせるために変数指定)
    I = np.sqrt(D ** 2 + T ** 2)
    return I

def I_1(D,T,lam):
    I = D + T * lam
    return I

def I_2(D,T,lam):
    I = D * lam + T
    return I

def S_0(D,T,M):
    S = np.array(np.abs(M)) / np.sqrt(M ** 2 + D ** 2 + T ** 2)
    return S

def S_1(D,T,M):
    S = np.array(np.abs(M)) / np.sqrt(D ** 2 + T ** 2)
    return S

I_function_map = {'I_0': I_0,'I_1': I_1,'I_2': I_2}
S_function_map = {'S_0': S_0,'S_1': S_1}

#lamに対して、Ｉの最小値と、そのときの音量比の組み合わせを計算するモジュール
def lam_min(f1,f2,f3,lam,I_num,S_num):
    D_list = []
    T_list = []
    M_list = []
    I_list = []
    S_list = []
    for i in range(len(v_com)):
      Da = D(f1,f2,f3,v_com[i][0],v_com[i][1],v_com[i][2],N,a,b,c,d,g)
      Ta = TM(f1,f2,f3,v_com[i][0],v_com[i][1],v_com[i][2],N,e,h,g)[0]
      Ma = TM(f1,f2,f3,v_com[i][0],v_com[i][1],v_com[i][2],N,e,h,g)[1]
      Ia = I_num(Da,Ta,lam)
      Sa = S_num(Da,Ta,Ma)

      D_list.append(Da)
      T_list.append(Ta)
      M_list.append(Ma)
      I_list.append(Ia)
      S_list.append(Sa)

    v_com_min = v_com[I_list.index(min(I_list))]
    return(lam,v_com_min,min(I_list),T_list[I_list.index(min(I_list))],D_list[I_list.index(min(I_list))])

#相関係数
def reg(list1,list2):
    s1=pd.Series(list1)
    s2=pd.Series(list2)
    r=s1.corr(s2)
    return r

#csvファイルを出力するモジュール
def export_csv(hyo, name):
    jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    now_str = jst_now.strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{now_str}.csv"
    hyo.to_csv(filename, index=False, encoding="utf-8-sig")

#６ずつのスプリットリスト作成モジュール
def split_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]
    
# 入力
f1 = st.number_input("Aの値", value=39)
f2 = st.number_input("Bの値", value=43)
f3 = st.number_input("Cの値", value=46)
v1 = st.number_input("v1の値", value=1)
v2 = st.number_input("v2の値", value=1)
v3 = st.number_input("v3の値", value=1)

def round_tuple(t, ndigits=3):
    return tuple(sorted([round(x, ndigits) for x in t]))  # 組合せのキーに使う

for lam in range(11):
    I_num = I_2
    S_num = S_1
    v_com_all_unique = []

    # 音量比の順列全体を収集
    for item in v_com_a:
        perms = list(itertools.permutations(item))
        unique_perms = list(set(tuple(p) for p in perms))
        for unique_p in unique_perms:
            v_com_all_unique.append([p / 10 for p in unique_p])  # 10で割る

    # 組合せごとの結果リスト
    grouped_results = {}

    for v_comb in v_com_all_unique:
        Da = D(f1,f2,f3,v_comb[0],v_comb[1],v_comb[2],N,a,b,c,d,g)
        Ta = TM(f1,f2,f3,v_comb[0],v_comb[1],v_comb[2],N,e,h,g)[0]
        Ma = TM(f1,f2,f3,v_comb[0],v_comb[1],v_comb[2],N,e,h,g)[1]
        Ia = I_num(Da, Ta, lam)
        Sa = S_num(Da, Ta, Ma)

        # 組み合わせキー（順番は問わず、同じ構成でまとめる）
        comb_key = round_tuple(v_comb)  # e.g. (0.1, 0.1, 0.8)

        if comb_key not in grouped_results:
            grouped_results[comb_key] = []

        grouped_results[comb_key].append([
            lam, v_comb[0], v_comb[1], v_comb[2], Da, Ta, Ma, Ia, Sa
        ])

    # 出力（各組み合わせごとに I 昇順で表示）
    for comb_key, rows in grouped_results.items():
        # I 昇順でソート
        sorted_rows = sorted(rows, key=lambda x: x[7])  # x[7] = I
        df = pd.DataFrame(sorted_rows, columns=['lam', 'v1', 'v2', 'v3', 'D', 'T', 'M', 'I', 'S'])

     #   print(f"\n--- lam={lam}, 音量比の組み合わせ={comb_key} ---")
     #   print(df)

# 実行ボタン
if st.button("計算する"):
    result = (f1 + f2) * f3 + v1
    st.success(f"結果: {result}")
