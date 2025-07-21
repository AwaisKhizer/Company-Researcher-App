import streamlit as st
from crew import run_company_report

# Streamlit UI setup
st.set_page_config(page_title="AI Company Researcher", layout="wide")
st.title("🔍 Company Research Assistant (Groq + CrewAI)")

st.markdown("""
This assistant uses AI agents to:
- 🔎 Search for recent company news
- 🧠 Scrape website content
- 📝 Generate a complete business report
""")

with st.form("research_form"):
    company = st.text_input("Company Name", placeholder="e.g. Anthropic")
    website = st.text_input("Official Website URL", placeholder="e.g. https://www.anthropic.com")
    submitted = st.form_submit_button("🚀 Run Research")

if submitted:
    if not company or not website:
        st.error("Please provide both company name and website URL.")
    else:
        with st.spinner(f"Generating research report for {company}..."):
            try:
                result = run_company_report(company, website)
                st.success("✅ Report generated!")
                st.markdown(result, unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Report",
                    data=result,
                    file_name=f"{company.lower().replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
