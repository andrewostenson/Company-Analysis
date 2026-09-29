import streamlit as st
import database as db

st.title("RAG Dashboard")
ticker = st.selectbox("Select a stock ticker: ", ["NVDA", "AAPL", "GOOGL", "MSFT", "AMZN", "META", "BRK.A", "AVGO", "TSLA", "LLY"])
question = st.text_input("Ask a question")

if st.button("Analyze"):
    st.write("Ticker: ", ticker)
    st.write("Question: ", question)
    db.buildCollection(ticker)

    embeddedq = db.embedQuestion(question)
    collection = db.queryCollection(embeddedq)
    answer = db.gptQuery(question, collection)

    st.write(answer)

