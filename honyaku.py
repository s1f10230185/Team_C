import streamlit as st #streamlitでは変数の変化が保存されない?らしいので、st.session_stateを使って状態を保存するらしい
from deep_translator import GoogleTranslator
import pandas as pd
from google.cloud import texttospeech
st.set_page_config(page_title="オシハナ", layout="centered") #ページのタイトルとレイアウト(広めか、中央寄せか)を設定してる
GOOGLE_CREDENTIALS_PATH = r"C:/Users/飲める醤油/Documents/path/verdant-axiom-474123-u5-3216f94bb49a.json"  # 認証JSONファイルパスを指定

st.markdown('<style>[data-testid="stSidebarNav"]{display:none}</style>', unsafe_allow_html=True) #サイドバーのページ名を非表示できます、ただのCSSなのでコメントアウトしても大丈夫でした
ss = st.session_state #長いので略してる  session_stateは別ページでも共有されるので便利そう
target_lang = ss.get("target_lang", "en") #翻訳先の言語コード(英語)
df = pd.read_csv("phrases.csv") #phrases.csvから文章リストを読み込む
ss.phrases = df['phrase'].dropna().tolist() #NaNを除く
#↑のss.phrasesでphraseという変数にアクセスしている
ss.is_playing = ss.get("is_playing", False) #is_playingはフラグ管理とかに使う
ss.tts_client = ss.get("tts_client", texttospeech.TextToSpeechClient.from_service_account_json(GOOGLE_CREDENTIALS_PATH))
def translate_text(text, target_lang):
# 日本語から他言語への翻訳
  translated_text = GoogleTranslator(source='ja', target=target_lang).translate(text)
  return translated_text

def voice_speak (translated_text, lang_code):
  lang_map = {
        "en": "en-US",
        "zh-CN": "cmn-CN",
        "vi": "vi-VN",
        "tl": "tl-PH"
    }
  response = ss.tts_client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=translated_text),
        voice=texttospeech.VoiceSelectionParams(
            language_code=lang_map[lang_code],
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
    )
  st.audio(response.audio_content, format="audio/mp3",autoplay=True)
langs = {
    "英語": "en", "中国語": "zh-CN", "ベトナム語": "vi","タガログ語": "tl"
} #言語選択のための辞書(表示名(key):値(ラベル))  ↓のヘッダー部分で使う

#ここからヘッダー部
col1, col2 = st.columns([2, 1]) #2:1の比率で2つのカラム(要素)を作成
            # ↑では更新しない値なので、ss.ではなくst.でOK
col1.title("オシハナ") #col1にタイトルを表示
lang_name = col2.selectbox("翻訳先", list(langs.keys()), label_visibility="collapsed") #(カテゴリ名, 選択肢のリスト(langsのkeyをリスト化), ラベルを非表示)
with st.expander("ガイド"):
    st.markdown("""
                このアプリは、タッチした文章を翻訳して音声で再生するものです。<br><br>
                1. 右上の選択ボックスで翻訳先の言語を選択します。<br>
                2. 文章ボタンをクリックすると、選択した言語に翻訳された音声が再生されます。<br>
                3. 新しい文章を追加したい場合は、サイドバーから「文章登録」ページに移動してください。<br>
""", unsafe_allow_html=True)
st.sidebar.header("メニュー") #サイドバーのヘッダー
st.sidebar.page_link("honyaku.py", label="翻訳再生") #サイドバーにページリンクを追加(ファイル名, 表示名)
st.sidebar.page_link("pages/form.py", label="文章登録")
st.divider() #区切り線(なくても動く)
st.subheader("文章リスト") #そのまま小見出しのこと

for i, p in enumerate(ss.phrases): #ss.phrasesの中身を一つずつ取り出してpに代入
    if st.button(p, key=f"p{i}", disabled=ss.is_playing, use_container_width=True): #pの中身をボタンにして表示(ボタンの名前, ボタン独自のkey, is_playingがTrueならボタンを押せなくする, ボタンをいっぱいに広げる)
        ss.is_playing = True
        translated_text = translate_text(p, langs[lang_name]) #翻訳されたテキストを取得
        voice_speak(translated_text, langs[lang_name])
        print(translated_text)
        ss.is_playing = False
    #↑のkeyは同じ名前のボタンがあるとエラーになるので、f"p{i}" により、p0, p1, p2 … のように番号付きキーを自動生成


