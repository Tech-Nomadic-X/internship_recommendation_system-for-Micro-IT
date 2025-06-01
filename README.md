# 🎓 Internship Recommendation App

An intelligent internship recommendation system built with **Streamlit** that suggests internship domains based on a student's skill set. It also emails the top matches using **SendGrid**, with a professional HTML template and unsubscribe option.

## 🚀 Features

* 🔍 AI-powered internship domain recommendations using TF-IDF + Cosine Similarity
* 📩 Email delivery of results with **SendGrid**
* ✅ Custom CTA: “Apply Now” linking to [Google Form](https://forms.gle/7pet4PKXdMcR2H1B9)
* ⚠️ Spam notice: Users are asked to mark the email as “Not Spam” if it lands in Spam
* ❌ Unsubscribe functionality with in-app list management
* 📊 Clean and responsive UI using Streamlit

---

## 📁 Folder Structure

```
internship_app/
├── app.py
├── domain_profiles.csv         # Contains domain names and skills
├── unsubscribed.csv            # Generated automatically to track unsubscribed users
├── .streamlit/
│   └── secrets.toml            # Secure API keys (SendGrid config)
├── requirements.txt
├── README.md
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/internship-recommender.git
cd internship-recommender
pip install -r requirements.txt
```

---

## 🔑 Setup Secrets

Inside `.streamlit/secrets.toml`:

```toml
[sendgrid]
api_key = "your_sendgrid_api_key"
from_email = "your_verified_sender@example.com"
from_name = "Internship Recommender"
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📬 Email Disclaimer

If you requested an email but don’t see it, check your **Spam** folder. Please mark it as **"Not Spam"** to receive future updates properly.

---

## 🔗 License

This project is open-source under the MIT License.
Please give it a star if you like it.
          ____Bhooma Anand
