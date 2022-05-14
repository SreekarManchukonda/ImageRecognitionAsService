#!/bin/bash

cd /home/ec2-user/app_tier/compute_engine
python3 receive_message.py
cd /home/ec2-user/app_tier/image_recognition
image_name=$(find -name "*.jpg" -not -path "./facenet_pytorch/*" -or -name "*.png" -not -path "./facenet_pytorch/*" -or -name "*.jpeg"  -not -path "./facenet_pytorch/*")
python3 face_recognition.py $image_name
cd /home/ec2-user/app_tier/compute_engine
python3 send_message.py
