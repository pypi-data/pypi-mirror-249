import random
import sys

from dotenv import load_dotenv

from .constants import OBJECT_TO_INSERT_CODE

load_dotenv()
from circles_local_database_python.connector import Connector  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)


class NumberGenerator:
    @staticmethod
    # TODO: Add new parameters to define new logic region: Region, entity_type: EntityType
    def get_random_number(schema: str, table: str, number_column_name: str = "`number`") -> int:
        logger.start()
        connector = Connector.connect(schema)
        cursor = connector.cursor()

        random_number = None

        for _ in range(100):  # Try 100 times to get a random number that does not already exist in the database
            random_number = random.randint(1, sys.maxsize)
            logger.info(object={"Random number generated": random_number})

            query_get = f"SELECT COUNT(*) FROM {schema}.{table} WHERE {number_column_name} = %s LIMIT 1"
            cursor.execute(query_get, (random_number, ))
            rows_count = cursor.fetchone()
            if rows_count[0] == 0:  # COUNT(*) = 0
                logger.info(f"Number {random_number} does not already exist in database")
                break
            else:
                logger.info(f"Number {random_number} already exists in database")

        logger.end(object={"random_number": random_number})
        return random_number
