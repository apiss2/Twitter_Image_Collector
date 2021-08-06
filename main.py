import logging
import sys

from app.controllers.webserver import start

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    start()
