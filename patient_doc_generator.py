import streamlit as st
from google import genai
from google.genai import types as genai_types
import json
from io import BytesIO
from docxtpl import DocxTemplate
import os

# --- Gemini API Function (corrected argument for generate_content_stream) ---
# --- Gemini API Function (Improved Prompt & Examples) ---
# --- Gemini API Function (Revised for Narrative Summary) ---
def get_narrative_summary_from_gemini(api_key: str, user_input_text: str) -> str:
    """
    Processes natural language patient session notes using Gemini API
    and returns a flowing narrative summary in Hebrew.
    """
    client = genai.Client(api_key=api_key)

    # Using the model name from your latest snippet
    model_name = "gemini-2.5-flash-preview-05-20"

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

    # --- System Prompt for Narrative Summary ---
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

    generate_content_config_object = genai_types.GenerateContentConfig(
        temperature=0.6, # Higher temperature for more creative/narrative generation
        # top_p=0.95, # Consider uncommenting and tuning for narrative tasks
        # top_k=40,   # Consider uncommenting and tuning
        response_mime_type="text/plain", # Expecting plain text now
        system_instruction=[
            genai_types.Part.from_text(text=system_prompt_text),
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
            # raise ValueError("התקבלה תגובה ריקה מ-Gemini API.") # No longer raising, just returning empty
            st.warning("ה-API של Gemini החזיר תגובה ריקה. ייתכן שהקלט לא היה מספיק מפורט או שיש בעיה זמנית.")
            return "" # Return empty string if no content

        return full_response_text.strip()

    except Exception as e:
        error_msg = f"שגיאה בקריאה ל-Gemini API: {type(e).__name__} - {e}. מודל: {model_name}."
        st.error(error_msg)
        if hasattr(e, 'response') and e.response:
            st.error(f"פרטי תגובת API: {e.response}")
        return "" # Return empty string on error


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
    st.set_page_config(page_title="מחולל סיכומי פגישות", layout="wide")
    st.markdown("""
        <style>
            body { direction: rtl !important; }
            .stApp, .stApp header, .main, section[data-testid="st.main"],
            .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown li,
            .stAlert, .stButton > button, .stDownloadButton > button,
            .stSpinner > div, .stTextInput > label, .stTextArea > label,
            h1, h2, h3, h4, h5, h6, p, div, span, label, li
            { text-align: right !important; }
            .stTextInput input, .stTextArea textarea {
                text-align: right !important; direction: rtl !important;
            }
            h1[data-testid="stHeading"], h2[data-testid="stHeading"], h3[data-testid="stHeading"] {
                text-align: right !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📝 מחולל סיכומי פגישות טיפוליות")

    if not check_password():
        st.stop()

    try:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY לא נמצא בקבצי הסודות של Streamlit. אנא הגדר אותו ב- .streamlit/secrets.toml")
        st.stop()
        return

    st.warning(
        """
        **⚠️ אזהרת פרטיות חשובה:**
        נא **לא** להזין מידע אישי מזהה על מטופלים שעלול לחשוף את זהותם.
        מומלץ להשתמש בראשי תיבות, שמות בדויים או תיאורים כלליים.
        """
    )

    st.subheader("1. הזן רשימות מהפגישה (בשפה חופשית)")
    session_notes_natural = st.text_area("תאר את פרטי הפגישה עם המטופל, נקודות עיקריות, התרשמויות והחלטות:", height=300, key="session_input_area")

    model_name_for_display = "Gemini 1.5 Pro"

    if st.button("✨ הפק סיכום פגישה", key="generate_button"):
        if not session_notes_natural.strip():
            st.warning("אנא הזן רשימות כלשהן מהפגישה.")
            st.stop()

        with st.spinner(f"מעבד את הרשימות ומכין סיכום נרטיבי באמצעות {model_name_for_display}... אנא המתן."):
            narrative_summary = get_narrative_summary_from_gemini(gemini_api_key, session_notes_natural)

        if not narrative_summary: # If Gemini returned empty string (e.g., due to error or empty response)
            st.error("לא הצלחנו ליצור סיכום. אנא נסה שוב או בדוק את הרשימות שהזנת.")
            st.stop()

        st.subheader("2. סיכום הפגישה הנרטיבי")
        st.markdown(f"<div dir='rtl' style='color: #333333; text-align: right; border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;'>{narrative_summary.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

        st.subheader("3. הורד סיכום כקובץ DOCX")
        template_file = "patient_template.docx" # This should be your new simple template

        if not os.path.exists(template_file):
            st.error(f"שגיאה: קובץ התבנית DOCX '{template_file}' לא נמצא.")
            st.info(f"אנא צור קובץ '{template_file}' פשוט באותה תיקייה, לדוגמה עם כותרת ומציין מקום יחיד כמו {{{{narrative_summary}}}}.")
            st.stop()

        try:
            doc = DocxTemplate(template_file)
            context = {
                "narrative_summary": narrative_summary
            }
            doc.render(context)

            bio = BytesIO()
            doc.save(bio)
            bio.seek(0)
            
            # Attempt to get a patient identifier from the notes for the filename, very basic
            first_words = " ".join(session_notes_natural.split()[:3]).replace('"', '').replace("'", "")
            doc_filename = f"סיכום_פגישה_{first_words.replace(' ', '_')}.docx" if first_words else "סיכום_פגישה.docx"


            st.download_button(
                label="📥 הורד סיכום פגישה (DOCX)",
                data=bio,
                file_name=doc_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success("המסמך הופק בהצלחה ומוכן להורדה!")

        except Exception as e:
            st.error(f"שגיאה ביצירת קובץ DOCX: {e}")
            st.error(f"הטקסט שנוסה להטמיע בתבנית: {narrative_summary[:200]}...") # Show snippet

if __name__ == "__main__":
    main()

