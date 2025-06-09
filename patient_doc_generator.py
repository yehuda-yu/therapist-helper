import streamlit as st
from google import genai
from google.genai import types as genai_types
import json # Not directly used in the provided snippet, but often useful
from io import BytesIO
from docxtpl import DocxTemplate
import os
import datetime # For dynamic year in footer

# --- Gemini API Function (corrected argument for generate_content_stream) ---
# --- Gemini API Function (Improved Prompt & Examples) ---
# --- Gemini API Function (Revised for Narrative Summary - FIX APPLIED HERE) ---
def get_narrative_summary_from_gemini(api_key: str, user_input_text: str) -> str:
    """
    Processes natural language patient session notes using Gemini API
    and returns a flowing narrative summary in Hebrew.
    """
    # 1. Configure the API key globally for the genai module
    genai.configure(api_key=api_key) 

    model_name = "gemini-1.5-flash-preview-0514" 

    key_topics_to_cover = [
        "פרטי המטופל (גיל, מצב משפחתי, רקע רלוונטי)",
        "סיבת הפניה או נושא מרכזי של הפגישה",
        "תיאור המצב הנוכחי של המטופל (תסמינים, תחושות, תפקוד)",
        "מידע סובייקטיבי עיקרי (מה שהמטופל מדווח)",
        "מידע אובייקטיבי או תצפיות רלוונטיות (אם צוין)",
        "הערכה כללית של המצב (התרשמות)",
        "תכנית התערבות או המלצות עיקריות להמשך",
        "רקע ביו-פסיכו-סוציאלי רלוונטי (משפחה, עבודה, תמיכה)",
        "אירועים משמעותיים בעבר ובהווה",
        "ציפיות מהטיפול (אם צוין)"
    ]

    # --- Enhanced Few-Shot Examples for Narrative ---
    contents = [
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text="""מטופל, גבר כבן 80, אלמן, אב לשניים. מתמודד עם COPD, מונשם כרונית בבית מזה שנתיים. גר כעת בדירה שכורה מונגשת, אמור לעבור בקרוב חזרה לדירתו הקבועה בקומה 3 ללא מעלית. לאחרונה התגלה גידול בערמונית בבירור, הוא עוד לא יודע. הבת גרה קרוב ותומכת עיקרית, הבן השני רחוק ופחות מעורב. סיעודי, זקוק לעזרה מלאה בפעולות יומיום, מקבל עזרה ממטפל זר. המשפחה מיצתה זכויות בביטוח לאומי. מביע מצוקה רגשית גדולה מהניתוק מהסביבה המוכרת ובדידות בדירה השכורה. רוצה מאוד לחזור הביתה למרות הקושי בנגישות בגלל השכנים והקשר למקום. צריך זחליל ליציאה לבדיקות ומעקב רפואי, וגם לנפש ולאיכות חיים. על הבת עומס טיפולי ורגשי גדול כמתכללת הטיפול, מצריך התייחסות. המלצות: סיוע בהגשת בקשה לזחליל ממשרד הבריאות, מפגשי תמיכה והדרכה לבת אחת לחודש להקלה על העומס, מעקב רפואי גידול בערמונית, בחינת שירותים תומכים נוספים בקהילה. התכנית היא לשיפור איכות חייו, מענה לניידות ורווחה נפשית, ותמיכה במשפחה בדגש על הבת."""),
            ],
        ),
        genai_types.Content(
            role="model",
            parts=[
                genai_types.Part.from_text(text="""התקיים ביקור בית אצל מטופל בן 80, אלמן ואב לשניים, המתמודד עם מחלת COPD ומונשם כרונית בביתו מזה כשנתיים. המטופל מתגורר כעת בדירה שכורה מונגשת ועתיד לעבור בימים הקרובים חזרה לדירתו הקבועה בקומה שלישית ללא מעלית. לאחרונה התגלה אצלו גידול בערמונית הנמצא בבירור, מידע שטרם נמסר לו. בתו מתגוררת בסמיכות אליו ומהווה את התומכת העיקרית, בעוד בנו השני מתגורר במרחק ופחות מעורב בטיפול היומיומי. המטופל סיעודי וזקוק לעזרה בכל פעולות היומיום, עזרה המסופקת כיום על ידי מטפל זר. המשפחה מיצתה את זכויותיהם בביטוח לאומי.
המטופל מביע מצוקה רגשית ניכרת בשל הניתוק מסביבתו המוכרת והבדידות החברתית בדירה השכורה. קיים רצון עז מצדו לחזור לביתו הקבוע, למרות אתגרי הנגישות, בשל היכרותו את השכנים והקשר הרגשי למקום. זקוק למכשיר זחליל לצורך יציאה מהבית לבדיקות ומעקב רפואי, וגם כחלק חיוני משמירה על רווחתו הנפשית ואיכות חייו. על הבת מוטל עומס טיפולי ורגשי משמעותי כמתכללת הטיפול באביה, דבר המצריך התייחסות והתערבות תומכת.
המלצות ההתערבות כוללות: סיוע בהגשת בקשה למכשיר זחליל דרך משרד הבריאות, קביעת מפגשי תמיכה והדרכה לבת המטפלת אחת לחודש לצורך הקלה על העומס הטיפולי והרגשי, מעקב אחר התהליך הרפואי בנוגע לגידול בערמונית, ובחינת שירותים תומכים נוספים בקהילה. תכנית ההתערבות המוצעת מכוונת לשיפור איכות חייו של המטופל תוך מתן מענה לצרכי הניידות והרווחה הנפשית, ובמקביל תמיכה במערך המשפחתי, בדגש על הקלת העומס המוטל על הבת."""),
            ],
        ),
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text="""פגישה עם דנה, בת 32, רווקה. הגיעה עקב תחושות חרדה וקשיי הירדמות שהחמירו לאחר פרידה מבן זוג לפני חודשיים. מתארת דאגנות יתר לגבי העתיד, קושי להתרכז בעבודה (מנהלת חשבונות). בעבר חוותה אפיזודות דומות אך פחות אינטנסיביות. מצפה לקבל כלים לוויסות רגשי ולהפחית את החרדה. קופ"ח כללית. הפגישה התקיימה בזום."""),
            ],
        ),
        genai_types.Content(
            role="model",
            parts=[
                genai_types.Part.from_text(text="""דנה, רווקה בת 32, פנתה לטיפול בשל החמרה בתחושות חרדה וקשיי הירדמות, שהתעצמו בעקבות פרידה מבן זוגה לפני כחודשיים. היא מתארת דאגנות יתר לגבי העתיד וקושי בריכוז בעבודתה כמנהלת חשבונות. דנה מציינת כי חוותה בעבר אפיזודות דומות של חרדה, אך בעוצמה פחותה. ציפיותיה מהטיפול הן לרכוש כלים לוויסות רגשי ולהפחית את רמות החרדה. הפגישה התקיימה באמצעות זום, והיא חברה בקופת חולים כללית.
במהלך הפגישה, נראה כי דנה מודעת לקשייה ומביעה מוטיבציה לשינוי. ההתמקדות הראשונית תהיה בהבנת דפוסי החשיבה המעוררים חרדה ובחינת טכניקות הרגעה והתמודדות מיידיות. כמו כן, ייבחנו הגורמים התורמים לקשיי ההירדמות.
המלצות ראשוניות כוללות תרגול טכניקות נשימה והרפיה, וכן ניהול יומן מחשבות לזיהוי טריגרים לחרדה. בנוסף, נשקלת האפשרות להפניה להערכה פסיכיאטרית במידה והסימפטומים לא יראו שיפור או יחמירו, זאת בהתאם להתקדמות בטיפול."""),
            ],
        ),
        genai_types.Content(
            role="user",
            parts=[
                genai_types.Part.from_text(text=user_input_text),
            ],
        ),
    ]

    system_prompt_text = f"""
אתה עוזר AI מומחה לכתיבת סיכומי פגישות טיפוליות עבור מטפלים רגשיים.
המשימה שלך היא לקרוא את רשימות המטפל (שיינתנו בעברית) ולכתוב סיכום פגישה קוהרנטי ומקיף בעברית, בפסקאות רציפות.
הסיכום צריך להיות כתוב בשפה מקצועית אך קריאה, כאילו נכתב על ידי המטפל עצמו.

**מבנה ותוכן הסיכום:**
על הסיכום לשלב באופן טבעי מידע מהתחומים הבאים לפי הסדר שלהם, ככל שהוא מופיע ברשימות המטפל:
{', '.join(key_topics_to_cover)}

**סגנון הכתיבה:**
- כתוב בפסקאות רציפות, לא בנקודות או רשימות.
- שמור על זרימה לוגית בין חלקי הסיכום.
- השתמש בדוגמאות שניתנו לך כמודל לסגנון ולרמת הפירוט.
- אם מידע מסוים חסר ברשימות המטפל, אל תמציא אותו. התמקד במה שסופק.
- הימנע משימוש ישיר בכותרות סעיפים (כמו "S", "O", "A", "P") בתוך הטקסט הרציף.
- זכור כי המבנה של הטקסט שלך צריך לעקוב אחרי השלבים שצירפתי ולא בהכרח לפי הסדר שהמשתמש העלה 

**פלט:**
הפלט שלך צריך להיות טקסט אחד רציף בעברית, המהווה את סיכום הפגישה.

אנא עבד את הרשימות הבאות של המטפל וצור את סיכום הפגישה הנרטיבי:
"""
    
    generation_config = genai.types.GenerationConfig(
        temperature=0.6,
        response_mime_type="text/plain"
    )
    
    full_response_text = ""
    try:
        # 3. Instantiate GenerativeModel directly, passing system_instruction here
        model_instance = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt_text 
        )
        stream = model_instance.generate_content(
            contents=contents, # User and model examples, then current user input
            generation_config=generation_config,
            stream=True
        )

        for chunk in stream:
            if chunk.text:
                 full_response_text += chunk.text
        
        if not full_response_text.strip():
            st.warning("ה-API של Gemini החזיר תגובה ריקה. ייתכן שהקלט לא היה מספיק מפורט או שיש בעיה זמנית.")
            return "" 

        return full_response_text.strip()

    except Exception as e:
        error_msg = f"שגיאה בקריאה ל-Gemini API: {type(e).__name__} - {e}. מודל: {model_name}."
        st.error(error_msg)
        if hasattr(e, 'response') and e.response:
            st.error(f"פרטי תגובת API: {e.response}")
        return ""


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

    st.markdown("<div dir='rtl'>", unsafe_allow_html=True) 
    password_input = st.text_input("הזן סיסמה כדי לגשת לאפליקציה:", type="password", key="password_field")

    if st.button("התחבר", key="login_button"):
        if password_input == app_password:
            st.session_state.password_correct = True
            st.markdown("</div>", unsafe_allow_html=True) 
            st.rerun()
        else:
            st.error("הסיסמה שגויה.")
            st.session_state.password_correct = False
    st.markdown("</div>", unsafe_allow_html=True) 
    return False

