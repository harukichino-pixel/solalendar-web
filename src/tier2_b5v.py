# src/tier2_b5v.py

class SolalendarB5V:
    """
    Tier 2: The Dynamic Probe (Solalendar B5V)
    Managing Questions for BigFive (OS) and VALS (Drive).
    """
    
    def __init__(self):
        # BigFive簡易診断（各因子2問ずつ）
        self.bigfive_questions = {
            "Openness": [
                {"id": "O1", "text": "独創的で新しいアイデアが次々と浮かぶ方だ", "score": 1},
                {"id": "O2", "text": "抽象的な議論や哲学的な話は退屈だ", "score": -1}
            ],
            "Conscientiousness": [
                {"id": "C1", "text": "部屋や机の上はいつも整理整頓されている", "score": 1},
                {"id": "C2", "text": "約束の時間や締め切りに遅れることがよくある", "score": -1}
            ],
            "Extraversion": [
                {"id": "E1", "text": "初対面の人ともすぐに打ち解けられる", "score": 1},
                {"id": "E2", "text": "大人数のパーティーよりも、一人か少人数で過ごすのが好きだ", "score": -1}
            ],
            "Agreeableness": [
                {"id": "A1", "text": "他人の感情に敏感で、共感しやすい", "score": 1},
                {"id": "A2", "text": "自分の利益のためなら、他人と対立しても構わない", "score": -1}
            ],
            "Neuroticism": [
                {"id": "N1", "text": "些細なことでイライラしたり、落ち込んだりしやすい", "score": 1},
                {"id": "N2", "text": "プレッシャーがかかる状況でも、冷静でいられる", "score": -1}
            ]
        }

    def calculate_bigfive(self, answers):
        """回答（1-5）を受け取り、各因子のスコア（0-100）を算出する"""
        scores = {"Openness": 50, "Conscientiousness": 50, "Extraversion": 50, "Agreeableness": 50, "Neuroticism": 50}
        
        # answers = {"O1": 5, "O2": 2, ...}
        for factor, questions in self.bigfive_questions.items():
            raw_score = 0
            for q in questions:
                if q['id'] in answers:
                    val = answers[q['id']]
                    # 1(同意しない) ~ 5(同意する) を -2 ~ +2 に変換
                    norm_val = val - 3
                    # 反転項目の処理（scoreが-1の場合は値を反転）
                    if q['score'] == -1:
                        norm_val = -norm_val
                    raw_score += norm_val
            
            # スコアへの反映（簡易ロジック: ±4の範囲を±20点として加算）
            scores[factor] += raw_score * 5
            # 0-100の範囲に収める
            scores[factor] = max(0, min(100, scores[factor]))
            
        return scores

    def get_tier1_prediction(self, tier1_data):
        """Tier 1の星座データから、BigFiveの傾向を予測する（仮説生成）"""
        # ここでは簡易的に「エレメント」から予測を作成
        # 火(Fire): 外向性(E)高
        # 土(Earth): 誠実性(C)高
        # 風(Air): 開放性(O)高
        # 水(Water): 協調性(A)高 / 神経症傾向(N)高
        
        elem_map = {
            "Fire": ["Aries", "Leo", "Sagittarius"],
            "Earth": ["Taurus", "Virgo", "Capricorn"],
            "Air": ["Gemini", "Libra", "Aquarius"],
            "Water": ["Cancer", "Scorpio", "Pisces"]
        }
        
        sun_sign = tier1_data['raw_data']['western']['sun_sign']
        
        prediction = ""
        if sun_sign in elem_map['Fire']:
            prediction = f"あなたの太陽星座（{sun_sign}）は『情熱と行動（火）』の性質を持っています。本来は外向的でエネルギッシュなはずですが、現状はいかがですか？"
        elif sun_sign in elem_map['Earth']:
            prediction = f"あなたの太陽星座（{sun_sign}）は『感覚と物質（土）』の性質を持っています。本来は堅実で慎重なはずですが、現状はいかがですか？"
        elif sun_sign in elem_map['Air']:
            prediction = f"あなたの太陽星座（{sun_sign}）は『知性と論理（風）』の性質を持っています。本来は好奇心旺盛でドライなはずですが、現状はいかがですか？"
        elif sun_sign in elem_map['Water']:
            prediction = f"あなたの太陽星座（{sun_sign}）は『感情と融合（水）』の性質を持っています。本来は共感力が高く繊細なはずですが、現状はいかがですか？"
            
        return prediction