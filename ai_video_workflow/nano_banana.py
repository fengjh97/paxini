"""
Nano Banana Pro 图像生成模块
使用 Google Gemini API 生成高质量图片，作为 SeedDance 2.0 视频生成的素材
"""
import os
import base64
import logging
from pathlib import Path

from google import genai
from google.genai import types

from config import (
    NANO_BANANA_API_KEY,
    NANO_BANANA_MODEL,
    IMAGE_OUTPUT_DIR,
)

logger = logging.getLogger(__name__)


def get_client():
    """获取 Gemini API 客户端"""
    if not NANO_BANANA_API_KEY:
        raise ValueError(
            "请设置环境变量 GOOGLE_API_KEY。"
            "访问 https://aistudio.google.com 获取 API Key"
        )
    return genai.Client(api_key=NANO_BANANA_API_KEY)


def generate_image(
    prompt: str,
    output_filename: str = "generated.png",
    style_reference: str | None = None,
    negative_prompt: str | None = None,
) -> str:
    """
    使用 Nano Banana Pro 生成图片

    Args:
        prompt: 图片描述提示词
        output_filename: 输出文件名
        style_reference: 风格参考图片路径 (可选)
        negative_prompt: 负面提示词 (可选)

    Returns:
        生成图片的保存路径
    """
    client = get_client()
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

    # 构建内容
    contents = []

    # 如果有风格参考图，先加载
    if style_reference and os.path.exists(style_reference):
        logger.info(f"使用风格参考图: {style_reference}")
        ref_image = Path(style_reference).read_bytes()
        contents.append(
            types.Part.from_bytes(data=ref_image, mime_type="image/png")
        )
        contents.append(f"请参考这张图片的风格，生成以下内容: {prompt}")
    else:
        full_prompt = prompt
        if negative_prompt:
            full_prompt += f"\n\n避免: {negative_prompt}"
        contents.append(full_prompt)

    logger.info(f"正在生成图片: {prompt[:80]}...")

    response = client.models.generate_content(
        model=NANO_BANANA_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # 提取并保存图片
    output_path = os.path.join(IMAGE_OUTPUT_DIR, output_filename)
    image_saved = False

    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            image_saved = True
            logger.info(f"图片已保存: {output_path}")
        elif part.text:
            logger.info(f"模型回复: {part.text}")

    if not image_saved:
        raise RuntimeError("未能从响应中提取图片数据")

    return output_path


def generate_batch_images(
    prompts: list[dict],
) -> list[str]:
    """
    批量生成图片

    Args:
        prompts: 提示词列表, 每个元素为 dict:
            {"prompt": "描述", "filename": "文件名.png"}

    Returns:
        生成的图片路径列表
    """
    results = []
    for i, item in enumerate(prompts):
        prompt = item["prompt"]
        filename = item.get("filename", f"batch_{i:03d}.png")
        style_ref = item.get("style_reference")
        negative = item.get("negative_prompt")

        logger.info(f"批量生成 [{i + 1}/{len(prompts)}]: {prompt[:50]}...")
        path = generate_image(
            prompt=prompt,
            output_filename=filename,
            style_reference=style_ref,
            negative_prompt=negative,
        )
        results.append(path)

    logger.info(f"批量生成完成, 共 {len(results)} 张图片")
    return results


def image_to_base64(image_path: str) -> str:
    """将图片转换为 base64 字符串 (供 SeedDance API 使用)"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
