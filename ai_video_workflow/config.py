"""
AI Video Workflow 配置文件
Nano Banana Pro (图像生成) + SeedDance 2.0 (视频生成)
"""
import os

# ============================================================
# Nano Banana Pro (Gemini 3 Pro Image) 配置
# ============================================================
# 注意: gemini-3-pro-image-preview 将于 2026-03-09 停用
# 建议迁移到 gemini-3.1-flash-image-preview (Nano Banana 2)
NANO_BANANA_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
NANO_BANANA_MODEL = os.environ.get(
    "NANO_BANANA_MODEL", "gemini-3.1-flash-image-preview"
)

# 图片输出设置
IMAGE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "images")
IMAGE_DEFAULT_RESOLUTION = "1024x1024"  # 可选: 1024x1024, 2048x2048, 4096x4096

# ============================================================
# SeedDance 2.0 (ModelsLab) 配置
# ============================================================
MODELSLAB_API_KEY = os.environ.get("MODELSLAB_API_KEY", "")
MODELSLAB_BASE_URL = "https://modelslab.com/api/v6/video"

# SeedDance 模型 ID
SEEDANCE_T2V_MODEL = "seedance-t2v"  # 文生视频
SEEDANCE_I2V_MODEL = "seedance-i2v"  # 图生视频

# 视频输出设置
VIDEO_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "videos")
VIDEO_DEFAULT_RESOLUTION = "1080p"
VIDEO_DEFAULT_DURATION = 5  # 秒 (最大 20 秒)
VIDEO_DEFAULT_FPS = 24

# ============================================================
# 工作流设置
# ============================================================
# 轮询间隔 (秒) - 等待视频生成完成
POLL_INTERVAL = 10
MAX_POLL_ATTEMPTS = 60  # 最大轮询次数

# 日志
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
