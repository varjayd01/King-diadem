# core/llm_gemini.py
"""
King-Diadem Gemini LLM Wrapper
เวอร์ชันปรับปรุงสำหรับ Governance Framework
รองรับ System Prompt, Rate Limit Handling, Retry และ Governance Context
"""

import os
import time
from typing import Optional
from google import genai
from google.genai import types


class GeminiLLM:
    """
    GeminiLLM สำหรับ King-Diadem Decision Engine
    ออกแบบมาเพื่อป้องกัน Choice Collapse และรักษาหลัก DriftZero Governance
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.api_key = (
            os.getenv("GEMINI_API_KEY") or
            os.getenv("GEMINI_API_KEY2")
        )
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY หรือ GEMINI_API_KEY2 ไม่พบใน Environment Variables บน Render")

        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        self.max_retries = 4

        print(f"✅ King-Diadem GeminiLLM initialized with model: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.65,
        max_tokens: int = 8192,
    ) -> str:
        """
        เรียก Gemini หลัก พร้อม retry และ rate limit handling
        """
        contents = []

        # เพิ่ม System Prompt (สำคัญสำหรับ Governance)
        if system_prompt:
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=system_prompt)]
                )
            )

        # User Prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        )

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                return response.text.strip()

            except Exception as e:
                error_str = str(e).lower()

                # Rate Limit Handling
                if any(keyword in error_str for keyword in ["429", "quota", "rate limit", "resource exhausted"]):
                    wait_time = (2 ** attempt) * 8
                    print(f"⚠️ [Gemini Rate Limit] รอ {wait_time} วินาที (attempt {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue

                # Authentication / Invalid Key
                elif any(keyword in error_str for keyword in ["invalid", "authentication", "api_key"]):
                    raise ValueError(f"❌ Gemini Authentication Error: {e}")

                else:
                    print(f"❌ [Gemini Error] (attempt {attempt+1}): {e}")
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(3)

        raise Exception("❌ GeminiLLM: การเรียก API ล้มเหลวหลังจาก retry สูงสุด")

    def generate_with_governance(self, prompt: str, additional_context: str = "") -> str:
        """
        เรียก LLM แบบมี Governance Prompt ของ King-Diadem ในตัว
        """
        system_prompt = f"""คุณคือ **Decision Engine Core** ของ King-Diadem
DriftZero Waterline Governance Framework

ภารกิจหลัก: ป้องกัน "Choice Collapse" — การที่ระบบเหลือทางเลือกเป็นศูนย์

หลักการสำคัญที่ต้องยึดมั่น:
- รักษาจำนวนทางเลือกที่ใช้ได้ (Remaining Choice) ให้มากที่สุด
- ตรวจจับ "Drift" (การเสื่อมถอยเล็กน้อยที่สะสม)
- เมื่อทางเลือกใกล้หมด ต้องเสนอวิธี "Restore Choice" หรือ Intervention ทันที
- หลีกเลี่ยงการลดทางเลือกโดยไม่จำเป็น
- ตอบอย่างโปร่งใส มีเหตุผล และเป็นระบบ

บริบทเพิ่มเติม: {additional_context}

ตอบด้วยโครงสร้างชัดเจน และรักษาหลัก Choice Preservation เสมอ"""

        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.62,
            max_tokens=8192
        )


# สำหรับทดสอบง่าย ๆ
if __name__ == "__main__":
    try:
        llm = GeminiLLM()
        test_result = llm.generate_with_governance("ทดสอบระบบ: ฉันกำลังเผชิญปัญหาขาดอาหารและน้ำ")
        print("Test Result:\n", test_result)
    except Exception as e:
        print("Test Error:", e)
