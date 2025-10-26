import cv2
import mediapipe as mp
import numpy as np
import random

# --- Initialize MediaPipe Pose ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# --- Particle class for party popper effect ---
class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([random.uniform(-5,5), random.uniform(-5, -1)], dtype=float)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.radius = random.randint(3,6)
        self.life = 50

    def move(self):
        self.pos += self.vel
        self.vel[1] += 0.2  # gravity
        self.life -= 1

# --- Main Program ---
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
output_path = 'squat_session_smart.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

counter = 0
state = 'get_ready'
feedback = ''
visibility_threshold = 0.8
milestone_timer = 0
milestone_feedback = ""
particles = []

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        knee_angle = 0
        back_angle = 0

        try:
            landmarks = results.pose_landmarks.landmark

            # --- Key Landmarks ---
            l_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            l_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            l_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            r_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            r_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            is_body_visible = all(lm.visibility > visibility_threshold for lm in 
                                  [l_hip, l_knee, l_ankle, r_hip, r_knee, r_ankle, l_shoulder, r_shoulder])

            # --- Convert to (x, y) ---
            l_hip, l_knee, l_ankle = [l_hip.x, l_hip.y], [l_knee.x, l_knee.y], [l_ankle.x, l_ankle.y]
            r_hip, r_knee, r_ankle = [r_hip.x, r_hip.y], [r_knee.x, r_knee.y], [r_ankle.x, r_ankle.y]
            l_shoulder, r_shoulder = [l_shoulder.x, l_shoulder.y], [r_shoulder.x, r_shoulder.y]

            # --- Calculate Angles ---
            knee_angle = (calculate_angle(l_hip, l_knee, l_ankle) + calculate_angle(r_hip, r_knee, r_ankle)) / 2
            back_angle = (calculate_angle(l_shoulder, l_hip, l_knee) + calculate_angle(r_shoulder, r_hip, r_knee)) / 2

            # --- Squat State Machine ---
            if state == 'get_ready':
                if is_body_visible and knee_angle > 160:
                    state = 'up'
                    feedback = "STAND STRAIGHT"
                else:
                    feedback = "GET VISIBLE"

            elif state == 'up':
                if knee_angle < 140:
                    state = 'down'
                    feedback = "GO LOWER"
                else:
                    feedback = "STAND STRAIGHT" if back_angle > 160 else "STRAIGHTEN BACK"

            elif state == 'down':
                if knee_angle > 160:
                    counter += 1
                    state = 'up'
                    # Milestone every 15 reps
                    if counter % 15 == 0:
                        milestone_feedback = f"🎉 {counter} REPS DONE! GREAT JOB!"
                        milestone_timer = 60  # show for ~3 seconds at 20fps
                        # generate particles
                        for _ in range(50):
                            particles.append(Particle(frame_width//2, frame_height//2))
                    else:
                        feedback = "REP COUNTED!"
                else:
                    feedback = "FULL SQUAT!" if knee_angle < 90 else "GO LOWER"

        except:
            state = 'get_ready'
            feedback = "NO BODY DETECTED"

        # --- Render UI ---
        if "STRAIGHTEN" in feedback: feedback_box_color = (0, 0, 255)
        elif "GO LOWER" in feedback: feedback_box_color = (0, 165, 255)
        elif "FULL SQUAT" in feedback: feedback_box_color = (0, 150, 0)
        elif "COUNTED" in feedback: feedback_box_color = (200, 100, 0)
        else: feedback_box_color = (128, 0, 0)

        # Main Status Box
        cv2.rectangle(image, (0, 0), (250, 73), (50, 50, 50), -1)
        cv2.putText(image, 'REPS', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STATUS', (130, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, state.upper(), (120, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Feedback Box
        cv2.rectangle(image, (250, 0), (640, 73), feedback_box_color, -1)
        (text_width, _), _ = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_x = 250 + (390 - text_width) // 2
        cv2.putText(image, feedback, (text_x, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Debug angles
        cv2.putText(image, f"KNEE: {int(knee_angle)}", (15, frame_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f"BACK: {int(back_angle)}", (15, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Draw Pose
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

        # --- Milestone message in center ---
        if milestone_timer > 0:
            (text_width, text_height), _ = cv2.getTextSize(milestone_feedback, cv2.FONT_HERSHEY_SIMPLEX, 2, 4)
            x = (frame_width - text_width) // 2
            y = frame_height // 2
            cv2.putText(image, milestone_feedback, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 4, cv2.LINE_AA)
            milestone_timer -= 1

        # --- Draw particles ---
        new_particles = []
        for p in particles:
            cv2.circle(image, (int(p.pos[0]), int(p.pos[1])), p.radius, p.color, -1)
            p.move()
            if p.life > 0:
                new_particles.append(p)
        particles = new_particles

        out.write(image)
        cv2.imshow('Smart Squat Trainer', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
