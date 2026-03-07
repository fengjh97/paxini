"""
SeedDance 2.0 视频生成模块
通过 ModelsLab API 调用 ByteDance SeedDance 2.0 模型
支持 文生视频 (T2V) 和 图生视频 (I2V)
"""
import os
import time
import logging

import requests

from config import (
    MODELSLAB_API_KEY,
    MODELSLAB_BASE_URL,
    SEEDANCE_T2V_MODEL,
    SEEDANCE_I2V_MODEL,
    VIDEO_OUTPUT_DIR,
    VIDEO_DEFAULT_DURATION,
    VIDEO_DEFAULT_FPS,
    POLL_INTERVAL,
    MAX_POLL_ATTEMPTS,
)
from nano_banana import image_to_base64

logger = logging.getLogger(__name__)


def _get_headers():
    """获取 API 请求头"""
    if not MODELSLAB_API_KEY:
        raise ValueError(
            "请设置环境变量 MODELSLAB_API_KEY。"
            "访问 https://modelslab.com 注册获取 API Key"
        )
    return {
        "Content-Type": "application/json",
    }


def text_to_video(
    prompt: str,
    output_filename: str = "output.mp4",
    duration: int | None = None,
    resolution: str = "1080p",
    fps: int | None = None,
    negative_prompt: str | None = None,
) -> str:
    """
    文生视频 - 通过文字描述直接生成视频

    Args:
        prompt: 视频描述提示词
        output_filename: 输出文件名
        duration: 视频时长 (秒, 最大 20)
        resolution: 分辨率 (480p/720p/1080p)
        fps: 帧率
        negative_prompt: 负面提示词

    Returns:
        生成视频的保存路径
    """
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

    payload = {
        "key": MODELSLAB_API_KEY,
        "model_id": SEEDANCE_T2V_MODEL,
        "prompt": prompt,
        "negative_prompt": negative_prompt or "",
        "height": _resolution_to_height(resolution),
        "width": _resolution_to_width(resolution),
        "num_frames": (duration or VIDEO_DEFAULT_DURATION) * (fps or VIDEO_DEFAULT_FPS),
        "fps": fps or VIDEO_DEFAULT_FPS,
        "output_type": "mp4",
        "webhook": None,
        "track_id": None,
    }

    logger.info(f"正在生成文生视频: {prompt[:80]}...")

    response = requests.post(
        f"{MODELSLAB_BASE_URL}/text2video",
        json=payload,
        headers=_get_headers(),
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()

    return _handle_generation_result(result, output_filename)


def image_to_video(
    image_path: str,
    prompt: str,
    output_filename: str = "output.mp4",
    duration: int | None = None,
    resolution: str = "1080p",
    fps: int | None = None,
    end_image_path: str | None = None,
    negative_prompt: str | None = None,
) -> str:
    """
    图生视频 - 将 Nano Banana 生成的图片转为视频

    Args:
        image_path: 输入图片路径 (作为视频第一帧)
        prompt: 视频动作/效果描述
        output_filename: 输出文件名
        duration: 视频时长 (秒, 最大 20)
        resolution: 分辨率
        fps: 帧率
        end_image_path: 结束帧图片路径 (可选)
        negative_prompt: 负面提示词

    Returns:
        生成视频的保存路径
    """
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"输入图片不存在: {image_path}")

    # 将图片转为 base64
    init_image_b64 = image_to_base64(image_path)

    payload = {
        "key": MODELSLAB_API_KEY,
        "model_id": SEEDANCE_I2V_MODEL,
        "prompt": prompt,
        "negative_prompt": negative_prompt or "",
        "init_image": init_image_b64,
        "height": _resolution_to_height(resolution),
        "width": _resolution_to_width(resolution),
        "num_frames": (duration or VIDEO_DEFAULT_DURATION) * (fps or VIDEO_DEFAULT_FPS),
        "fps": fps or VIDEO_DEFAULT_FPS,
        "output_type": "mp4",
        "webhook": None,
        "track_id": None,
    }

    # 如果有结束帧图片
    if end_image_path and os.path.exists(end_image_path):
        payload["end_image"] = image_to_base64(end_image_path)

    logger.info(f"正在生成图生视频: {prompt[:80]}...")
    logger.info(f"输入图片: {image_path}")

    response = requests.post(
        f"{MODELSLAB_BASE_URL}/img2video",
        json=payload,
        headers=_get_headers(),
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()

    return _handle_generation_result(result, output_filename)


def _handle_generation_result(result: dict, output_filename: str) -> str:
    """处理生成结果 - 支持同步和异步返回"""
    status = result.get("status")

    if status == "success":
        # 同步完成
        video_url = result.get("output", [None])[0]
        if video_url:
            return _download_video(video_url, output_filename)

    elif status == "processing":
        # 异步处理, 需要轮询
        fetch_url = result.get("fetch_result")
        if not fetch_url:
            raise RuntimeError("API 返回 processing 状态但未提供轮询地址")
        logger.info("视频正在生成中, 开始轮询...")
        return _poll_for_result(fetch_url, output_filename)

    elif status == "error":
        error_msg = result.get("message", "未知错误")
        raise RuntimeError(f"视频生成失败: {error_msg}")

    raise RuntimeError(f"未知 API 响应状态: {status}, 响应: {result}")


def _poll_for_result(fetch_url: str, output_filename: str) -> str:
    """轮询等待视频生成完成"""
    for attempt in range(MAX_POLL_ATTEMPTS):
        time.sleep(POLL_INTERVAL)
        logger.info(f"轮询中... ({attempt + 1}/{MAX_POLL_ATTEMPTS})")

        response = requests.post(
            fetch_url,
            json={"key": MODELSLAB_API_KEY},
            headers=_get_headers(),
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        status = result.get("status")
        if status == "success":
            video_url = result.get("output", [None])[0]
            if video_url:
                return _download_video(video_url, output_filename)
        elif status == "error":
            raise RuntimeError(f"视频生成失败: {result.get('message')}")
        elif status == "processing":
            continue

    raise TimeoutError(
        f"视频生成超时, 已轮询 {MAX_POLL_ATTEMPTS} 次 "
        f"(共 {MAX_POLL_ATTEMPTS * POLL_INTERVAL} 秒)"
    )


def _download_video(url: str, output_filename: str) -> str:
    """下载生成的视频文件"""
    output_path = os.path.join(VIDEO_OUTPUT_DIR, output_filename)
    logger.info(f"正在下载视频: {url}")

    response = requests.get(url, timeout=120, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    logger.info(f"视频已保存: {output_path}")
    return output_path


def _resolution_to_height(resolution: str) -> int:
    """分辨率字符串转高度"""
    mapping = {"480p": 480, "720p": 720, "1080p": 1080}
    return mapping.get(resolution, 1080)


def _resolution_to_width(resolution: str) -> int:
    """分辨率字符串转宽度"""
    mapping = {"480p": 854, "720p": 1280, "1080p": 1920}
    return mapping.get(resolution, 1920)
