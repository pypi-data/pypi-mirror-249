import subprocess
from swarms.telemetry.check_update import check_for_update


def auto_update():
    """auto update swarms"""
    try:
        if check_for_update():
            subprocess.run(["pip", "install", "--upgrade", "swarms"])
    except Exception as e:
        print(e)
