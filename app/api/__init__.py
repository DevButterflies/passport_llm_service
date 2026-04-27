from app.core.llm_client import ThreadManager
from dotenv import load_dotenv
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent  

env_path = parent_dir / "api_keys.env"
MODEL_PATH = parent_dir / "assets" / "best.onnx"
print(f"Loading environment variables from: {env_path}")
load_dotenv(dotenv_path=env_path)
#gemini-2.5-flash-lite
CONFIGS_MAIN = [
    {"name": f"gemini-worker-{i}", "model": "gemini-3.1-flash-lite-preview", "api_key": "AIzaSyCLHTFUNi6O1MMxn6n3jYs1JHbqVvdaOcA"}
    for i in range(1, 5)
]

CONFIGS_LIGHT = [
    {"name": f"gemini-worker-{i}", "model": "gemini-2.5-flash-lite", "api_key": "AIzaSyCLHTFUNi6O1MMxn6n3jYs1JHbqVvdaOcA"}
    for i in range(1, 5)
]

llm = ThreadManager(model1_configs=CONFIGS_MAIN , model2_configs =CONFIGS_LIGHT )
