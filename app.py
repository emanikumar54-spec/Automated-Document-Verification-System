
import streamlit as st
import os
import tempfile

from modules.ocr_engine import extract_document_text
from modules.information_extraction import extract_information
from modules.document_comparison import (
    compare_documents,
    generate_summary
)

from database import (
    initialize_database,
    save_document,
    save_comparison,
    get_documents,
    get_comparisons
)


# PAGE CONFIGURATION
st.set_page_config(
    page_title="DocVerify AI",
    page_icon="📄",
    layout="wide"
)

initialize_database()


# CUSTOM STYLE
st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: white;
}
h1, h2, h3 {
    color: #e2e8f0;
}
[data-testid="stMetric"] {
    background: #172033;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.title("DOCVERIFY AI")
st.sidebar.caption("Automated Document Verification")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Documents",
        "Compare Documents",
        "Verification History"
    ]
)


# DASHBOARD
if page == "Dashboard":

    st.title("Document Verification Dashboard")
    st.write("Automated Information Inconsistency Detection System")

    documents = get_documents()
    comparisons = get_comparisons()

    col1, col2, col3 = st.columns(3)

    col1.metric("Documents Uploaded", len(documents))
    col2.metric("Comparisons", len(comparisons))

    mismatches = sum(
        int(__import__("json").loads(row["summary"]).get("mismatching", 0))
        for row in comparisons
    )

    col3.metric("Mismatches Detected", mismatches)

    st.divider()

    st.subheader("System Features")

    st.write("• Automated OCR text extraction")
    st.write("• Personal information identification")
    st.write("• Document comparison")
    st.write("• Inconsistency detection")
    st.write("• PDF verification reports (coming next)")


# UPLOAD DOCUMENTS
elif page == "Upload Documents":

    st.title("Upload Documents")

    uploaded_file = st.file_uploader(
        "Choose PDF or Image",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file:

        if st.button("Process Document"):

            extension = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            try:
                with st.spinner("Extracting document information..."):

                    text = extract_document_text(temp_path)
                    information = extract_information(text)

                    document_id = save_document(
                        uploaded_file.name,
                        extension.upper().replace(".", ""),
                        text,
                        information
                    )

                st.success(
                    f"Document processed successfully! ID: {document_id}"
                )

                st.subheader("Extracted Information")
                st.json(information)

                with st.expander("View Extracted Text"):
                    st.text(text)

            except Exception as error:
                st.error(f"Processing failed: {error}")

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)


# COMPARE DOCUMENTS
elif page == "Compare Documents":

    st.title("Compare Documents")

    documents = get_documents()

    if len(documents) < 2:

        st.info("Upload at least two documents before comparing.")

    else:

        options = {
            f"ID {doc['id']} - {doc['filename']}": doc
            for doc in documents
        }

        col1, col2 = st.columns(2)

        with col1:
            selected1 = st.selectbox(
                "Select First Document",
                list(options.keys()),
                key="doc1"
            )

        with col2:
            selected2 = st.selectbox(
                "Select Second Document",
                list(options.keys()),
                index=1,
                key="doc2"
            )

        if st.button("Compare Documents"):

            doc1 = options[selected1]
            doc2 = options[selected2]

            if doc1["id"] == doc2["id"]:
                st.warning("Select two different documents.")

            else:

                import json

                data1 = json.loads(doc1["extracted_data"])
                data2 = json.loads(doc2["extracted_data"])

                results = compare_documents(data1, data2)
                summary = generate_summary(results)

                save_comparison(
                    doc1["id"],
                    doc2["id"],
                    results,
                    summary
                )

                st.subheader("Comparison Results")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total Fields", summary["total_fields"])
                col2.metric("Matching", summary["matching"])
                col3.metric("Mismatching", summary["mismatching"])
                col4.metric("Missing", summary["missing"])

                st.divider()

                for field, result in results.items():

                    with st.expander(
                        f"{field.replace('_', ' ').title()} — {result['status']}"
                    ):

                        st.write(
                            "Document 1:", result["document_1"]
                        )

                        st.write(
                            "Document 2:", result["document_2"]
                        )

                        st.write(
                            "Status:", result["status"]
                        )


# HISTORY
elif page == "Verification History":

    st.title("Verification History")

    comparisons = get_comparisons()

    if not comparisons:
        st.info("No comparison history available.")

    else:

        import json

        for record in comparisons:

            with st.expander(
                f"Comparison #{record['id']} — {record['created_at']}"
            ):

                st.json(json.loads(record["summary"]))
                st.json(json.loads(record["results"]))


