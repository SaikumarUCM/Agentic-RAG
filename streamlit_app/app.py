import json

import requests
import streamlit as st
import os

UPLOAD_FOLDER = "storage/uploads"
AIRFLOW_UPLOAD_FOLDER = "/opt/airflow/storage/uploads"  # path as seen inside Airflow container

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("RAG Document Upload")

uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt", "docx"])

if uploaded_file:
    path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    airflow_path = os.path.join(AIRFLOW_UPLOAD_FOLDER, uploaded_file.name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved: {uploaded_file.name}")

    if st.button("Send for Indexing"):
        url = "http://localhost:8080/api/v1/dags/rag_ingest_dag/dagRuns"

        payload = {
            "conf": {
                "file_path": airflow_path
            }
        }

        r = requests.post(
            url,
            json=payload,
            auth=("airflow", "airflow")
        )
 
        if r.status_code in (200, 201):
            st.success("Airflow DAG triggered successfully!")
            st.json(r.json())
        else:
            st.error(f"Failed to trigger DAG: {r.status_code}")
            st.write(r.text)

st.divider()
st.subheader("Ask a Question")

user_query = st.text_area("Enter your query", placeholder="Ask something about your documents...")

if st.button("Submit"):
    if not user_query.strip():
        st.warning("Please enter a query before submitting.")
    else:
        st.markdown("**Answer:**")
        response_placeholder = st.empty()
        full_response = ""

        with requests.post(
            "http://localhost:8000/chat",
            json={"prompt": user_query},
            stream=True,
        ) as r:
            if r.status_code == 200:
                for line in r.iter_lines():
                    if line:
                        line = line.decode("utf-8")
                        if line == "data: [DONE]":
                            break
                        if line.startswith("data: "):
                            token = json.loads(line[6:])["token"]
                            full_response += token
                            response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
            else:
                st.error(f"Request failed: {r.status_code}")
                st.write(r.text)
