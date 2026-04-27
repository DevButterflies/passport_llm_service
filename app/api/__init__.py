import os
from pathlib import Path
from dotenv import load_dotenv
from app.core.llm_client import ThreadManager

# 1. Get the current file path (root/app/api/__init__.py)
current_file = Path(__file__).resolve()

project_root = current_file.parent.parent.parent

# 3. Define the path to your .env file
env_path = project_root / "api_keys.env"


print(f"Looking for .env at: {env_path}")
if not env_path.exists():
    print("❌ ERROR: api_keys.env NOT found at this path!")
else:
    print("✅ Found api_keys.env, loading now...")

# 4. Load the environment variables
load_dotenv(dotenv_path=env_path)

# Update MODEL_PATH as well (assuming assets is in root/assets)
MODEL_PATH = project_root / "assets" / "best.onnx"

# CONFIGS
CONFIGS_MAIN = [
    {"name": f"gemini-worker-{i}", "model": "gemini-3.1-flash-lite-preview", "api_key": os.getenv(f"GOOGLE_API_KEY_{i}") }
    for i in range(1, 5)
]

CONFIGS_LIGHT = [
    {"name": f"gemini-worker-{i}", "model": "gemini-2.5-flash-lite", "api_key": os.getenv(f"GOOGLE_API_KEY_{i}") }
    for i in range(1, 5)
]

llm = ThreadManager(model1_configs=CONFIGS_MAIN, model2_configs=CONFIGS_LIGHT)