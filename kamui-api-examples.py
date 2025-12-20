"""
Kamui Code API 使用示例

此文件展示了如何使用 Kamui Code API 端点：
- t2i-kamui-fal-nano-banana-pro: 文本生成图像
- i2i-kamui-fal-nano-banana-pro-edit: 图像编辑

安装依赖：pip install requests
"""

import requests
import json
from typing import Optional, Dict, Any
from pathlib import Path

# 加载配置文件
with open("kamui-api-config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class KamuiAPI:
    def __init__(self):
        self.endpoints = config["endpoints"]
        self.headers = {"Content-Type": "application/json"}

    def generate_image(
        self,
        prompt: str,
        num_images: int = 1,
        aspect_ratio: str = "1:1",
        output_format: str = "webp",
        sync_mode: bool = False,
        limit_generations: bool = False
    ) -> Dict[Any, Any]:
        """
        使用文本生成图像

        Args:
            prompt: 描述要生成图像的文本提示
            num_images: 要生成的图像数量 (1-4)
            aspect_ratio: 图像宽高比 ("21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16")
            output_format: 输出格式 ("jpeg", "png", "webp")
            sync_mode: 是否同步运行
            limit_generations: 是否限制生成数量

        Returns:
            API 响应
        """
        endpoint = self.endpoints["t2i-kamui-fal-nano-banana-pro"]

        payload = {
            "prompt": prompt,
            "num_images": num_images,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "sync_mode": sync_mode,
            "limit_generations": limit_generations
        }

        # 合并头部信息
        headers = {**self.headers, **endpoint["headers"]}

        try:
            response = requests.post(
                endpoint["url"],
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def edit_image(
        self,
        prompt: str,
        image_url: str,
        image_url2: Optional[str] = None,
        num_images: int = 1,
        aspect_ratio: str = "auto",
        output_format: str = "webp",
        sync_mode: bool = False,
        limit_generations: bool = False
    ) -> Dict[Any, Any]:
        """
        编辑图像

        Args:
            prompt: 描述要进行的编辑的文本提示
            image_url: 要编辑的图像URL
            image_url2: 可选的第二张图像URL，用于复杂编辑
            num_images: 要生成的图像数量 (1-4)
            aspect_ratio: 图像宽高比 ("auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16")
            output_format: 输出格式 ("jpeg", "png", "webp")
            sync_mode: 是否同步运行
            limit_generations: 是否限制生成数量

        Returns:
            API 响应
        """
        endpoint = self.endpoints["i2i-kamui-fal-nano-banana-pro-edit"]

        payload = {
            "prompt": prompt,
            "image_url": image_url,
            "num_images": num_images,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "sync_mode": sync_mode,
            "limit_generations": limit_generations
        }

        if image_url2:
            payload["image_url2"] = image_url2

        # 合并头部信息
        headers = {**self.headers, **endpoint["headers"]}

        try:
            response = requests.post(
                endpoint["url"],
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# 使用示例
if __name__ == "__main__":
    # 初始化 API 客户端
    api = KamuiAPI()

    # 示例 1: 文本生成图像
    print("=== 文本生成图像示例 ===")
    t2i_result = api.generate_image(
        prompt="A beautiful sunset over mountains with a lake, anime style",
        num_images=2,
        aspect_ratio="16:9",
        output_format="png",
        sync_mode=True
    )
    print(json.dumps(t2i_result, indent=2, ensure_ascii=False))

    # 示例 2: 图像编辑
    print("\n=== 图像编辑示例 ===")
    # 注意：你需要提供一个有效的图像URL
    example_image_url = "https://example.com/your-image.jpg"

    i2i_result = api.edit_image(
        prompt="Add a rainbow in the sky, make it more colorful",
        image_url=example_image_url,
        num_images=1,
        aspect_ratio="auto",
        output_format="webp",
        sync_mode=True
    )
    print(json.dumps(i2i_result, indent=2, ensure_ascii=False))

    # 示例 3: 生成创意艺术
    print("\n=== 创意艺术生成示例 ===")
    art_result = api.generate_image(
        prompt="Cyberpunk city at night with neon lights, futuristic style",
        num_images=4,
        aspect_ratio="21:9",
        output_format="jpeg",
        sync_mode=False,
        limit_generations=True
    )
    print(json.dumps(art_result, indent=2, ensure_ascii=False))

    # 示例 4: 使用第二张图像进行复杂编辑
    print("\n=== 复杂图像编辑示例 ===")
    example_image_url2 = "https://example.com/your-second-image.jpg"

    complex_edit_result = api.edit_image(
        prompt="Combine the style of the second image with the content of the first, create a hybrid artwork",
        image_url=example_image_url,
        image_url2=example_image_url2,
        num_images=2,
        aspect_ratio="1:1",
        output_format="png",
        sync_mode=True
    )
    print(json.dumps(complex_edit_result, indent=2, ensure_ascii=False))