import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transcript Missing Word Tool")

st.title("Transcript Missing Word Finder")

st.write("Upload your Excel file with two columns:")
st.write("Column A = Correct Script")
st.write("Column B = ASR Transcript")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

def find_missing(correct, asr):
    correct_words = correct.lower().split()
    asr_words = asr.lower().split()
    missing = [word for word in correct_words if word not in asr_words]
    return " ".join(missing)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    if len(df.columns) < 2:
        st.error("Excel must have at least 2 columns")
    else:
        results = []

        for i in range(len(df)):
            correct_text = str(df.iloc[i, 0])
            asr_text = str(df.iloc[i, 1])
            missing_words = find_missing(correct_text, asr_text)
            results.append(missing_words)

        df["Missing Words"] = results
        st.success("Comparison Completed")

        st.dataframe(df)

        st.download_button(
            label="Download Result Excel",
            data=df.to_excel(index=False),
            file_name="missing_words_output.xlsx"
        )
