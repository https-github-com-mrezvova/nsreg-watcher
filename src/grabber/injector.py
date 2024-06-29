import os
import sys
from pathlib import Path

import django


def load_django_settings(path: Path) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    sys.path.append(str(path / "src" / "website"))
    django.setup()
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
