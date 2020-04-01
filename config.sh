#!/bin/bash

source venv/bin/activate
echo Virtual Environment Mode: ON

export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo Archivo Principal $FLASK_APP : Environment $FLASK_ENV : Mode $FLASK_DEBUG 
