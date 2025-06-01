# app.py (final version with unsubscribe support)
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("domain_profiles.csv")

# Load unsubscribed emails (if any)
def load_unsubscribed():
    if os.path.exists("unsubscribed.csv"):
        return pd.read_csv("unsubscribed.csv")['email'].tolist()
    return []

def save_unsubscribed(email):
    with open("unsubscribed.csv", "a") as f:
        f.write(email + "\n")

# Recommendation logic
def get_recommendations(user_input, top_n=3):
    df = load_data()
    df["Profile"] = df["Skills"].str.replace(",", " ")
    user_profile = user_input.replace(",", " ")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["Profile"].tolist() + [user_profile])
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    df["Match Score"] = cosine_sim.flatten()
    top_matches = df.sort_values(by="Match Score", ascending=False).head(top_n)
    return top_matches

# SendGrid Email Sender
def send_email(name, to_email, matches_df):
    from_email = st.secrets["sendgrid"]["from_email"]
    from_name = st.secrets["sendgrid"]["from_name"]
    api_key = st.secrets["sendgrid"]["api_key"]

    logo_url = "https://res.cloudinary.com/dzyhrywhg/image/upload/v1748741198/chat-icon_ygiory.png"
    cta_link = "https://forms.gle/7pet4PKXdMcR2H1B9"
    unsubscribe_link = "https://internship-ai.streamlit.app/?page=unsubscribe"

    recommendations_html = ""
    for _, row in matches_df.iterrows():
        recommendations_html += f"""
        <div style=\"margin-bottom: 16px;\">
            <strong>{row['Domain']}</strong><br>
            🔍 Match Score: {row['Match Score'] * 100:.1f}%<br>
            🧠 Skills: {row['Skills']}
        </div>
        """

    email_content = f"""
    <div style=\"font-family: Arial, sans-serif; color: #333;\">
        <img src=\"{logo_url}\" alt=\"Internship Recommender\" width=\"80\" style=\"margin-bottom: 20px;\">
        <h2 style=\"color: #0059ff;\">Hi {name},</h2>
        <p>Based on your skills, here are your top internship matches:</p>
        {recommendations_html}
        <a href=\"{cta_link}\" style=\"display:inline-block; background-color:#0059ff; color:#fff; padding:10px 20px; text-decoration:none; border-radius:6px; font-weight:bold;\">Apply Now</a>
        <p style=\"margin-top: 30px; font-size: 12px; color: #888;\">
            — Internship Recommender Bot<br>
            If this mail goes to spam, please mark it as 'Not Spam'.<br>
            <a href=\"{unsubscribe_link}\">Unsubscribe</a>
        </p>
    </div>
    """

    try:
        message = Mail(
            from_email=Email(from_email, from_name),
            to_emails=To(to_email),
            subject="Your Top Internship Recommendations",
            html_content=Content("text/html", email_content)
        )
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        return True
    except Exception as e:
        st.error(f"❌ Email sending failed: {e}")
        return False

# Page router
def render_unsubscribe():
    st.title("🚫 Unsubscribe")
    email = st.text_input("Enter your email to unsubscribe")
    if st.button("Unsubscribe"):
        if email:
            save_unsubscribed(email)
            st.success("You have been unsubscribed and will no longer receive emails.")
        else:
            st.warning("Please enter a valid email.")

def render_main():
    st.title("🎓 Internship Recommender")
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Your Email")
    skills = st.text_area("💼 Enter your skills (comma-separated, e.g., Python, SQL, TensorFlow)")
    send_email_opt = st.checkbox("📩 Email me my recommendations")

    if st.button("🔎 Get Recommendations"):
        if not name or not email or not skills:
            st.warning("⚠️ Please complete all fields.")
        elif email in load_unsubscribed():
            st.error("❌ You have unsubscribed from email updates. Please contact support if this was a mistake.")
        else:
            results = get_recommendations(skills)
            if results["Match Score"].max() == 0:
                st.info("😕 No strong matches found. Try adding more technical or relevant skills.")
            else:
                st.subheader("📌 Top Internship Recommendations")
                for _, row in results.iterrows():
                    st.markdown(f"**✅ {row['Domain']}**  \n🔍 Match Score: `{row['Match Score']*100:.1f}%`  \n🧠 Skills: `{row['Skills']}`\n")

                if send_email_opt:
                    if send_email(name, email, results):
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error("❌ Could not send the email. Please try again.")

# Main entry
page = st.query_params.get("page", "main")
if page == "unsubscribe":
    render_unsubscribe()
else:
    render_main()
