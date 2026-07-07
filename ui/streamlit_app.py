import os
from io import BytesIO
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="IOC Threat Assessment Agent", layout="wide")
st.title("IOC Threat Assessment Agent")
st.caption("Unified VirusTotal + AbuseIPDB enrichment with SQLite cache and history")

page = st.sidebar.radio("Navigation", ["Single IOC", "Bulk Upload", "History"])


def verdict_color(verdict: str):
    return {
        "Clean": "green",
        "Suspicious": "orange",
        "Malicious": "red",
        "Critical": "darkred",
        "Invalid": "gray",
    }.get(verdict, "blue")


if page == "Single IOC":
    st.subheader("Analyze single IOC")
    ioc = st.text_input("Enter IP, domain, URL, MD5, SHA1, or SHA256")
    if st.button("Analyze", type="primary") and ioc.strip():
        with st.spinner("Analyzing IOC..."):
            resp = requests.post(f"{API_BASE}/analyze", json={"ioc": ioc}, timeout=60)
        if resp.ok:
            data = resp.json()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("IOC Type", data["type"])
            c2.metric("Risk Score", data["score"])
            c3.markdown(f"**Verdict:** :{verdict_color(data['verdict'])}[{data['verdict']}]")
            c4.metric("Sources", len(data.get("sources", {})))

            st.markdown("### Reasons")
            for reason in data.get("reasons", []):
                st.write(f"- {reason}")

            st.markdown("### Recommendation")
            st.info(data.get("recommendation", "Review manually."))

            st.markdown("### Raw Source Results")
            st.json(data.get("sources", {}))
        else:
            st.error(resp.text)

elif page == "Bulk Upload":
    st.subheader("Bulk IOC Analysis")
    st.write("Upload a CSV/XLSX with an `ioc` column or IOC values in the first column.")
    uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
    if uploaded and st.button("Analyze File", type="primary"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        with st.spinner("Analyzing bulk IOCs..."):
            resp = requests.post(f"{API_BASE}/bulk-analyze", files=files, timeout=300)
        if resp.ok:
            payload = resp.json()
            st.success(f"Analyzed {payload['count']} IOCs")
            table = pd.DataFrame(payload["table"])
            st.dataframe(table, use_container_width=True)

            csv_data = table.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV Results", csv_data, "ioc_analysis_results.csv", "text/csv")

            xlsx_buffer = BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
                table.to_excel(writer, index=False, sheet_name="IOC Results")
            st.download_button(
                "Download Excel Results",
                xlsx_buffer.getvalue(),
                "ioc_analysis_results.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(resp.text)

elif page == "History":

    st.subheader(
        "Analysis History"
    )

    limit = st.slider(
        "Rows",
        10,
        500,
        50
    )

    col1, col2 = st.columns(2)

    refresh_clicked = col1.button(
        "Refresh History"
    )

    delete_clicked = col2.button(
        "Delete History",
        type="secondary"
    )

    if delete_clicked:

        response = requests.delete(
            f"{API_BASE}/history",
            timeout=30
        )

        if response.ok:

            st.success(
                response.json()["message"]
            )

            st.rerun()

        else:

            st.error(
                response.text
            )

    resp = requests.get(
        f"{API_BASE}/history",
        params={
            "limit": limit
        },
        timeout=30
    )

    if resp.ok:

        df = pd.DataFrame(
            resp.json()
        )

        if df.empty:

            st.info(
                "No analysis history found."
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )

    else:

        st.error(
            resp.text
        )

        

