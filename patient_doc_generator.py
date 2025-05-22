import streamlit as st
from google import genai
from google.genai import types as genai_types
import json
from io import BytesIO
from docxtpl import DocxTemplate
import os

# --- Gemini API Function (corrected argument for generate_content_stream) ---
def get_structured_data_from_gemini(api_key: str, user_input_text: str) -> dict:
    """
    Processes natural language patient info using Gemini API (google-genai SDK)
    and returns structured data. Uses the client.models.generate_content_stream method.
    """
    client = genai.Client(api_key=api_key)

    model_name = "gemini-2.5-flash-preview-05-20" # As per your specification

    contents = [
        genai_types.Content(
            role="user",
            parts=[
                # Example of user input (already in Hebrew, good)
                genai_types.Part.from_text(text="""היי אני ידידיה זהו דוגמא בלבד, כשממיר את הקוד לפונקציה תשאיר את זה עם משתנה, ככה זה יימשך מתוך הצד לקוח

ידידיה בן 40 חולה"""),
            ],
        ),
        genai_types.Content(
            role="model",
            parts=[
                # Example of model output (values in Hebrew, keys in English, good)
                genai_types.Part.from_text(text="""{
  "name": "ידידיה",
  "age": "40",
  "kupat_cholim": "",
  "symptoms": "חולה",
  "ai_recommondation": ""
}"""),
            ],
        ),
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text=user_input_text),
            ],
        ),
    ]

    # System prompt remains in English as it defines JSON structure with English keys
    # which the Python code and DocxTemplate rely on.
    # The example "kupat_cholim: like מכבי or כללית etc" already has Hebrew examples.
    generate_content_config_object = genai_types.GenerateContentConfig(
        temperature=0,
        thinking_config=genai_types.ThinkingConfig(
            thinking_budget=0,
        ),
        response_mime_type="application/json",
        system_instruction=[
            genai_types.Part.from_text(text="""system prompt here
this is the system prompt. act as a patient info analuzer
analyze the attached user input, and return a json with the relevant fields. always return the fierlds. if the fiels is empty, just retirn it empty.

json:
name
age
kupat_cholim: like מכבי or כללית etc
symptoms
ai_recommondation:

here is the user input:"""),
        ],
    )

    full_response_text = ""
    try:
        stream = client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=generate_content_config_object,
        )
        for chunk in stream:
            if chunk.text:
                 full_response_text += chunk.text
        
        if not full_response_text.strip():
            raise ValueError("Received empty response from Gemini API.") # Internal error, can remain English or be translated

        data = json.loads(full_response_text)
        
        expected_keys = ["name", "age", "kupat_cholim", "symptoms", "ai_recommondation"]
        for key in expected_keys:
            if key not in data:
                data[key] = ""
            elif key == "age" and data.get(key) is not None: 
                data[key] = str(data[key])
            elif key == "age" and data.get(key) is None:
                 data[key] = ""

        if "age" in data and data["age"] is not None:
            data["age"] = str(data["age"])
        elif "age" not in data or data.get("age") is None:
            data["age"] = ""

        return data

    except json.JSONDecodeError as e:
        error_msg = f"שגיאת פיענוח JSON: {e}. תגובת Gemini: '{full_response_text}'"
        st.error(error_msg)
        return {"error": "כשל בפענוח JSON מ-Gemini", "details": error_msg, "name": "", "age": "", "kupat_cholim": "", "symptoms": "", "ai_recommondation": ""}
    except ValueError as e:
        # This specific ValueError is for empty response, can be more user-friendly
        if "Received empty response from Gemini API." in str(e):
            error_msg = f"שגיאת ערך: התקבלה תגובה ריקה מ-Gemini API. תגובת Gemini: '{full_response_text}'"
            details_msg = "ה-API של Gemini החזיר תגובה ריקה. ייתכן שיש בעיה בתקשורת או שהקלט לא עובד כראוי."
        else:
            error_msg = f"שגיאת ערך: {e}. תגובת Gemini: '{full_response_text}'"
            details_msg = error_msg
        st.error(error_msg)
        return {"error": "נתונים לא תקינים מ-Gemini", "details": details_msg, "name": "", "age": "", "kupat_cholim": "", "symptoms": "", "ai_recommondation": ""}
    except Exception as e:
        error_msg = f"שגיאה בקריאה ל-Gemini API: {type(e).__name__} - {e}. מודל: {model_name}."
        st.error(error_msg)
        if hasattr(e, 'response') and e.response: 
            st.error(f"פרטי תגובת API: {e.response}")
        return {"error": "הקריאה ל-Gemini API נכשלה", "details": error_msg, "name": "", "age": "", "kupat_cholim": "", "symptoms": "", "ai_recommondation": ""}


