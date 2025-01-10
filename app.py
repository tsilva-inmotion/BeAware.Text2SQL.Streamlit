import requests
import sqlparse
import streamlit as st

URL = st.secrets["URL"]

st.title("BeAware.Text2SQL")

user_input = st.text_input("Enter your question:", key="user_input")

if user_input:
    response = requests.get(
        f"{URL}/api/v1/translate-to-sql",
        params={"question": user_input},
        headers={"accept": "application/json"},
    )
    if response.status_code == 200:
        sql_query = response.json().get("sql_query")
        formatted_sql = sqlparse.format(sql_query, reindent=True, keyword_case="upper")
        st.code(formatted_sql, language="sql")

        # Extract and display execution time
        process_time = response.headers.get("x-process-time")
        if process_time:
            st.write(f"**Execution Time:** {float(process_time):.4f} seconds")

    else:
        st.error("Error: Unable to process the request.")
