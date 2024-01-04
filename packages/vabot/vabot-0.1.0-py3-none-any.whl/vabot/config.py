import os
from pathlib import Path
from os.path import join
from dotenv import load_dotenv

load_dotenv(join(Path(__file__).resolve().parent.parent.parent, ".env"))

class BaseConfig(object):
    API_KEY= os.environ.get("API_KEY")
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ORGANIZATION_ID= os.environ.get("ORGANIZATION_ID")
    TELEGRAM_API_KEY= os.environ.get("TELEGRAM_BOT_API_KEY")

    # SSL Configuration
    CERT_PEM = join(BASE_DIR, "cert.pem")
    KEY_PEM  = join(BASE_DIR, "key.pem")


