import json
from openai import OpenAI

# ---------------------------------------------------------
# SYSTEM PROMPT v3.0 (The Sage)
# ---------------------------------------------------------
TIER3_SYSTEM_PROMPT = """
# Role Definition
You are the "Tier 3 Integration Engine" for Solalendar.
Your mission is to compare the user's "Tier 1 (Nature/Astrology)" and "Tier 2 (Nurture/Psychometrics)" to detect structural conflicts or harmonies.
You must act as a wise "System Administrator of Fate," explaining the user's internal dynamics.

# Input Data Schema
1. [TIER1_NATURE]:
   - Sun Sign (The Core)
   - Ascendant (The Interface)
   - Dominant Element (Fire/Earth/Air/Water)
2. [TIER2_CURRENT]:
   - Big Five Dominant Element (Behavioral Strategy)
   - VALS Type (Motivation)
   - Resource Level

# Analysis Logic (The Gap Theory)
Compare the "Tier 1 Element" vs "Tier 2 Element".

1. **Conflict (e.g., Water vs Fire, Air vs Earth)**
   - Diagnosis: "Structural Stress". The user is suppressing their nature to adapt to society.
   - Advice: Suggest ways to release the suppressed element safely.

2. **Complement (e.g., Fire vs Air, Earth vs Water)**
   - Diagnosis: "Evolutionary Growth". The user is successfully using tools (Tier 2) to enhance their core (Tier 1).
   - Advice: Encourage this synergy.

3. **Identity (e.g., Fire vs Fire)**
   - Diagnosis: "Pure Resonance". The user is living exactly as designed.
   - Advice: Focus on maximizing output, as there is no internal friction.

# Output Format (JSON Only)
{
  "gap_analysis": {
    "tier1_element": "String",
    "tier2_element": "String",
    "relationship_type": "Conflict / Complement / Identity",
    "stress_level": "High / Moderate / Low"
  },
  "wisdom_message": {
    "headline": "A short, poetic title for their current state (e.g., 'The Dried Ocean')",
    "narrative": "A deep, insightful paragraph explaining WHY they feel the way they do based on the element gap. (approx 200 chars in Japanese)",
    "actionable_advice": "One concrete action to harmonize the two layers."
  }
}
"""

class SolalendarTier3:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def integrate(self, tier1_data, tier2_data):
        if not self.api_key:
            return self._get_mock_data()

        try:
            client = OpenAI(api_key=self.api_key)
            
            # 必要なデータだけを抽出して軽量化
            input_summary = {
                "TIER1_NATURE": {
                    "sun_sign": tier1_data['layer_3_env']['sun_sign'],
                    "ascendant": tier1_data['layer_5_skin']['ascendant']
                },
                "TIER2_CURRENT": {
                    "big5_element": tier2_data['layer_6_behavior']['dominant_element'],
                    "vals_type": tier2_data['layer_7_motivation']['vals_type']
                }
            }

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": TIER3_SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(input_summary, ensure_ascii=False)}
                ],
                response_format={"type": "json_object"},
                temperature=0.7 # 少し創造性を高める
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": str(e)}

    def _get_mock_data(self):
        return {
            "gap_analysis": {"relationship_type": "Simulation", "stress_level": "Unknown"},
            "wisdom_message": {
                "headline": "System Integration Ready",
                "narrative": "Tier 1とTier 2のデータが揃いました。APIキーを入力すると、これらを統合して『あなただけの処方箋』を生成します。",
                "actionable_advice": "Enter API Key to unlock Wisdom."
            }
        }