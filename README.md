# AI Squat Trainer

==================
## 🎥 Demo
[WhatsApp Video 2026-01-20 at 11.36.47 PM.mp4 (CLICK HERE)](https://github.com/user-attachments/assets/30952aa4-ff9f-414d-8bde-d5f748a2412e)

> Your personal AI-powered fitness coach that counts your squats and corrects your form in real-time, right from your webcam.

This project uses Python with OpenCV and MediaPipe to create a smart squat counter. It goes beyond simple counting by implementing an intelligent state machine that waits for the user to stand straight before starting, and provides real-time feedback on squat depth and posture to ensure proper form.

*(A live demonstration of the application counting reps and providing real-time form feedback.)*

## ✨ Key Features

* 🧠 **Intelligent State Machine:** The trainer waits for you to stand straight in a visible position before it starts counting. No more accidental counts from random movements!

* 🏋️‍♂️ **Real-Time Repetition Counting:** Accurately counts squats by tracking the angle of your knees.

* 💪 **Form Correction:** Actively monitors your back posture and squat depth, providing instant visual feedback to help you maintain proper form.

* 🎯 **Reward Milestones:** Celebrate milestones every 15 reps with an on-screen message and a fun party popper effect.

* 📊 **Intuitive UI:** A clean, on-screen display shows your rep count, current stage (GET_READY, UP, DOWN), and color-coded form feedback.

* 📹 **Session Recording:** Automatically records your workout session and saves it as an .mp4 file for you to review later.

* 🐛 **Live Debug View:** An optional display shows the exact knee and back angles the AI is tracking, helping you understand its logic.

---

## 🧠 How It Works

The application processes your webcam feed frame-by-frame to analyze your posture and count repetitions.

1. **Video Capture:** OpenCV is used to capture the live video feed from your webcam.

2. **Pose Estimation:** Google's MediaPipe library is used to detect and track 33 key body landmarks (joints) in real-time.

3. **Angle Calculation:** The program calculates the angles at the knees (hip-knee-ankle) and back (shoulder-hip-knee) to understand your squat depth and posture.

4. **State Machine Logic:** The core of the trainer is a state machine that progresses through three states:

   * **GET_READY**: The initial state. The program waits for you to stand straight in view, preventing false counts.

   * **UP**: You are standing upright. The trainer now actively waits for you to lower into a squat.

   * **DOWN**: You have reached the squat position. The trainer now waits for you to return to standing. A rep is counted upon returning to the UP state.

5. **Form Analysis:** In every frame, the program also monitors back posture and squat depth. Feedback like “GO LOWER” or “STRAIGHTEN BACK” is provided to ensure proper form and reduce injury risk.

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

* Python 3.8+

* A webcam connected to your computer.

### 🛠️ Installation & Setup

1. **Clone the repository:**

```bash
git clone [https://github.com/your-username/AI-Squat-Trainer.git]
cd AI-Squat-Trainer
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install the required libraries:**

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ How to Run

With your virtual environment activated and dependencies installed, run the following command in your terminal:

```bash
python squat_trainer.py
```

* A window will pop up showing your webcam feed.
* Position yourself so your full body is visible.
* Follow the on-screen prompts to get into the proper starting position.
* Press the **'q'** key to quit the application.
* A video file named `squat_session_smart.mp4` will be saved in the project folder.

---

## 🔧 Technologies Used

* **Python:** The core programming language.
* **OpenCV:** For video capture, image processing, and rendering the UI.
* **MediaPipe:** For high-fidelity body pose tracking.
* **NumPy:** For numerical operations and angle calculations.

---

## 💡 Future Improvements

* [ ] **Audio Feedback:** Add voice cues for rep counts, milestones, and form corrections.
* [ ] **Advanced Posture Analysis:** Include hip alignment and knee tracking to further reduce injury risk.
* [ ] **Workout Logging:** Save workout stats (reps, milestones, session duration) to a CSV or database.
* [ ] **Multiple Exercise Support:** Extend to other exercises like push-ups, lunges, and planks.
* [ ] **Customizable Milestones:** Allow users to set milestone frequency and reward effects.

---