# --- Main App ---
def main():
    st.set_page_config(
        page_title="מחולל סיכומי פגישות",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS מעוצב ומקצועי יותר
    st.markdown("""
        <style>
            /* כיוון RTL וגופנים */
            @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
            
            * {
                direction: rtl !important;
                font-family: 'Rubik', 'Arial Hebrew', Arial, sans-serif !important;
            }
            
            /* רקע ראשי */
            .stApp {
                background-color: #F4F6F8; /* אפור כחלחל בהיר מאוד */
                min-height: 100vh;
            }
            
            /* יישור לימין לכל האלמנטים */
            .stApp, .stApp header, .main, section[data-testid="st.main"],
            .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown li,
            /* .stAlert, */ /* ניתן להם טיפול ספציפי */
            .stButton > button, .stDownloadButton > button,
            .stSpinner > div, .stTextInput > label, .stTextArea > label,
            h1, h2, h3, h4, h5, h6, p, div, span, label, li {
                text-align: right !important;
            }
            
            /* כותרת ראשית (כללית של Streamlit, אם מופיעה) */
            h1[data-testid="stHeading"] {
                color: #2E3A4D; /* כחול כהה אפרפר */
                font-size: 2.6rem; 
                font-weight: 600;
                margin-bottom: 1.5rem;
                text-align: center !important;
                padding: 0.5rem;
            }
            
            /* כותרות משנה */
            h2[data-testid="stHeading"], h3[data-testid="stHeading"] {
                color: #3B4A61; /* כחול אפרפר בינוני */
                font-weight: 600;
                margin-top: 1.8rem;
                margin-bottom: 0.8rem;
                padding-right: 0.8rem;
                border-right: 3px solid #4A90E2; /* כחול נעים */
            }
            
            /* אזור הטקסט */
            .stTextArea > div > div > textarea {
                text-align: right !important;
                direction: rtl !important;
                font-size: 1rem; /* 16px */
                line-height: 1.7;
                border-radius: 8px; /* פחות עגול */
                border: 1px solid #D1D5DB; /* אפור בהיר */
                padding: 0.8rem 1rem;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); /* צל עדין */
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }
            
            .stTextArea > div > div > textarea:focus {
                border-color: #4A90E2; /* כחול נעים בפוקוס */
                box-shadow: 0 0 0 2.5px rgba(74, 144, 226, 0.25); /* אפקט פוקוס עדין */
            }
            
            /* כפתורים */
            .stButton > button, .stDownloadButton > button {
                background-color: #4A90E2; /* כחול נעים */
                color: white;
                border: none;
                border-radius: 8px; /* פחות עגול */
                padding: 0.65rem 1.6rem;
                font-size: 1rem;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(74, 144, 226, 0.2); /* צל עדין */
                transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
                margin: 0.8rem 0;
                width: auto;
                min-width: 180px;
            }
            
            .stButton > button:hover, .stDownloadButton > button:hover {
                background-color: #357ABD; /* כחול מעט כהה יותר */
                transform: translateY(-1px);
                box-shadow: 0 3px 6px rgba(74, 144, 226, 0.3);
            }

            /* כללי להתראות Streamlit */
            div[data-testid="stNotification"] {
                border-radius: 8px !important;
                padding: 1.1rem 1.3rem !important;
                margin: 1rem 0 !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
                border-right-width: 3px !important;
                border-right-style: solid !important;
                text-align: right !important; /* לוודא שהטקסט בפנים מיושר */
            }
            div[data-testid="stNotification"] [data-testid="stMarkdownContainer"] p {
                 text-align: right !important;
            }


            /* הודעת שגיאה (st.error) */
            div[data-testid="stNotification"][role="alert"] {
                background-color: #FEE2E2 !important; /* רקע אדום בהיר */
                border-right-color: #EF4444 !important; /* גבול אדום */
            }
            div[data-testid="stNotification"][role="alert"] div[data-testid="stMarkdownContainer"] p {
                color: #B91C1C !important; /* טקסט אדום כהה */
            }

            /* הודעת אזהרה (st.warning) */
            div[data-testid="stNotification"]:has(div[data-testid="stNotificationContentWarning"]) {
                background-color: #FEF3C7 !important; /* רקע צהוב בהיר */
                border-right-color: #F59E0B !important; /* גבול צהוב */
            }
            div[data-testid="stNotification"]:has(div[data-testid="stNotificationContentWarning"]) div[data-testid="stMarkdownContainer"] p {
                color: #92400E !important; /* טקסט צהוב כהה */
            }
            
            /* הודעת הצלחה (st.success) */
            div[data-testid="stNotification"]:has(div[data-testid="stNotificationContentSuccess"]) {
                background-color: #D1FAE5 !important; /* רקע ירוק בהיר */
                border-right-color: #10B981 !important; /* גבול ירוק */
            }
            div[data-testid="stNotification"]:has(div[data-testid="stNotificationContentSuccess"]) div[data-testid="stMarkdownContainer"] p {
                color: #065F46 !important; /* טקסט ירוק כהה */
            }

            /* אזהרת פרטיות מותאמת אישית */
            .privacy-warning-box {
                background-color: #FEF3C7; /* רקע צהוב בהיר */
                border-right: 3px solid #F59E0B; /* גבול צהוב */
                border-radius: 8px;
                padding: 1.1rem 1.3rem;
                margin: 1rem 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .privacy-warning-box h4, .privacy-warning-box p {
                color: #92400E !important; /* טקסט צהוב כהה */
            }
            
            /* ספינר */
            .stSpinner > div > div { /* התאמה לסלקטור של Streamlit */
                text-align: center !important;
                color: #4A90E2; /* כחול נעים */
                font-size: 1rem;
            }
            
            /* תיבת הסיכום */
            .summary-box {
                background: white;
                border-radius: 8px;
                padding: 1.5rem 2rem;
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* צל עדין ומורם */
                border: 1px solid #E5E7EB; /* אפור בהיר מאוד */
                line-height: 1.7;
                font-size: 1rem; /* 16px */
                position: relative;
                overflow: hidden;
            }
            
            .summary-box:before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 3px;
                height: 100%;
                background: #4A90E2; /* כחול נעים */
            }
            
            /* כרטיסיות שלבים */
            .step-card {
                background: white;
                border-radius: 8px;
                padding: 1rem 1.2rem;
                margin: 1rem 0;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
                border-right: 3px solid #4A90E2; /* כחול נעים */
            }
            .step-card h3 { /* כותרת בתוך כרטיסיית שלב */
                color: #2E3A4D; /* כחול כהה אפרפר */
                border-right: none !important; /* הסרת גבול כפול אפשרי */
                padding-right: 0 !important;
                margin-top: 0.3rem !important;
                margin-bottom: 0.3rem !important;
                font-size: 1.4rem; /* התאמת גודל */
            }
            
            /* מספור שלבים */
            .step-number {
                display: inline-block;
                width: 32px;
                height: 32px;
                background: #4A90E2; /* כחול נעים */
                color: white;
                border-radius: 50%;
                text-align: center !important; /* חשוב ליישור המספר */
                line-height: 32px;
                font-weight: bold;
                font-size: 0.85rem;
                margin-left: 10px; /* מרווח מהטקסט */
            }
            
            /* אייקונים */
            .icon { /* אייקון בכותרת הראשית */
                font-size: 2.2rem; /* התאמה לגודל הכותרת */
                margin-left: 10px;
                vertical-align: middle;
                color: #4A90E2; /* כחול נעים */
            }
            
            /* אנימציה לכניסה */
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(15px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .main > div { /* החלת האנימציה על האלמנטים הראשיים */
                animation: fadeIn 0.4s ease-out;
            }
            
            /* רספונסיב */
            @media (max-width: 768px) {
                /* הכותרת הראשית המותאמת אישית */
                 h1[style*="color: #2E3A4D"] { /* סלקטור לכותרת המותאמת */
                    font-size: 2rem !important;
                }
                h1[data-testid="stHeading"] { /* כותרת כללית של Streamlit */
                    font-size: 2rem;
                }
                
                .stButton > button, .stDownloadButton > button {
                    width: 100%;
                    margin: 0.5rem 0;
                    padding: 0.7rem 1rem;
                }
                .summary-box {
                    padding: 1rem 1.2rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # כותרת מותאמת אישית עם אייקון
    st.markdown("""
        <h1 style="text-align: center; color: #2E3A4D; font-size: 2.5rem; font-weight: 600; margin-bottom: 1.5rem;">
            <span class="icon">📝</span>
            מחולל סיכומי פגישות טיפוליות
        </h1>
    """, unsafe_allow_html=True)

    if not check_password():
        st.stop()

    try:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("⚠️ GEMINI_API_KEY לא נמצא בקבצי הסודות של Streamlit. אנא הגדר אותו ב- .streamlit/secrets.toml")
        st.stop()
        return

    # אזהרת פרטיות מעוצבת (משתמשת במחלקה .privacy-warning-box)
    st.markdown("""
        <div class="privacy-warning-box">
            <h4 style="color: #92400E; margin-bottom: 0.5rem; font-weight: 600;">
                ⚠️ אזהרת פרטיות חשובה
            </h4>
            <p style="margin: 0;">
                נא <strong>לא</strong> להזין מידע אישי מזהה על מטופלים שעלול לחשוף את זהותם.<br>
                מומלץ להשתמש בראשי תיבות, שמות בדויים או תיאורים כלליים.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # שלב 1 - הזנת רשימות
    st.markdown("""
        <div class="step-card">
            <h3>
                <span class="step-number">1</span>
                הזיני רשימות מהפגישה
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    session_notes_natural = st.text_area(
        "תארי את פרטי הפגישה, נקודות עיקריות, התרשמויות והחלטות:",
        height=280, # גובה מעט מוקטן
        key="session_input_area",
        placeholder="לדוגמה: פגישה עם א.ב., דיברנו על החרדות מהעבודה החדשה..."
    )

    model_name_for_display = "Gemini 1.5 Flash" # עדכון שם התצוגה של המודל

    col1, col2, col3, col4 = st.columns([0.5, 2, 2, 0.5]) # התאמת רוחב עמודות
    with col2:
        generate_clicked = st.button("✨ הפיקי סיכום פגישה", key="generate_button", use_container_width=True)
    with col3:
        if st.button("🔄 איפוס", key="reset_button", use_container_width=True):
            # Clear text area and any generated summary from session state if needed
            if "session_input_area" in st.session_state:
                st.session_state.session_input_area = ""
            # Potentially clear other relevant session state variables here
            st.rerun()
    
    if generate_clicked:
            if not session_notes_natural.strip():
                st.warning("⚠️ אנא הזיני רשימות כלשהן מהפגישה.")
                st.stop()

            with st.spinner(f"🔄 מעבד את הרשימות ומכין סיכום נרטיבי באמצעות {model_name_for_display}... אנא המתיני."):
                narrative_summary = get_narrative_summary_from_gemini(gemini_api_key, session_notes_natural)

            if not narrative_summary: # הודעת שגיאה כבר מוצגת מתוך הפונקציה אם יש בעיה עם ה-API
                if not any(msg.type == "error" for msg in st.session_state.get("streamlit_INTERNAL_messages", [])): # Check if an error was already shown
                     st.error("❌ לא הצלחנו ליצור סיכום. אנא נסי שוב או בדקי את הרשימות שהזנת.")
                st.stop()


            # שלב 2 - הצגת הסיכום
            st.markdown("""
                <div class="step-card" style="margin-top: 1.5rem;">
                    <h3>
                        <span class="step-number">2</span>
                        סיכום הפגישה הנרטיבי
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="summary-box">
                    {narrative_summary.replace('\n', '<br>')}
                </div>
            """, unsafe_allow_html=True)

            # שלב 3 - הורדת הקובץ
            st.markdown("""
                <div class="step-card" style="margin-top: 1.5rem;">
                    <h3>
                        <span class="step-number">3</span>
                        הורד סיכום כקובץ
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            template_file = "patient_template.docx"

            if not os.path.exists(template_file):
                st.error(f"❌ שגיאה: קובץ התבנית DOCX '{template_file}' לא נמצא.")
                st.info(f"💡 אנא צרי קובץ '{template_file}' פשוט באותה תיקייה, לדוגמה עם כותרת ומציין מקום יחיד כמו {{{{narrative_summary}}}}.")
                st.stop()

            try:
                doc = DocxTemplate(template_file)
                context = {
                    "narrative_summary": narrative_summary # Ensure this matches the placeholder in your docx
                }
                doc.render(context)

                bio = BytesIO()
                doc.save(bio)
                bio.seek(0)
                
                first_words = " ".join(session_notes_natural.split()[:3]).replace('"', '').replace("'", "")
                doc_filename = f"סיכום_פגישה_{first_words.replace(' ', '_')}.docx" if first_words else "סיכום_פגישה.docx"

                col_dl1, col_dl2, col_dl3, col_dl4 = st.columns([0.5, 2, 2, 0.5])
                with col_dl2:
                    st.download_button(
                        label="📥 הורידי סיכום פגישה (DOCX)",
                        data=bio,
                        file_name=doc_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                with col_dl3:
                    if st.button("🔄 התחילי מחדש", key="new_session_after_download", use_container_width=True):
                        if "session_input_area" in st.session_state:
                             st.session_state.session_input_area = ""
                        st.rerun()
                
                st.success("✅ המסמך הופק בהצלחה ומוכן להורדה!")

            except Exception as e:
                st.error(f"❌ שגיאה ביצירת קובץ DOCX: {e}")
                st.error(f"הטקסט שנוסה להטמיע בתבנית (תחילתו): {narrative_summary[:200]}...")
            
    current_year = datetime.date.today().year
    # פוטר עם פרטי קשר
    st.markdown(f"""
        <div style="margin-top: 3rem; padding: 1.5rem; text-align: center;">
            <p style="font-size: 1.1rem; color: #525F6C; margin-bottom: 1.5rem;">
                 פותח על ידי יהודה יונגשטיין עבור אנשי מקצוע בתחום הטיפול
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_foot1, col_foot_icons, col_foot3 = st.columns([2,1,2]) # Centering the icons a bit
    with col_foot_icons:
        subcol_icon1, subcol_icon2 = st.columns(2, gap="small")
        with subcol_icon1:
            image_url_mail = "https://img.icons8.com/fluency-systems-filled/48/new-post.png" # Alternative icon
            mail_url = "mailto:yehudayu@gmail.com"
            st.markdown(f"""
                <div style="text-align: center;">
                    <a href='{mail_url}' style="text-decoration: none;">
                        <img src='{image_url_mail}' width='40' height='40' style="transition: transform 0.2s ease; border-radius: 8px; opacity: 0.7; filter: grayscale(30%);"
                             onmouseover="this.style.opacity=1; this.style.transform='scale(1.1)'; this.style.filter='grayscale(0%)';"
                             onmouseout="this.style.opacity=0.7; this.style.transform='scale(1)'; this.style.filter='grayscale(30%)';">
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
        with subcol_icon2:
            image_url_linkedin = "https://img.icons8.com/fluency-systems-filled/48/linkedin.png" # Alternative icon
            linkedin_url = "https://www.linkedin.com/in/yehuda-yungstein/"
            st.markdown(f"""
                <div style="text-align: center;">
                    <a href='{linkedin_url}' target='_blank' style="text-decoration: none;">
                        <img src='{image_url_linkedin}' width='40' height='40' style="transition: transform 0.2s ease; border-radius: 8px; opacity: 0.7; filter: grayscale(30%);"
                             onmouseover="this.style.opacity=1; this.style.transform='scale(1.1)'; this.style.filter='grayscale(0%)';"
                             onmouseout="this.style.opacity=0.7; this.style.transform='scale(1)'; this.style.filter='grayscale(30%)';">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem; padding: 0.8rem;">
            <p style="font-size: 0.85rem; color: #8A94A0;">
                © {current_year} | נבנה עם Streamlit
            </p>
        </div>
    """, unsafe_allow_html=True)
   

if __name__ == "__main__":
    main()