# --- Password Protection ---
def check_password():
    if "APP_PASSWORD" not in st.secrets:
        st.error("שגיאה קריטית: APP_PASSWORD אינו מוגדר בקבצי הסודות של Streamlit (.streamlit/secrets.toml).")
        st.stop()
        return False

    app_password = st.secrets["APP_PASSWORD"]

    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.markdown("<div dir='rtl'>", unsafe_allow_html=True) # Ensure RTL for password section
    password_input = st.text_input("הזן סיסמה כדי לגשת לאפליקציה:", type="password", key="password_field")

    if st.button("התחבר", key="login_button"):
        if password_input == app_password:
            st.session_state.password_correct = True
            st.markdown("</div>", unsafe_allow_html=True) # Close RTL div
            st.rerun()
        else:
            st.error("הסיסמה שגויה.")
            st.session_state.password_correct = False
    st.markdown("</div>", unsafe_allow_html=True) # Close RTL div if button not pressed or after error
    return False

# --- Main App ---
def main():
    st.set_page_config(page_title="מחולל מסמכי מטופלים", layout="wide")
    st.markdown("<div dir='rtl' style='text-align: right;'>", unsafe_allow_html=True)

    st.title("📝 מחולל מסמכי מטופלים")

    if not check_password():
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    try:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY לא נמצא בקבצי הסודות של Streamlit. אנא הגדר אותו ב- .streamlit/secrets.toml")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()
        return

    # --- 1. Privacy Warning ---
    st.warning(
        """
        **⚠️ אזהרת פרטיות חשובה:**

        נא **לא** להזין מידע אישי מזהה על מטופלים שעלול לחשוף את זהותם.
        לדוגמה: שם פרטי ושם משפחה מלאים, מספר תעודת זהות, כתובת מגורים, מספר טלפון, כתובת דוא"ל או כל פרט אחר המאפשר זיהוי חד-משמעי של המטופל.

        מומלץ להשתמש בראשי תיבות, שמות בדויים או תיאורים כלליים שאינם חושפים זהות, בהתאם למדיניות הפרטיות והאתיקה המקצועית.
        """
    )

    st.subheader("1. הזן פרטי פגישה (בשפה חופשית)")
    patient_info_natural = st.text_area("תאר את פרטי הפגישה עם המטופל, תסמינים, היסטוריה וכו':", height=250, key="patient_input_area")

    model_name_for_display = "gemini-2.5-flash-preview-05-20"


    if st.button("✨ הפק מסמך", key="generate_button"): # Changed button text slightly
        if not patient_info_natural.strip():
            st.warning("אנא הזן מידע כלשהו על הפגישה.")
            st.stop()

        with st.spinner(f"מעבד את הבקשה ומכין את המסמך באמצעות Gemini AI (מודל: {model_name_for_display})... אנא המתן."):
            structured_data = get_structured_data_from_gemini(gemini_api_key, patient_info_natural)

        # --- Error handling after Gemini call ---
        if "error" in structured_data and structured_data["error"]: # Check if error key exists and has a value
            # Error already displayed by get_structured_data_from_gemini
            # st.error(f"לא ניתן היה לעבד את הנתונים: {structured_data.get('details', 'שגיאה לא ידועה')}")
            st.markdown("</div>", unsafe_allow_html=True) # Close RTL div before stopping
            st.stop() # Stop further processing if Gemini returned an error structure
        elif not structured_data: # Should not happen if get_structured_data_from_gemini always returns a dict
            st.error("אירעה שגיאה בלתי צפויה: לא התקבלו נתונים מ-Gemini.")
            st.markdown("</div>", unsafe_allow_html=True) # Close RTL div
            st.stop()


        # --- No longer displaying structured_data directly ---
        # st.subheader("2. נתוני מטופל מובנים (מ-Gemini)")
        # st.json(structured_data)

        st.subheader("2. הפק והורד קובץ DOCX") # Renumbered from 3 to 2
        template_file = "patient_template.docx"

        if not os.path.exists(template_file):
            st.error(f"שגיאה: קובץ התבנית DOCX '{template_file}' לא נמצא.")
            st.info(f"אנא צור קובץ '{template_file}' באותה תיקייה של הסקריפט. השתמש במצייני מקום כמו {{{{name}}}}, {{{{age}}}} וכו' (אלו צריכים להיות באנגלית כפי שהם מוגדרים בקוד).")
            st.markdown("</div>", unsafe_allow_html=True) # Close RTL div
            st.stop()

        try:
            doc = DocxTemplate(template_file)
                # EXPANDED CONTEXT - ensure all placeholders from DOCX are here
            context = {
                "name": structured_data.get("name", ""),
                "age": str(structured_data.get("age", "")), # Ensure age is string
                "kupat_cholim": structured_data.get("kupat_cholim", ""),
                "symptoms": structured_data.get("symptoms", ""),
                "ai_recommondation": structured_data.get("ai_recommondation", ""),
        
                # Placeholders from INTRODUCTION / SETTING
                "referring_person_details": structured_data.get("referring_person_details", ""), # New - AI might not provide yet
                "referral_reason_source_and_quote": structured_data.get("referral_reason_source_and_quote", ""), # New
                "initial_patient_complaint": structured_data.get("initial_patient_complaint", ""), # New
                "meeting_location": structured_data.get("meeting_location", ""), # New
                "other_participants": structured_data.get("other_participants", ""), # New
        
                # Placeholders from S - SUBJECTIVE
                "patient_story_details": structured_data.get("patient_story_details", ""), # New
                "bio_psycho_social_background": structured_data.get("bio_psycho_social_background", ""), # New
                "significant_life_events": structured_data.get("significant_life_events", ""), # New
                "coping_mechanisms_strengths_weaknesses": structured_data.get("coping_mechanisms_strengths_weaknesses", ""), # New
                "past_present_treatments": structured_data.get("past_present_treatments", ""), # New
                "treatment_expectations": structured_data.get("treatment_expectations", ""), # New
        
                # Placeholders from O - OBJECTIVE & OBSERVATIONS
                "objective_patient_description": structured_data.get("objective_patient_description", ""), # New
                "reports_from_other_systems": structured_data.get("reports_from_other_systems", ""), # New
                "questionnaire_results": structured_data.get("questionnaire_results", ""), # New
                "holocaust_survivor_status": structured_data.get("holocaust_survivor_status", ""), # New
                "violence_abuse_screening_details": structured_data.get("violence_abuse_screening_details", ""), # New
                "rights_utilization_mapping": structured_data.get("rights_utilization_mapping", ""), # New
                "medical_poa_guardianship_status": structured_data.get("medical_poa_guardianship_status", ""), # New
                "other_objective_information": structured_data.get("other_objective_information", ""), # New
        
                # Placeholders from A - ASSESSMENT
                "functional_assessment_details": structured_data.get("functional_assessment_details", ""), # New
                "problem_list_sw_impression": structured_data.get("problem_list_sw_impression", ""), # New
                "identified_resources": structured_data.get("identified_resources", ""), # New
                "inhibiting_factors": structured_data.get("inhibiting_factors", ""), # New
                "overall_assessment_summary": structured_data.get("overall_assessment_summary", ""), # New
        
                # Placeholders from P - PLAN
                "treatment_plan_details": structured_data.get("treatment_plan_details", ""), # New
                "additional_vital_information_for_plan": structured_data.get("additional_vital_information_for_plan", ""), # New
                "patient_family_guidance_plan": structured_data.get("patient_family_guidance_plan", ""), # New
                "rights_accessibility_plan_details": structured_data.get("rights_accessibility_plan_details", ""), # New
                "follow_up_referral_mediation_plan": structured_data.get("follow_up_referral_mediation_plan", ""), # New
                "duty_to_report_plan": structured_data.get("duty_to_report_plan", ""), # New
                "treatment_contract_registration_notes": structured_data.get("treatment_contract_registration_notes", ""), # New
                "no_further_intervention_justification": structured_data.get("no_further_intervention_justification", ""), # New
        
                # Placeholders from S - SUMMARY (Final)
                "gender": structured_data.get("gender", ""), # New
                "marital_status": structured_data.get("marital_status", ""), # New
                "summary_bps_assessment_brief": structured_data.get("summary_bps_assessment_brief", ""), # New
                "summary_treatment_goals_brief": structured_data.get("summary_treatment_goals_brief", ""), # New
                "summary_intervention_plan_recommendations": structured_data.get("summary_intervention_plan_recommendations", "") # New
            }
            doc.render(context)

            bio = BytesIO()
            doc.save(bio)
            bio.seek(0)

            doc_filename = f"{str(context.get('name', 'מטופל')).replace(' ', '_')}_document.docx"
            st.download_button(
                label="📥 הורד מסמך מטופל (DOCX)",
                data=bio,
                file_name=doc_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"שגיאה ביצירת קובץ DOCX: {e}")
            st.error(f"נתונים ששימשו לתבנית (ייתכן שחסר מפתח או שהערך אינו תקין): {context}")
            # Consider logging the full exception traceback for debugging
            # import traceback
            # st.error(traceback.format_exc())

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
