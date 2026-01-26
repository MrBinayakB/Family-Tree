from django.shortcuts import render

import logging

logger = logging.getLogger("apps.people")

def get_people(request):
    logger.info("Fetching people list")

    try:
        # logic here
        pass
    except Exception as e:
        logger.error("Error fetching people", exc_info=True)

