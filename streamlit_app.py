import streamlit as st
import yfinance as yf
import pandas as pd
import ta
st.title("港美股两层监控系统")
st.subheader("第一层：大盘指数 | 第二层：自选个股")
# ==================== 第一层：固定指数 ====================
indexes = {
    "恒生指数": "^HSI",
    "纳斯达克100": "^NDX",
    "标普500": "^GSPC"
}
# ==================== 第二层：自选港股/美股 ====================
my_stocks = {
    "港股": ["00700.HK", "09988.HK"],
    "美股": ["AAPL", "MSFT", "MSTR"]
}
# 拿数据 + 计算RSI、MACD
def get_data(symbol):
    df = yf.Ticker(symbol).history(period="60d")
    df["rsi"] = ta.momentum.rsi(df["Close"], window=14)
    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    return df
  # 看有没有底部信号
def check_signal(df):
    latest = df.iloc[-1]
    signal = []

    if latest["rsi"] < 30:
        signal.append(f"RSI超卖 ({latest['rsi']:.1f})")

    if latest["macd"] > latest["macd_signal"]:
        signal.append("MACD偏多")

    return signal if signal else ["正常无信号"]
  # ==================== 显示第一层：指数 ====================
st.header("🔴 第一层：大盘指数")
for name, symbol in indexes.items():
    df = get_data(symbol)
    latest = df.iloc[-1]
    signals = check_signal(df)

    st.subheader(name)
    st.metric("价格", f"{latest['Close']:.2f}")
    st.write("信号：", signals)
    st.divider()
  # ==================== 显示第二层：自选股 ====================
st.header("🔵 第二层：自选港股 + 美股")

st.subheader("港股")
for symbol in my_stocks["港股"]:
    df = get_data(symbol)
    latest = df.iloc[-1]
    signals = check_signal(df)
    st.write(symbol)
    st.metric("价格", f"{latest['Close']:.2f}")
    st.write("信号：", signals)
    st.divider()

st.subheader("美股")
for symbol in my_stocks["美股"]:
    df = get_data(symbol)
    latest = df.iloc[-1]
    signals = check_signal(df)
    st.write(symbol)
    st.metric("价格", f"{latest['Close']:.2f}")
    st.write("信号：", signals)
    st.divider()
