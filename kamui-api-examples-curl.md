# Kamui Code API 使用示例 - cURL 版本

此文档展示了如何使用 cURL 命令调用 Kamui Code API 端点。

## 设置

### 通用头部
```bash
HEADER='-H "Content-Type: application/json" -H "KAMUI-CODE-PASS: kamui-pass-2025-7568"'
```

### API 基础 URL
- Text-to-Image: `https://kamui-code.ai/t2i/fal/nano-banana-pro`
- Image-to-Image Edit: `https://kamui-code.ai/i2i/fal/nano-banana-pro/edit`

---

## 1. 文本生成图像 (Text-to-Image)

### 基础示例
```bash
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  $HEADER \
  -d '{
    "prompt": "A beautiful sunset over mountains with a lake, anime style",
    "num_images": 1,
    "aspect_ratio": "1:1",
    "output_format": "webp",
    "sync_mode": true,
    "limit_generations": false
  }'
```

### 生成多张图像
```bash
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  $HEADER \
  -d '{
    "prompt": "Cyberpunk city at night with neon lights, futuristic style",
    "num_images": 4,
    "aspect_ratio": "21:9",
    "output_format": "jpeg",
    "sync_mode": false,
    "limit_generations": true
  }'
```

### 不同宽高比
```bash
# 肖像 (9:16)
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  $HEADER \
  -d '{
    "prompt": "A warrior princess in fantasy armor, standing on a cliff edge",
    "num_images": 1,
    "aspect_ratio": "9:16",
    "output_format": "png",
    "sync_mode": true
  }'

# 宽屏 (21:9)
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  $HEADER \
  -d '{
    "prompt": "Epic landscape of fantasy world with castles and dragons",
    "num_images": 1,
    "aspect_ratio": "21:9",
    "output_format": "jpeg",
    "sync_mode": true
  }'
```

---

## 2. 图像编辑 (Image-to-Image)

### 基础编辑
```bash
# 将图像 URL 替换为你的实际图像 URL
curl -X POST "https://kamui-code.ai/i2i/fal/nano-banana-pro/edit" \
  $HEADER \
  -d '{
    "prompt": "Add a rainbow in the sky, make it more colorful",
    "image_url": "https://example.com/your-image.jpg",
    "num_images": 1,
    "aspect_ratio": "auto",
    "output_format": "webp",
    "sync_mode": true
  }'
```

### 风格迁移
```bash
curl -X POST "https://kamui-code.ai/i2i/fal/nano-banana-pro/edit" \
  $HEADER \
  -d '{
    "prompt": "Transform this photo into a watercolor painting style",
    "image_url": "https://example.com/your-photo.jpg",
    "num_images": 2,
    "aspect_ratio": "auto",
    "output_format": "png",
    "sync_mode": true
  }'
```

### 使用双图混合编辑
```bash
curl -X POST "https://kamui-code.ai/i2i/fal/nano-banana-pro/edit" \
  $HEADER \
  -d '{
    "prompt": "Combine the style of the second image with the content of the first, create a hybrid artwork",
    "image_url": "https://example.com/first-image.jpg",
    "image_url2": "https://example.com/second-image.jpg",
    "num_images": 2,
    "aspect_ratio": "1:1",
    "output_format": "png",
    "sync_mode": true
  }'
```

### 季节变换
```bash
curl -X POST "https://kamui-code.ai/i2i/fal/nano-banana-pro/edit" \
  $HEADER \
  -d '{
    "prompt": "Change summer scene to winter with snow and frost effects",
    "image_url": "https://example.com/summer-landscape.jpg",
    "num_images": 1,
    "aspect_ratio": "auto",
    "output_format": "webp",
    "sync_mode": true
  }'
```

---

## 3. 实用技巧

### 批量生成脚本
```bash
#!/bin/bash
# batch_generate.sh

HEADER='-H "Content-Type: application/json" -H "KAMUI-CODE-PASS: kamui-pass-2025-7568"'

prompts=(
    "A magical forest with glowing mushrooms"
    "Abstract geometric patterns"
    "Steampunk mechanical dragon"
    "Zen garden with koi pond"
    "Space station interior with view of Earth"
)

for prompt in "${prompts[@]}"; do
    echo "Generating: $prompt"
    curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
        $HEADER \
        -d "{
            \"prompt\": \"$prompt\",
            \"num_images\": 1,
            \"aspect_ratio\": \"1:1\",
            \"output_format\": \"webp\",
            \"sync_mode\": true
        }" \
        -o "output_${prompt// /_}.json"
    sleep 1
done
```

### 检查生成状态
```bash
# 对于异步请求 (sync_mode: false)，可以检查状态
curl -X POST "https://kamui-code.ai/t2i/fal/nano-banana-pro" \
  $HEADER \
  -d '{
    "prompt": "A complex detailed scene that might take time",
    "num_images": 4,
    "sync_mode": false
  }'

# 响应会包含 request_id，可以用来查询状态
```

---

## 4. 参数说明

### 共同参数
- `prompt`: 文本提示词
- `num_images`: 生成图像数量 (1-4)
- `output_format`: 输出格式 (jpeg, png, webp)
- `sync_mode`: 同步模式 (true/false)
- `limit_generations`: 限制生成数量 (true/false)

### aspect_ratio 选项
- Text-to-Image: "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"
- Image-to-Image: "auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"

### 图像编辑特有参数
- `image_url`: 要编辑的图像 URL
- `image_url2`: 第二张图像 URL（可选，用于复杂编辑）

---

## 5. 响应格式

### 同步模式响应示例
```json
{
  "images": [
    {
      "url": "https://example.com/generated-image-1.webp",
      "width": 1024,
      "height": 1024
    }
  ],
  "prompt": "A beautiful sunset",
  "generation_time": 2.3,
  "model": "nano-banana-pro"
}
```

### 异步模式响应示例
```json
{
  "request_id": "req_123456789",
  "status": "processing",
  "message": "Your request is being processed"
}
```

---

## 6. 注意事项

1. **认证**: 每个请求都需要包含正确的 `KAMUI-CODE-PASS` 头部
2. **图像 URL**: 图像 URL 必须是公开可访问的
3. **时间限制**: 复杂请求可能需要较长时间
4. **并发限制**: 避免同时发送过多请求
5. **错误处理**: 检查响应状态码，处理可能的错误

---

## 7. 常见错误

### 认证错误
```json
{
  "error": "Invalid authentication credentials"
}
```
**解决**: 检查 `KAMUI-CODE-PASS` 头部是否正确

### 参数错误
```json
{
  "error": "Invalid aspect_ratio value"
}
```
**解决**: 确保使用有效的 aspect_ratio 值

### 图像 URL 无效
```json
{
  "error": "Unable to access image URL"
}
```
**解决**: 确保 image_url 是有效的、公开可访问的图像 URL