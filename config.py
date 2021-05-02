from starlette.config import Config

config = Config(".env")

# LOGGING #
LOGGING_LEVEL: int = config(
    "LOGGING_LEVEL",
    default=20
)

# SUMMARISER CONFIGURATION #
## Model path
DEFAULT_MODEL_PATH: str = config(
    "DEFAULT_MODEL_PATH",
    default='microsoft/xprophetnet-large-wiki100-cased-xglue-ntg')
## GPU usage
GPU: bool = config("GPU", default=True)
## Batch size of the model
BATCH_SIZE: int = config("BATCH_size", default=8)
