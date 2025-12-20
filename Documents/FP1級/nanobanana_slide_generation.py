"""
Nano Banana を使って FP1級「FPの心構えと倫理」のスライドを生成するスクリプト
"""

import requests
import json
import time
from typing import List, Dict, Any

# Nano Banana API 設定
API_URL = "https://kamui-code.ai/t2i/fal/nano-banana-pro"
HEADERS = {
    "Content-Type": "application/json",
    "KAMUI-CODE-PASS": "kamui-pass-2025-7568"
}

class NanoBananaSlideGenerator:
    def __init__(self):
        self.slides_data = []

    def generate_slide_image(self, prompt: str, aspect_ratio: str = "16:9") -> Dict[str, Any]:
        """
        Nano Banana を使ってスライド画像を生成

        Args:
            prompt: 画像生成プロンプト
            aspect_ratio: アスペクト比 (16:9 for slides)

        Returns:
            API レスポンス
        """
        payload = {
            "prompt": prompt,
            "num_images": 1,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "sync_mode": True,
            "limit_generations": False
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error generating image: {e}")
            return {"error": str(e)}

    def generate_title_slide(self):
        """タイトルスライドを生成"""
        prompt = """
        Professional presentation slide title slide for "FP1級取得への道 第1回：FPの心構えと倫理"
        Financial Planner ethics professional development. Clean, modern design with blue and gold color scheme.
        Japanese text visible: "FPの心構えと倫理" and "信頼されるプロフェッショナルになるための必修科目".
        Minimalist design with finance/ethics iconography.
        """
        return self.generate_slide_image(prompt)

    def generate_ethics_principles_slide(self, principle: str, description: str):
        """倫理原則のスライドを生成"""
        prompt = f"""
        Professional presentation slide about Financial Planner ethics principle: "{principle}"
        Description: {description[:100]}...
        Clean corporate design with professional layout.
        Japanese and English text. Modern business presentation style.
        Include visual elements representing ethics and professionalism.
        """
        return self.generate_slide_image(prompt)

    def generate_case_study_slide(self, case_title: str, situation: str):
        """ケーススタディのスライドを生成"""
        prompt = f"""
        Professional business presentation slide showing a case study: {case_title}
        Financial Planner ethical dilemma scenario.
        Situation: {situation[:150]}...
        Clean design with question mark icon or ethics dilemma visual.
        Corporate training presentation style.
        """
        return self.generate_slide_image(prompt)

    def generate_summary_slide(self):
        """まとめスライドを生成"""
        prompt = """
        Professional presentation summary slide for Financial Planner ethics training.
        Key points: Customer first principle, Conflict of interest management,
        Legal compliance, Trust relationship building.
        Clean design with checkmarks or key takeaways visual.
        Modern corporate presentation style with Japanese and English text.
        """
        return self.generate_slide_image(prompt)

    def generate_all_slides(self):
        """すべてのスライドを生成"""
        slides_to_generate = [
            {
                "title": "タイトルスライド",
                "generator": self.generate_title_slide,
                "description": "FP1級取得への道 第1回：FPの心構えと倫理"
            },
            {
                "title": "顧客利益最優先の原則",
                "generator": self.generate_ethics_principles_slide,
                "args": ["顧客利益最優先の原則", "常に顧客の利益を第一に考え、行動する"],
                "description": "FP倫理綱領の第一原則"
            },
            {
                "title": "誠実性の原則",
                "generator": self.generate_ethics_principles_slide,
                "args": ["誠実性の原則", "公正、誠実、忠実に行動する"],
                "description": "FP倫理綱領の第二原則"
            },
            {
                "title": "利益相反管理",
                "generator": self.generate_ethics_principles_slide,
                "args": ["利益相反管理", "手数料体系の透明化と適切な対応"],
                "description": "利益相反の具体的な管理手法"
            },
            {
                "title": "ケーススタディ1",
                "generator": self.generate_case_study_slide,
                "args": ["手数料と顧客利益の衝突", "ノーロード投信が適切だが、手数料あり投信を推奨したい"],
                "description": "典型的な倫理的ジレンマ"
            },
            {
                "title": "ケーススタディ2",
                "generator": self.generate_case_study_slide,
                "args": ["情報漏洩のリスク", "顧客の機密情報を同僚から求められる"],
                "description": "守秘義務に関するケース"
            },
            {
                "title": "まとめ",
                "generator": self.generate_summary_slide,
                "description": "倫理はFPの生命線"
            }
        ]

        results = []

        for slide_info in slides_to_generate:
            print(f"\n生成中: {slide_info['title']}")

            if "args" in slide_info:
                result = slide_info["generator"](*slide_info["args"])
            else:
                result = slide_info["generator"]()

            slide_data = {
                "title": slide_info["title"],
                "description": slide_info["description"],
                "result": result
            }

            results.append(slide_data)

            # API 制限を避けるため少し待機
            time.sleep(2)

        return results

    def save_results(self, results: List[Dict[str, Any]], filename: str = "nanobanana_slides_result.json"):
        """結果を保存"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n結果を {filename} に保存しました")

# メイン実行
if __name__ == "__main__":
    generator = NanoBananaSlideGenerator()

    print("=== Nano Banana で FP1級スライドを生成します ===\n")

    # スライドを生成
    results = generator.generate_all_slides()

    # 結果を保存
    generator.save_results(results)

    # 画像URLを表示
    print("\n=== 生成された画像 URL ===")
    for i, slide in enumerate(results):
        print(f"\nスライド {i+1}: {slide['title']}")
        if "images" in slide["result"]:
            for j, img in enumerate(slide["result"]["images"]):
                print(f"  画像 {j+1}: {img.get('url', 'N/A')}")
        elif "error" in slide["result"]:
            print(f"  エラー: {slide['result']['error']}")