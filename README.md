# AI-Powered Therapy Session Summarizer

## 📝 About This Application

This application is designed to assist emotional therapists by transforming free-form notes from patient sessions into coherent, structured narrative summaries. The therapist inputs session details in natural language, and the system, utilizing an advanced language model (Gemini AI), generates a flowing summary of the meeting. This summary is then provided as a downloadable DOCX file, ready for use or further editing.

The goal is to save therapists valuable time, allowing them to focus more on their patients and less on documentation, while maintaining a high standard for session summaries.

**Important:** The application emphasizes patient privacy and guides users to avoid entering personally identifiable information (PII).

## 🚀 Key Technologies & Components

*   **Streamlit:** For creating the interactive and user-friendly web interface.
*   **Google Gemini AI (via `google-genai` SDK):** The core engine for natural language processing and generating narrative summaries.
*   **DocxTemplater (`docxtpl`):** For dynamically creating DOCX files based on a template and processed data.
*   **Python:** The primary programming language for the application.

## 🌐 How to Use

Using the application is simple and convenient, done directly through your web browser:

1.  **Access the Application:**
    *   [Click here to access the application](https://shortherapist.streamlit.app/)
2.  **Login:** Upon accessing the site, you will be prompted to enter a password (this password is pre-configured by the system administrator).
3.  **Enter Session Notes:** After logging in, a large text area will be displayed. Type or paste your notes from the patient session here, in free-form Hebrew.
    *   **Remember the privacy warning:** Do not enter any personally identifiable information about patients.
4.  **Generate Summary:** Click the "✨ הפק סיכום פגישה" (Generate Session Summary) button.
5.  **View and Download:**
    *   The system will process the information and display the narrative summary on the screen.
    *   A "📥 הורד סיכום פגישה (DOCX)" (Download Session Summary (DOCX)) button will then appear, allowing you to download the summary as a Word file.

---

I hope this application proves helpful to you!
