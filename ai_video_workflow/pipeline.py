"""
AI 视频生成工作流主管道
Nano Banana Pro (图像生成) → SeedDance 2.0 (视频生成)

工作流程:
1. 用 Nano Banana Pro 生成高质量参考图片
2. 将图片传入 SeedDance 2.0 进行图生视频
3. 支持批量处理和多镜头叙事
"""
import argparse
import json
import logging
import os
import sys

from nano_banana import generate_image, generate_batch_images
from seedance import text_to_video, image_to_video
from config import LOG_LEVEL

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_single(
    image_prompt: str,
    video_prompt: str,
    output_name: str = "result",
    duration: int = 5,
    resolution: str = "1080p",
    style_reference: str | None = None,
) -> dict:
    """
    单条工作流: 生成一张图 → 转为一段视频

    Args:
        image_prompt: 图片生成的提示词
        video_prompt: 视频动作/效果描述
        output_name: 输出文件名前缀
        duration: 视频时长 (秒)
        resolution: 视频分辨率
        style_reference: 风格参考图路径

    Returns:
        包含图片路径和视频路径的字典
    """
    logger.info("=" * 60)
    logger.info("开始单条工作流")
    logger.info(f"图片提示: {image_prompt[:80]}")
    logger.info(f"视频提示: {video_prompt[:80]}")
    logger.info("=" * 60)

    # 第一步: 用 Nano Banana Pro 生成图片
    logger.info("[Step 1/2] 使用 Nano Banana Pro 生成图片...")
    image_path = generate_image(
        prompt=image_prompt,
        output_filename=f"{output_name}.png",
        style_reference=style_reference,
    )
    logger.info(f"图片生成完成: {image_path}")

    # 第二步: 用 SeedDance 2.0 将图片转为视频
    logger.info("[Step 2/2] 使用 SeedDance 2.0 生成视频...")
    video_path = image_to_video(
        image_path=image_path,
        prompt=video_prompt,
        output_filename=f"{output_name}.mp4",
        duration=duration,
        resolution=resolution,
    )
    logger.info(f"视频生成完成: {video_path}")

    result = {"image": image_path, "video": video_path}
    logger.info(f"单条工作流完成: {result}")
    return result


def run_multi_shot(
    shots: list[dict],
    project_name: str = "project",
    resolution: str = "1080p",
    style_reference: str | None = None,
) -> list[dict]:
    """
    多镜头叙事工作流: 生成多组图片 → 分别转为视频片段

    Args:
        shots: 镜头列表, 每个元素为:
            {
                "image_prompt": "图片描述",
                "video_prompt": "视频动作描述",
                "duration": 5  # 可选
            }
        project_name: 项目名称
        resolution: 视频分辨率
        style_reference: 统一的风格参考图路径

    Returns:
        每个镜头的结果列表
    """
    logger.info("=" * 60)
    logger.info(f"开始多镜头工作流: {project_name}")
    logger.info(f"共 {len(shots)} 个镜头")
    logger.info("=" * 60)

    results = []
    for i, shot in enumerate(shots):
        shot_name = f"{project_name}_shot{i + 1:02d}"
        logger.info(f"\n--- 镜头 {i + 1}/{len(shots)} ---")

        result = run_single(
            image_prompt=shot["image_prompt"],
            video_prompt=shot["video_prompt"],
            output_name=shot_name,
            duration=shot.get("duration", 5),
            resolution=resolution,
            style_reference=style_reference,
        )
        results.append(result)

    logger.info(f"\n多镜头工作流完成! 共生成 {len(results)} 个片段")
    return results


def run_text_only(
    prompt: str,
    output_name: str = "text_video",
    duration: int = 5,
    resolution: str = "1080p",
) -> str:
    """
    纯文生视频工作流 (不经过图片生成, 直接用 SeedDance 2.0)

    Args:
        prompt: 视频描述
        output_name: 输出文件名前缀
        duration: 视频时长
        resolution: 分辨率

    Returns:
        视频文件路径
    """
    logger.info("=" * 60)
    logger.info("开始纯文生视频工作流")
    logger.info(f"提示: {prompt[:80]}")
    logger.info("=" * 60)

    video_path = text_to_video(
        prompt=prompt,
        output_filename=f"{output_name}.mp4",
        duration=duration,
        resolution=resolution,
    )
    logger.info(f"视频生成完成: {video_path}")
    return video_path


def run_from_config(config_path: str) -> list[dict]:
    """
    从 JSON 配置文件运行工作流

    JSON 格式示例:
    {
        "project_name": "my_project",
        "resolution": "1080p",
        "style_reference": null,
        "shots": [
            {
                "image_prompt": "一个穿着和服的女孩站在樱花树下",
                "video_prompt": "女孩缓缓转头微笑，樱花花瓣飘落",
                "duration": 5
            },
            {
                "image_prompt": "同一个女孩走在京都的小巷中",
                "video_prompt": "女孩慢步前行，阳光透过巷子投下光影",
                "duration": 8
            }
        ]
    }
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return run_multi_shot(
        shots=config["shots"],
        project_name=config.get("project_name", "project"),
        resolution=config.get("resolution", "1080p"),
        style_reference=config.get("style_reference"),
    )


def main():
    parser = argparse.ArgumentParser(
        description="AI 视频生成工作流: Nano Banana Pro + SeedDance 2.0"
    )
    subparsers = parser.add_subparsers(dest="command", help="工作流模式")

    # 单条工作流
    single_parser = subparsers.add_parser("single", help="单条: 图片 → 视频")
    single_parser.add_argument("--image-prompt", required=True, help="图片提示词")
    single_parser.add_argument("--video-prompt", required=True, help="视频提示词")
    single_parser.add_argument("--output", default="result", help="输出文件名前缀")
    single_parser.add_argument("--duration", type=int, default=5, help="视频时长(秒)")
    single_parser.add_argument("--resolution", default="1080p", help="分辨率")
    single_parser.add_argument("--style-ref", default=None, help="风格参考图路径")

    # 纯文生视频
    text_parser = subparsers.add_parser("text", help="纯文生视频")
    text_parser.add_argument("--prompt", required=True, help="视频提示词")
    text_parser.add_argument("--output", default="text_video", help="输出文件名前缀")
    text_parser.add_argument("--duration", type=int, default=5, help="视频时长(秒)")
    text_parser.add_argument("--resolution", default="1080p", help="分辨率")

    # 多镜头 (从配置文件)
    multi_parser = subparsers.add_parser("multi", help="多镜头叙事 (JSON配置)")
    multi_parser.add_argument("--config", required=True, help="JSON 配置文件路径")

    args = parser.parse_args()

    if args.command == "single":
        run_single(
            image_prompt=args.image_prompt,
            video_prompt=args.video_prompt,
            output_name=args.output,
            duration=args.duration,
            resolution=args.resolution,
            style_reference=args.style_ref,
        )
    elif args.command == "text":
        run_text_only(
            prompt=args.prompt,
            output_name=args.output,
            duration=args.duration,
            resolution=args.resolution,
        )
    elif args.command == "multi":
        run_from_config(args.config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
