import cv2
import mediapipe as mp
import pyfirmata
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def is_arm_extended(landmarks):
  # 左肩、左肘、左手首のランドマークのインデックス
  left_shoulder = mp_pose.PoseLandmark.LEFT_SHOULDER.value
  left_elbow = mp_pose.PoseLandmark.LEFT_ELBOW.value
  left_wrist = mp_pose.PoseLandmark.LEFT_WRIST.value
  # 右肩、右肘、右手首のランドマークのインデックス
  right_shoulder = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
  right_elbow = mp_pose.PoseLandmark.RIGHT_ELBOW.value
  right_wrist = mp_pose.PoseLandmark.RIGHT_WRIST.value
  # 肩と肘と手首の座標を取得
  l_shoulder_x = landmarks.landmark[left_shoulder].x
  l_shoulder_y = landmarks.landmark[left_shoulder].y
  l_elbow_x = landmarks.landmark[left_elbow].x
  l_elbow_y = landmarks.landmark[left_elbow].y
  l_wrist_x = landmarks.landmark[left_wrist].x
  l_wrist_y = landmarks.landmark[left_wrist].y
  r_shoulder_x = landmarks.landmark[right_shoulder].x
  r_shoulder_y = landmarks.landmark[right_shoulder].y
  r_elbow_x = landmarks.landmark[right_elbow].x
  r_elbow_y = landmarks.landmark[right_elbow].y
  r_wrist_x = landmarks.landmark[right_wrist].x
  r_wrist_y = landmarks.landmark[right_wrist].y

  # 肩と肘と手首の距離を計算（ピタゴラスの定理）
  l_arm_length = ((l_shoulder_x - l_elbow_x) ** 2 + (l_shoulder_y - l_elbow_y) ** 2) ** 0.5 + \
                 ((l_elbow_x - l_wrist_x) ** 2 + (l_elbow_y - l_wrist_y) ** 2) ** 0.5
  r_arm_length = ((r_shoulder_x - r_elbow_x) ** 2 + (r_shoulder_y - r_elbow_y) ** 2) ** 0.5 + \
                 ((r_elbow_x - r_wrist_x) ** 2 + (r_elbow_y - r_wrist_y) ** 2) ** 0.5
  # 距離が閾値以上であれば、腕が伸びていると判断（閾値は適宜調整）
  threshold = 0.5
  if l_arm_length < threshold and r_arm_length < threshold:
    return True # 腕が伸びている
  else:
    return False # 腕が伸びていない
  
def main():
  # cap = cv2.VideoCapture('/Users/awayaniina/logistic/sample.mp4')
  cap = cv2.VideoCapture(0)
  pose= mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5)

  # 腕が伸びた回数をカウントする変数
  arm_count = 0
  # 前回の判定結果を保持する変数
  prev_result = False
  # 腕が伸びている時間を計測する変数
  arm_time = 0
  # 腕が伸び始めた時刻を保持する変数
  start_time = None

  while True:
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # 腕が伸びているかどうかを判定
    result = is_arm_extended(results.pose_landmarks)
    if result:
      # 腕が伸びていれば「OK」と表示
      cv2.putText(image, "OK", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
      # 前回の判定結果がFalseであれば、腕が伸びた回数をインクリメント
      if not prev_result:
        arm_count += 1
      # 腕が伸び始めた時刻を記録
      if start_time is None:
        start_time = time.time()
    else:
      # 腕が伸びていなければ「NG」と表示
      cv2.putText(image, "NG", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
      # 腕が伸びていた時間を計算
      if start_time is not None:
        end_time = time.time()
        arm_time += end_time - start_time
        start_time = None

    # 前回の判定結果を更新
    prev_result = result
    # 腕が伸びた回数を表示
    cv2.putText(image, f"Count: {arm_count}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
    cv2.imshow('MediaPipe Pose', image)

    # 腕が伸びている時間を表示
    cv2.putText(image, f"Time: {arm_time:.2f}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

if __name__ == "__main__":
  main()