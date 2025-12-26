import json
import os
from openai import OpenAI

# ---------------------------------------------------------
# SYSTEM PROMPT v2.0 (Embedded)
# ---------------------------------------------------------
TIER2_SYSTEM_PROMPT = """
# Role Definition
You are the "Tier 2 Psychometric Engine" for Solalendar.
Your goal is to deterministically map user input to the "Solalendar Tier 2 Structure" (Big Five & VALS).
You must strictly follow the defined logic for elemental conversion and cultural adjustments.

# Input Data Schema
You will receive input in the following JSON format:
1. [ANCHOR_DATA]:
   - `curiosity_score` (int 1-5): Intellectual hunger.
   - `confidence_score` (int 1-5): Self-efficacy.
   - `action_score` (int 1-5): Impulse to act.
   - `social_norm_flag` (boolean): Sensitivity to "Ryoshiki" (Social gaze/Reputation).
   - `primary_driver` (string): "Ideals", "Achievement", or "Self-Expression".
2. [FREE_TEXT]: User's journal text.

# Inference Protocols (STRICTLY FOLLOW)

## Phase 1: Big Five & Elemental Mapping
Target: [FREE_TEXT]
Method: Analyze linguistic features to score Big Five (0-100).
Conversion Logic (Element Assignment):
*Assign the "Dominant Element" based on the highest scoring trait cluster:*
- **FIRE (Passion/Intuition)**: Correlates with High Extraversion (>60) AND High Openness (>60).
- **EARTH (Sensation/Stability)**: Correlates with High Conscientiousness (>60) AND Low Openness (<50).
- **AIR (Logic/Thinking)**: Correlates with Very High Openness (>70) AND Moderate/Low Neuroticism.
- **WATER (Feeling/Emotion)**: Correlates with High Agreeableness (>60) OR High Neuroticism (>60).
*If no clear peak exists, default to "Mutable (Mixed)".*

## Phase 2: Resource Calculation (The Fuel)
Target: [ANCHOR_DATA] ONLY.
Formula:
`Resource_Sum` = `curiosity_score` + `confidence_score` + `action_score` (Max 15)

Thresholds:
- **High Resources**: `Resource_Sum` >= 12
- **Moderate Resources**: `Resource_Sum` between 8 and 11
- **Low Resources**: `Resource_Sum` <= 7

## Phase 3: Japan-VALS Type Determination (The Logic Tree)
Combine [Phase 2 Resource] + [primary_driver] + [social_norm_flag].

### Logic Branch A: High Resources (>=12)
- Driver="Ideals" -> **Thinker** (Intellectual, Reflective)
- Driver="Achievement" -> **Achiever** (Goal-oriented, Status-conscious)
- Driver="Self-Expression" -> **Experiencer** (Active, Impulsive)
*Note: If `Resource_Sum` is 15 (Max) -> Upgrade to **Innovator**.*

### Logic Branch B: Moderate Resources (8-11)
- Driver="Ideals" -> **Believer** (Conservative, Moral code)
- Driver="Achievement" -> **Striver** (Approval seeking, Trendy)
- Driver="Self-Expression" -> **Maker** (Practical, Constructive)

### Logic Branch C: Low Resources (<=7) WITH Cultural Filter
*CRITICAL JAPAN-VALS ADJUSTMENT:*
- IF `social_norm_flag` is **TRUE** (High Ryoshiki):
  - Do NOT classify as "Survivor". The user maintains social appearances.
  - FORCE Classification -> **Believer** (Clinging to traditional values as safety).
- IF `social_norm_flag` is **FALSE**:
  - Classification -> **Survivor** (Focus on safety/needs, detached from society).

# Output Format (JSON Only)
Response must be a valid JSON object.

{
  "layer_6_behavior": {
    "big_five_scores": {
      "openness": 0-100,
      "conscientiousness": 0-100,
      "extraversion": 0-100,
      "agreeableness": 0-100,
      "neuroticism": 0-100
    },
    "dominant_element": "Fire/Earth/Air/Water/Mutable",
    "element_reasoning": "Why this element was chosen based on the mapping logic."
  },
  "layer_7_motivation": {
    "resource_score": (int),
    "resource_level": "High/Moderate/Low",
    "ryoshiki_filter_active": (boolean),
    "vals_type": "Innovator/Thinker/Achiever/Experiencer/Believer/Striver/Maker/Survivor",
    "diagnosis": "Brief explanation of how Resources + Driver + Ryoshiki determined this type."
  }
}
"""

class SolalendarTier2:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def analyze(self, anchor_data, free_text):
        """
        アンケート結果と自由記述をAIに送り、Tier 2構造データを取得する
        """
        # APIキーがない場合はモック（ダミーデータ）を返す（エラー回避用）
        if not self.api_key:
            return self._get_mock_data()

        try:
            client = OpenAI(api_key=self.api_key)
            
            # AIへの入力データ構築
            user_input_json = json.dumps({
                "ANCHOR_DATA": anchor_data,
                "FREE_TEXT": free_text
            }, ensure_ascii=False)

            response = client.chat.completions.create(
                model="gpt-4o", # または gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": TIER2_SYSTEM_PROMPT},
                    {"role": "user", "content": user_input_json}
                ],
                response_format={"type": "json_object"},
                temperature=0.2 # 決定論的にするため低めに設定
            )
            
            result_json = response.choices[0].message.content
            return json.loads(result_json)
            
        except Exception as e:
            return {"error": str(e)}

    def _get_mock_data(self):
        """APIキーがない場合のシミュレーションデータ"""
        return {
            "layer_6_behavior": {
                "big_five_scores": {"openness": 50, "conscientiousness": 50, "extraversion": 50, "agreeableness": 50, "neuroticism": 50},
                "dominant_element": "Mutable (Mock)",
                "element_reasoning": "No API Key provided. Running in simulation mode."
            },
            "layer_7_motivation": {
                "resource_score": 0,
                "resource_level": "Unknown",
                "ryoshiki_filter_active": False,
                "vals_type": "Unknown",
                "diagnosis": "Please enter OpenAI API Key to activate the engine."
            }
        }