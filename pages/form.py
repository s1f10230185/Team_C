import streamlit as st
import pandas as pd

st.set_page_config(page_title="オシハナ - 文章登録", layout="centered")
st.markdown('<style>[data-testid="stSidebarNav"]{display:none}</style>', unsafe_allow_html=True)

st.title("オシハナ")
st.subheader("文章登録")
st.divider()
with st.expander("ガイド"):
    st.markdown("""
                このページでは、翻訳・音声再生に使う文章を登録・削除できます。<br><br>
                1. テキスト入力欄に新しい文章を入力し、「登録」ボタンを押すと、文章がリストに追加されます。<br>
                2. 登録された文章は、「翻訳再生」ページでボタンとして表示されます。<br>
                3. 削除したい文章を選択し、「削除」ボタンを押すと、文章がリストから削除されます。<br>
""", unsafe_allow_html=True)
ss = st.session_state
df = pd.read_csv("phrases.csv") #phrases.csvから短文リストを読み込む
ss.phrases = df['phrase'].dropna().tolist()
st.sidebar.header("メニュー")
st.sidebar.page_link("honyaku.py", label="翻訳再生") #サイドバーにページリンクを追加(ファイル名, 表示名)
st.sidebar.page_link("pages/form.py", label="文章登録")
#ここまでtest2に近い
new = st.text_input("文章を入力してください", placeholder="例: おはようございます", max_chars=100) 
#↑テキスト入力欄(ラベル, 薄く表示される例文, 最大文字数)
if st.button("登録", disabled=not new.strip(), type="primary", use_container_width=True):
    new = new.strip() #前後の空白を削除
    if new in ss.phrases:
        st.warning("この文章は既に登録されています。")
    else:
        ss.phrases.append(new) #新しい短文をリストに追加
        df = pd.DataFrame(ss.phrases, columns=["phrase"]) #DataFrameに変換
        df.to_csv("phrases.csv", index=False) #CSVファイルに保存
        st.success("文章を登録しました。")
        #st.rerun() #ページをリロードして更新されたリストを表示

option = st.selectbox("削除したい文章を選んでください", list(ss.phrases))

st.write("この文章を削除しますか？:", option)
if st.button("削除", disabled=not option, type="primary"):
    ss.phrases.remove(option)
    df = pd.DataFrame(ss.phrases, columns=["phrase"])
    df.to_csv("phrases.csv", index=False)
    st.success("文章を削除しました。")
    #st.rerun()
