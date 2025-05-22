import streamlit as st
from google import genai
from google.genai import types as genai_types
import json
from io import BytesIO
from docxtpl import DocxTemplate
import os

# --- Gemini API Function (corrected argument for generate_content_stream) ---
# --- Gemini API Function (Improved Prompt & Examples) ---
def get_structured_data_from_gemini(api_key: str, user_input_text: str) -> dict:
    """
    Processes natural language patient info using Gemini API (google-genai SDK)
    and returns structured data. Aims for comprehensive extraction for a detailed template.
    """
    client = genai.Client(api_key=api_key)

    # Using the model name from your latest snippet
    model_name = "gemini-2.5-flash-preview-05-20"

    # This list should contain ALL placeholders used in your patient_template.docx
    all_template_keys = [
        "name", "age", "kupat_cholim", "symptoms", "ai_recommondation",
        "referring_person_details", "referral_reason_source_and_quote",
        "initial_patient_complaint", "meeting_location", "other_participants",
        "patient_story_details", "bio_psycho_social_background",
        "significant_life_events", "coping_mechanisms_strengths_weaknesses",
        "past_present_treatments", "treatment_expectations",
        "objective_patient_description", "reports_from_other_systems",
        "questionnaire_results", "holocaust_survivor_status",
        "violence_abuse_screening_details", "rights_utilization_mapping",
        "medical_poa_guardianship_status", "other_objective_information",
        "functional_assessment_details", "problem_list_sw_impression",
        "identified_resources", "inhibiting_factors", "overall_assessment_summary",
        "treatment_plan_details", "additional_vital_information_for_plan",
        "patient_family_guidance_plan", "rights_accessibility_plan_details",
        "follow_up_referral_mediation_plan", "duty_to_report_plan",
        "treatment_contract_registration_notes", "no_further_intervention_justification",
        "gender", "marital_status", "summary_bps_assessment_brief",
        "summary_treatment_goals_brief", "summary_intervention_plan_recommendations"
    ]

    # --- Enhanced Few-Shot Examples ---
    contents = [
        # Example 1: More detailed input and output
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text="""מפגש ראשוני עם שרה כהן (שם בדוי), בת 45, נשואה + 3. הופנתה ע"י רופא משפחה ד"ר לוי ממרפאת 'השלום' עקב תחושות דכדוך וחרדה מזה כחצי שנה, מאז שפוטרה מעבודתה כגרפיקאית. קופ"ח: מכבי. מתארת קשיי שינה, חוסר תיאבון וירידה בחשק לעשות דברים שאהבה. בעבר טופלה פסיכולוגית למשך שנה סביב גיל 30 עקב משבר אישי. מצפה מהטיפול לקבל כלים להתמודדות ולהרגיש טוב יותר עם עצמה. הפגישה התקיימה בקליניקה."""),
            ],
        ),
        genai_types.Content(
            role="model",
            parts=[
                genai_types.Part.from_text(text=json.dumps({
                    "name": "שרה כהן (שם בדוי)",
                    "age": "45",
                    "gender": "נקבה", # Inferred
                    "marital_status": "נשואה + 3",
                    "kupat_cholim": "מכבי",
                    "symptoms": "תחושות דכדוך וחרדה, קשיי שינה, חוסר תיאבון, ירידה בחשק",
                    "referring_person_details": "רופא משפחה ד\"ר לוי, מרפאת 'השלום'",
                    "referral_reason_source_and_quote": "הופנתה עקב תחושות דכדוך וחרדה",
                    "initial_patient_complaint": "תחושות דכדוך וחרדה",
                    "meeting_location": "קליניקה",
                    "other_participants": "", # Assuming only Sarah and therapist
                    "patient_story_details": "מזה כחצי שנה, מאז שפוטרה מעבודתה כגרפיקאית. מתארת קשיי שינה, חוסר תיאבון וירידה בחשק לעשות דברים שאהבה.",
                    "bio_psycho_social_background": "פוטרה מעבודתה כגרפיקאית לפני כחצי שנה. נשואה עם שלושה ילדים.",
                    "significant_life_events": "פיטורין מעבודה (לאחרונה), משבר אישי (סביב גיל 30)",
                    "coping_mechanisms_strengths_weaknesses": "", # Not detailed in this input
                    "past_present_treatments": "טופלה פסיכולוגית למשך שנה סביב גיל 30",
                    "treatment_expectations": "לקבל כלים להתמודדות ולהרגיש טוב יותר עם עצמה",
                    "objective_patient_description": "", # Requires therapist's observation
                    "reports_from_other_systems": "",
                    "questionnaire_results": "",
                    "holocaust_survivor_status": "",
                    "violence_abuse_screening_details": "",
                    "rights_utilization_mapping": "",
                    "medical_poa_guardianship_status": "",
                    "other_objective_information": "",
                    "functional_assessment_details": "ירידה בתפקוד עקב קשיי שינה, חוסר תיאבון וירידה בחשק.",
                    "problem_list_sw_impression": "דכדוך וחרדה על רקע אובדן תעסוקתי, ירידה בתפקוד.",
                    "identified_resources": "פנתה לטיפול, תמיכה משפחתית (נשואה +3)",
                    "inhibiting_factors": "",
                    "overall_assessment_summary": "",
                    "treatment_plan_details": "",
                    "additional_vital_information_for_plan": "",
                    "patient_family_guidance_plan": "",
                    "rights_accessibility_plan_details": "",
                    "follow_up_referral_mediation_plan": "",
                    "duty_to_report_plan": "",
                    "treatment_contract_registration_notes": "",
                    "no_further_intervention_justification": "",
                    "summary_bps_assessment_brief": "",
                    "summary_treatment_goals_brief": "",
                    "summary_intervention_plan_recommendations": "",
                    "ai_recommondation": "הפיטורין נראים כגורם מרכזי למצב הנוכחי. יש מקום לבחון אסטרטגיות התמודדות עם אובדן ושינוי תעסוקתי."
                }, ensure_ascii=False)), # ensure_ascii=False for Hebrew in JSON string
            ],
        ),
        # Example 2: Simpler input, focusing on different fields, some missing
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text="""דני, בן 28, הגיע לפגישה ביוזמתו. סטודנט. מתאר קושי בריכוז בלימודים לאחרונה ותחושת 'תקיעות'. לא מקבל טיפול תרופתי. חבר בקופ"ח לאומית. רוצה להבין מה עובר עליו."""),
            ],
        ),
        genai_types.Content(
            role="model",
            parts=[
                genai_types.Part.from_text(text=json.dumps({
                    "name": "דני",
                    "age": "28",
                    "gender": "זכר", # Inferred
                    "marital_status": "", # Not mentioned
                    "kupat_cholim": "לאומית",
                    "symptoms": "קושי בריכוז בלימודים, תחושת 'תקיעות'",
                    "referring_person_details": "פניה עצמית",
                    "referral_reason_source_and_quote": "פניה עצמית",
                    "initial_patient_complaint": "קושי בריכוז בלימודים ותחושת 'תקיעות'",
                    "meeting_location": "", # Not mentioned
                    "other_participants": "",
                    "patient_story_details": "סטודנט. מתאר קושי בריכוז בלימודים לאחרונה ותחושת 'תקיעות'.",
                    "bio_psycho_social_background": "סטודנט.",
                    "significant_life_events": "",
                    "coping_mechanisms_strengths_weaknesses": "",
                    "past_present_treatments": "לא מקבל טיפול תרופתי.",
                    "treatment_expectations": "רוצה להבין מה עובר עליו.",
                    "objective_patient_description": "",
                    "reports_from_other_systems": "",
                    "questionnaire_results": "",
                    "holocaust_survivor_status": "",
                    "violence_abuse_screening_details": "",
                    "rights_utilization_mapping": "",
                    "medical_poa_guardianship_status": "",
                    "other_objective_information": "",
                    "functional_assessment_details": "קושי בריכוז בלימודים.",
                    "problem_list_sw_impression": "קשיי ריכוז, תחושת תקיעות.",
                    "identified_resources": "פנה לטיפול באופן יזום.",
                    "inhibiting_factors": "",
                    "overall_assessment_summary": "",
                    "treatment_plan_details": "",
                    "additional_vital_information_for_plan": "",
                    "patient_family_guidance_plan": "",
                    "rights_accessibility_plan_details": "",
                    "follow_up_referral_mediation_plan": "",
                    "duty_to_report_plan": "",
                    "treatment_contract_registration_notes": "",
                    "no_further_intervention_justification": "",
                    "summary_bps_assessment_brief": "",
                    "summary_treatment_goals_brief": "",
                    "summary_intervention_plan_recommendations": "",
                    "ai_recommondation": "יתכן שכדאי לבחון גורמים אפשריים לקשיי הריכוז, כגון עומס לימודי או גורמים רגשיים."
                }, ensure_ascii=False)),
            ],
        ),
        # Original simple example (can be kept or removed if the above are sufficient)
        # genai_types.Content(
        #     role="user",
        #     parts=[genai_types.Part.from_text(text="ידידיה בן 40 חולה")],
        # ),
        # genai_types.Content(
        #     role="model",
        #     parts=[
        #         genai_types.Part.from_text(text=json.dumps({key: ("ידידיה" if key == "name" else "40" if key == "age" else "חולה" if key == "symptoms" else "") for key in all_template_keys}, ensure_ascii=False)),
        #     ],
        # ),
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text=user_input_text),
            ],
        ),
    ]

    # --- Enhanced System Prompt ---
    system_prompt_text = f"""
You are an expert AI assistant for emotional therapists. Your primary function is to meticulously analyze unstructured Hebrew text, which represents a therapist's notes from a patient session, and extract relevant information into a structured JSON object.

Key Instructions:
1.  **Input Text**: The user will provide session notes in Hebrew.
2.  **Output Format**: You MUST return a single, valid JSON object.
3.  **JSON Keys**: The keys in the JSON object MUST be in English, as specified in the examples and the comprehensive list of target fields. The complete list of possible English keys is: {', '.join(all_template_keys)}.
4.  **JSON Values**: The values associated with these keys should be in Hebrew, extracted or inferred from the input text.
5.  **Comprehensive Extraction**: Attempt to extract information for ALL the fields from the provided list.
6.  **Handling Missing Information**: If specific information for a field is not present in the input text, you MUST include the key in the JSON output with an empty string ("") as its value. DO NOT omit any key from the full list.
7.  **Accuracy and Conciseness**: Prioritize accuracy. Extract information as verbatim as possible. If summarization is needed for a field (e.g., `patient_story_details` from a long narrative), be concise yet comprehensive. For fields like `symptoms`, list them clearly.
8.  **`name` Field**: If a full name is provided, use it. If only a first name, use that. If a pseudonym is indicated (e.g., "שם בדוי"), include that indication.
9.  **`gender` Field**: Infer gender (זכר/נקבה) from names or context if possible. If not clear, leave as an empty string.
10. **`ai_recommondation` Field**: This field is for a brief, high-level, non-clinical observation, a potential area for future exploration, or a general summary statement based on the input. It should be very concise (1-2 sentences). If nothing seems appropriate, use an empty string. Avoid giving direct medical or therapeutic advice.
11. **Contextual Understanding**: Pay attention to the context to correctly assign information to fields like `bio_psycho_social_background` (e.g., family, work, social situation) vs. `significant_life_events` (e.g., specific crises, traumas, major changes).

Analyze the user's input carefully and populate the JSON with all specified keys.
"""

    generate_content_config_object = genai_types.GenerateContentConfig(
        temperature=0.25, # Slightly higher for Pro model, allows a bit more nuance but still factual
        # top_p=0.95, # Consider if needed
        # top_k=40,   # Consider if needed
        response_mime_type="application/json",
        system_instruction=[
            genai_types.Part.from_text(text=system_prompt_text),
        ],
    )

    full_response_text = ""
    processed_data = {key: "" for key in all_template_keys} # Initialize with all keys
    processed_data["error"] = ""
    processed_data["details"] = ""

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
            raise ValueError("התקבלה תגובה ריקה מ-Gemini API.")

        gemini_extracted_data = json.loads(full_response_text)

        for key in all_template_keys:
            if key in gemini_extracted_data:
                # Ensure value is string, especially for numbers like age
                processed_data[key] = str(gemini_extracted_data[key]) if gemini_extracted_data[key] is not None else ""
        
        # Explicitly ensure age is a string, even if it was an int in JSON
        if processed_data.get("age") is not None:
            processed_data["age"] = str(processed_data["age"])
        else:
             processed_data["age"] = ""


        return processed_data

    except json.JSONDecodeError as e:
        error_msg = f"שגיאת פיענוח JSON: {e}. תגובת Gemini: '{full_response_text}'"
        st.error(error_msg)
        processed_data["error"] = "כשל בפענוח JSON מ-Gemini"
        processed_data["details"] = error_msg
        # Ensure all keys are still present in the returned dict on error
        for key_to_ensure in all_template_keys:
            if key_to_ensure not in processed_data:
                processed_data[key_to_ensure] = ""
        return processed_data
    except ValueError as e:
        error_msg = f"שגיאת ערך: {e}. תגובת Gemini: '{full_response_text}'"
        st.error(error_msg)
        processed_data["error"] = "נתונים לא תקינים מ-Gemini (תגובה ריקה או ערך שגוי)"
        processed_data["details"] = error_msg
        for key_to_ensure in all_template_keys:
            if key_to_ensure not in processed_data:
                processed_data[key_to_ensure] = ""
        return processed_data
    except Exception as e:
        error_msg = f"שגיאה בקריאה ל-Gemini API: {type(e).__name__} - {e}. מודל: {model_name}."
        st.error(error_msg)
        if hasattr(e, 'response') and e.response:
            st.error(f"פרטי תגובת API: {e.response}")
        processed_data["error"] = "הקריאה ל-Gemini API נכשלה"
        processed_data["details"] = error_msg
        for key_to_ensure in all_template_keys:
            if key_to_ensure not in processed_data:
                processed_data[key_to_ensure] = ""
        return processed_data

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

    # --- Inject CSS for RTL text alignment ---
    st.markdown("""
        <style>
            /* Set base direction for the whole page */
            body {
                direction: rtl !important;
            }

            /* Apply text-align: right to common Streamlit elements and containers */
            .stApp,
            .stApp header, /* Streamlit's header bar */
            .main, /* Main content area */
            section[data-testid="st.main"], /* Another way to target main area */
            .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown li, /* Content from st.markdown */
            .stAlert, /* Covers st.error, st.warning, st.info, st.success */
            .stButton > button, /* Text inside st.button */
            .stDownloadButton > button, /* Text inside st.download_button */
            .stSpinner > div, /* Text inside st.spinner */
            .stTextInput > label, /* Label for text input */
            .stTextArea > label, /* Label for text area */
            h1, h2, h3, h4, h5, h6, p, div, span, label, li /* General HTML tags if not covered above */
            {
                text-align: right !important;
            }

            /* Ensure input fields themselves also align their internal text (placeholder, typed text) */
            .stTextInput input, 
            .stTextArea textarea {
                text-align: right !important;
                direction: rtl !important; /* Reinforce direction for typing */
            }
            
            /* Specific for title and subheader if they are not inheriting properly */
            h1[data-testid="stHeading"], h2[data-testid="stHeading"], h3[data-testid="stHeading"] {
                text-align: right !important;
            }

            /* For password input in check_password, ensure its label is also aligned */
            /* This might be covered by general label, but being specific can help */
            div[data-testid="stForm"] .stTextInput > label {
                 text-align: right !important;
            }

        </style>
    """, unsafe_allow_html=True)
    # --- End of CSS Injection ---

    # The st.markdown("<div dir='rtl' ...>") wrapper is no longer strictly necessary
    # around the whole main app if the CSS above is effective.
    # However, for components like st.json (which you've removed) or complex custom HTML,
    # explicit divs can still be useful. For now, relying on CSS.

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
