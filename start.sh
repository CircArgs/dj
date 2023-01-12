#!/bin/bash
jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --port=8001 --allow-root &
uvicorn dj.api.main:app --host 0.0.0.0 --port 8000 --reload