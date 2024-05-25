#!/bin/bash
echo "--> Starting celery process"
celery -A apps.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
