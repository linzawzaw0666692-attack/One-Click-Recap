"""
translate.py
Function 2: Gemini API သုံးပြီး မြန်မာဘာသာပြန်ခြင်း
"""
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel("gemini-1.5-flash")


def translate_to_myanmar(text: str) -> str:
    """
    English (သို့) အခြားဘာသာစကား စာသားကို Recap Video အတွက်
    သဘာဝကျကျ၊ ပြောစကားဆန်တဲ့ မြန်မာစာအဖြစ် ဘာသာပြန်ပေးမယ်
    """
    prompt = f"""
အောက်ပါစာသားကို ရုပ်ရှင်/ဇာတ်လမ်း Recap ဗီဒီယိုတစ်ခုအတွက်
ပြောစကားဆန်ဆန်၊ သဘာဝကျကျ မြန်မာဘာသာသို့ ပြန်ဆိုပေးပါ။
ဘာသာပြန်ထားသောစာသားကိုသာ ပြန်ပေးပါ၊ အခြားရှင်းလင်းချက် မထည့်ပါနှင့်။

Original text:
{text}
"""
    response = _model.generate_content(prompt)
    return response.text.strip()


def translate_sentences(sentences: list) -> list:
    """
    sentence timestamp များကို ထိန်းထားပြီး တစ်ကြောင်းချင်း ဘာသာပြန်မယ်
    (subtitle timing လိုအပ်ရင် အသုံးဝင်သည်)
    """
    translated = []
    for s in sentences:
        my_text = translate_to_myanmar(s["text"])
        translated.append({
            "text": my_text,
            "start": s["start"],
            "end": s["end"],
        })
    return translated
