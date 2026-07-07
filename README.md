@app.delete("/history")
def clear_history(db: Session = Depends(get_db)):

    db.query(AnalysisHistory).delete()

    db.query(IOCCache).delete()

    db.commit()

    return {
        "message": "History and cache cleared successfully."
    }

    

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

        
