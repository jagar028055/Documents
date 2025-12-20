# Nano Banana で FP1級スライドを生成するプロンプト集

## 使用方法

以下のプロンプトを Nano Banana API または Web UI にコピー＆ペーストして、スライド画像を生成してください。

---

## 1. タイトルスライド

```
Professional presentation slide title slide for "FP1級取得への道 第1回：FPの心構えと倫理"
Financial Planner ethics professional development. Clean, modern design with blue and gold color scheme.
Japanese text visible: "FPの心構えと倫理" and "信頼されるプロフェッショナルになるための必修科目".
Minimalist design with finance/ethics iconography. Professional corporate training presentation style.
```

---

## 2. なぜ倫理が最初か？

```
Professional presentation slide explaining why ethics comes first in Financial Planner training.
Title: "倫理はFPの魂" (Ethics is the soul of FP).
Design includes imagery of trust, professional relationship between FP and client.
Clean layout with bullet points about FP being more than just money expert.
Modern corporate training aesthetic with blue professional color scheme.
```

---

## 3. FP倫理綱領 七つの原則

```
Professional presentation slide listing the seven principles of FP ethics in Japanese.
Title: "FP倫理綱領：七つの原則".
Clean numbered list design with icons for each principle:
1. 顧客利益最優先
2. 誠実性
3. 客観性
4. 公正性
5. 専門性
6. 秘密保持
7. 信頼性
Modern business presentation style with professional color scheme.
```

---

## 4. 顧客利益最優先の原則

```
Professional presentation slide about "Customer First Principle" in Financial Planning.
Title: "1. 顧客利益最優先の原則".
Include key points: Always prioritize customer interests, avoid conflicts of interest, provide suitable recommendations.
Visual elements showing balance scale favoring customer over profit.
Clean corporate design with professional layout. Japanese and English text.
```

---

## 5. 誠実性の原則

```
Professional presentation slide about "Integrity Principle" in Financial Planning.
Title: "2. 誠実性の原則".
Visual elements representing honesty, truthfulness, and ethical conduct.
Key points: No false statements, honest communication of capabilities, keeping promises.
Clean professional design with integrity symbols (handshake, shield, etc.).
```

---

## 6. 利益相反管理

```
Professional presentation slide about Conflict of Interest Management in Financial Planning.
Title: "利益相反管理：実践的な対応策".
Visual representation of balance scale or scales of justice.
Include key points: transparency, disclosure, multiple options, compliance framework.
Clean corporate design with professional business ethics imagery.
```

---

## 7. 典型的な利益相反ケース

```
Professional presentation slide showing typical conflict of interest cases in Financial Planning.
Title: "典型的な利益相反ケース".
Three-column layout showing: 1) Commission types, 2) Bank-affiliated FP position, 3) Incentive relationships.
Icons and visual elements for each case type.
Clean corporate training presentation design.
```

---

## 8. FP業務関連法令

```
Professional presentation slide about Financial Planning related laws and regulations.
Title: "FP業務関連法令".
Visual elements showing law books, scales of justice, legal symbols.
Four key laws listed with brief descriptions:
1. 金融商品取引法
2. 金融サービス提供法
3. 民法
4. 個人情報保護法
Professional legal education presentation style.
```

---

## 9. ケース1：手数料と顧客利益の衝突

```
Professional presentation slide showing an ethical dilemma case study.
Title: "ケース1：手数料と顧客利益の衝突".
Visual elements showing decision point or crossroads.
Situation: No-load fund is suitable but FP wants to recommend load fund for target.
Include red X for wrong behavior and green checkmark for correct approach.
Business ethics training presentation style.
```

---

## 10. ケース2：知識不足のケース

```
Professional presentation slide showing case study about knowledge limitations.
Title: "ケース2：知識不足のケース".
Visual elements showing consultant referring to specialist.
Situation: Complex inheritance tax consultation beyond FP's expertise.
Show correct approach: Referring to tax specialist.
Professional training presentation with clear moral lesson.
```

---

## 11. ケース3：情報漏洩のリスク

```
Professional presentation slide showing confidentiality case study.
Title: "ケース3：情報漏洩のリスク".
Visual elements showing locked files, privacy symbols, secure communication.
Situation: Colleague requests confidential client information.
Show correct approach: Declining to share confidential information.
Corporate compliance training presentation style.
```

---

## 12. FP1級試験の出題傾向

```
Professional presentation slide about FP1 exam question trends.
Title: "FP1級試験での出題傾向と対策".
Pie chart or bar graph showing question distribution:
- Ethics rule fill-in (30%)
- Case study violation identification (40%)
- Conflict management solutions (20%)
- Legal knowledge questions (10%)
Professional exam preparation presentation style.
```

---

## 13. 効率的な学習方法

```
Professional presentation slide about effective study methods.
Title: "効率的な学習方法".
Three-column layout with icons:
1. Memorize 7 principles completely
2. Practice case study questions
3. Organize related laws
Visual elements showing books, study materials, learning process.
Clean educational presentation design.
```

---

## 14. 信頼関係構築

```
Professional presentation slide about building trust with clients.
Title: "お客様との信頼関係構築".
Visual elements showing handshake, trusting relationship, professional consultation.
Two sections: Initial consultation and ongoing relationship maintenance.
Warm, professional design with imagery of client-FP relationship.
Corporate training presentation on relationship building.
```

---

## 15. まとめ

```
Professional presentation summary slide for Financial Planner ethics training.
Title: "まとめ：倫理はFPの生命線".
Key takeaways with checkmarks:
- Seven principles as foundation
- Always prioritize customer interests
- Proper conflict management and disclosure
- Understanding laws as professional duty
- Ethical action builds trust
Professional training presentation with summary visual elements.
```

---

## 16. 学習チェックリスト

```
Professional presentation slide with learning checklist.
Title: "学習チェックリスト".
Visual checklist design with checkboxes:
☐ Memorize all seven ethics principles
☐ Understand conflict cases and solutions
☐ Grasp key related laws
☐ Solve past 5 years of ethics questions
Interactive learning presentation style with clean checklist design.
```

---

## 17. 次回予告

```
Professional presentation slide for next session preview.
Title: "次回予告".
Subtitle: "【財務分析編】家計の見える化～キャッシュフロー表作成の極意～".
Visual elements showing financial charts, cash flow, household budget analysis.
Professional training presentation with forward-looking design.
```

---

## 18. ご清聴ありがとうございました

```
Professional presentation closing slide.
Title: "ご清聴ありがとうございました".
Subtitle: "ご質問はありますか？".
Clean, professional closing design with thank you message.
Corporate presentation closing slide with contact or Q&A prompt visual elements.
```

---

## API実行例（curl）

```bash
# 例：タイトルスライドを生成
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  -H "Content-Type: application/json" \
  -H "KAMUI-CODE-PASS: kamui-pass-2025-7568" \
  -d '{
    "prompt": "Professional presentation slide title slide for \"FP1級取得への道 第1回：FPの心構えと倫理\" Financial Planner ethics professional development. Clean, modern design with blue and gold color scheme.",
    "num_images": 1,
    "aspect_ratio": "16:9",
    "output_format": "png",
    "sync_mode": true
  }'
```

### パラメータ説明
- `prompt`: 上記のプロンプトテキスト
- `num_images`: 生成する画像数（通常は1）
- `aspect_ratio`: "16:9"（スライド用）
- `output_format`: "png"（高品質）
- `sync_mode`: true（同期的に生成）