import os
import django


def init(app="web"):
    "初始化"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{app}.settings")
    django.setup()
