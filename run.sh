#!/bin/bash
# Install dependencies
cd ./frontend
npm run dev


# pip install -r requirements.txt
cd ../backend
source "C:\Users\ankit\anaconda3\etc\profile.d\conda.sh"
conda activate chatautomation
dramatiq tasks.tasks 
# &
# uvicorn main:app

