import cv2
import time
import webbrowser
import pyautogui as pg

from tracker import PoseDetector

DOWN_THRESHOLD = 160
LEFT_THRESHOLD = RIGHT_THRESHOLD = 130
GAME_URL = 'https://arcadespot.com/game/road-rash/'

def open_game_tab():
    webbrowser.open(GAME_URL, new=2)

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def main():
    open_game_tab()
    
    time.sleep(3)
    
    pg.keyDown('x')
    pg.keyDown('up')
    
    global count, hand_near_face, up_key_pressed

    cap = cv2.VideoCapture(0)

    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    left_key_pressed = False
    right_key_pressed = False
    down_key_pressed = False

    while True:
        _, raw_img = cap.read()

        img = pose_detector.findPose(raw_img)
        lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

        try:
            if len(lmList) >= 16:
                
                right_elbow_coords = lmList[11][:2]
                right_wrist_coords = lmList[15][:2]

                left_elbow_coords = lmList[12][:2]
                left_wrist_coords = lmList[16][:2]
                
                left_distance, _, _ = pose_detector.findDistance(left_elbow_coords, left_wrist_coords, img=img, color=(0, 0, 255), scale=5)
                right_distance, _, _ = pose_detector.findDistance(right_elbow_coords, right_wrist_coords, img=img, color=(0, 0, 255), scale=5)                

                # put_text(img, f"L : {round(left_distance, 2)}", (img.shape[1]-300, 100))
                # put_text(img, f"R : {round(right_distance, 2)}", (img.shape[1]-300, 140))
                put_text(img, f"Left Key: {'Pressed' if left_key_pressed else 'Released'}", (img.shape[1]-300, 100))
                put_text(img, f"Right Key: {'Pressed' if right_key_pressed else 'Released'}", (img.shape[1]-300, 140))

                if left_distance < LEFT_THRESHOLD and not left_key_pressed:
                    pg.keyDown('left')
                    left_key_pressed = True

                elif left_distance >= LEFT_THRESHOLD and left_key_pressed:
                    pg.keyUp('left')
                    left_key_pressed = False

                if right_distance < RIGHT_THRESHOLD and not right_key_pressed:
                    pg.keyDown('right')
                    right_key_pressed = True

                elif right_distance >= RIGHT_THRESHOLD and right_key_pressed:
                    pg.keyUp('right')
                    right_key_pressed = False

                if left_distance < DOWN_THRESHOLD and right_distance < DOWN_THRESHOLD and not down_key_pressed:
                    pg.keyDown('x')
                    down_key_pressed = True

                elif left_distance >= DOWN_THRESHOLD and right_distance >= DOWN_THRESHOLD and down_key_pressed:
                    pg.keyUp('x')
                    down_key_pressed = False

        except Exception as e:
            print(e)
                
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Image", 320, 240)
        cv2.imshow("Image", raw_img)
        if cv2.waitKey(5) & 0xFF == 27:
            break
 
if __name__ == "__main__":
    main()