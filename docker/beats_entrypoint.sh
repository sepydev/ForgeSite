#!/bin/bash
echo "--> Starting beats process"
celery -A apps.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
