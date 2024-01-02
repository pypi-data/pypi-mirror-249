import subprocess
from loguru import logger


def run_code_quality():
    # Run pytest
    result = subprocess.run(["pytest", "-v"], check=False)

    issues_found = False
    # Check if pytest passed
    if result.returncode == 5:
        logger.warning("No tests found!")
    elif result.returncode != 0:
        logger.critical("Tests failed!")
        issues_found = True

    # Run prospector
    result = subprocess.run(["prospector", "--ignore-paths", "test/"], check=False)
    if result.returncode != 0:
        logger.critical("Prospector found issues!")
        issues_found = True

    # Run black
    result = subprocess.run(["black", "--check", "."], check=False)
    if result.returncode != 0:
        logger.critical("Black found formatting issues!")
        issues_found = True

    return not issues_found
