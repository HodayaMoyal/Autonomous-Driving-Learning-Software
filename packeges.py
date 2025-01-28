# FLASK מאפשר לאפליקצית  לקבל בקשות מכתובות URL שונות
from flask_cors import CORS
#שימוש בפונקציה שכתבתי
from center_point import get_traffic_sign_center
# ספריה מתמטית המספקת פונקציות מתמטיות שונות כמו טריגונומטריה ולוגריתמים
import math
# FLASK - WEB יוצר אפליקציות  
# request -  נכנסותHTTP מטפל בבקשות  
# jsonify -JSON ממיר מילונים לתגובות 
from flask import Flask, request, jsonify
# ספריה המספקת פונקציות שונות הקשורות לזמן, כמו השהייה ומדידת זמן ביצוע
import time
# ספריה המספקת תמיכה לפעולות מתמטיות על מערכים ומטריצות.
import numpy as np
# YOLO ספריה המספקת כלים לזיהוי עצמים באמצעות מודלי 
from ultralytics import YOLO
#פונקציה לחישוב מרחק בין שני קואורדינטות גיאוגרפיות.
from geopy.distance import geodesic 
# ספריה המספקת פונקציות תלויות מערכת הפעלה כמו קריאה/כתיבה לקבצים ומשתני סביבה
import os
# מחלקה לטיפול באובייקטים של תאריך ושעה 
from datetime import datetime
# ספרייה לשליטה תכנותית בעכבר ובמקלדת אני השתמשתי לצילום מסך
import pyautogui
# OpenCV (cv2) מספקת כלים לעיבוד תמונה ווידאו, כולל זיהוי עצמים ושינויי תמונה
import cv2
# YAML ספרייה לניתוח ויצירת קבצי , המשמשים לרוב לקבצי קונפיגורציה
# import yaml

