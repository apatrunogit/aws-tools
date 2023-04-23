import logging
import aws_session

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load AWS session
session = aws_session.load_session()

# Use the session to perform AWS operations
# ...

logger.info('Done!')
