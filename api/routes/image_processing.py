from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

router = APIRouter()


@router.post("/are_hands_up/")
async def are_hands_up(file: UploadFile = File(...)):
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
        image_bytes = await file.read()
        
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if image is None:
            return JSONResponse(content={"Detected_person": False, "Message": "Error decoding image"})
        
        image_height, image_width, _ = image.shape
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.pose_landmarks:
            return JSONResponse(content={"Detected_person": False, "Message": "No pose landmarks detected"})
        
        landmarks = results.pose_landmarks.landmark
        
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        
        left_hand_above_head = left_hand.y < nose.y
        right_hand_above_head = right_hand.y < nose.y
        hands_above_head = left_hand_above_head and right_hand_above_head
        
        return JSONResponse(content={
            "Detected_person": True,
            "Message": "Pose detected",
            "HandsAboveHead": hands_above_head,
            "LeftHandAboveHead": left_hand_above_head,
            "RightHandAboveHead": right_hand_above_head,
            "Nose coordinates": (nose.x * image_width, nose.y * image_height),
            "Left hand coordinates": (left_hand.x * image_width, left_hand.y * image_height),
            "Right hand coordinates": (right_hand.x * image_width, right_hand.y * image_height)
        })
