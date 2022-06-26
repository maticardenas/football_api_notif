from src.notifier_logger import get_logger
from src.utils.fixtures_utils import insert_head_to_heads

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Inserting head to head records...")
    insert_head_to_heads()
