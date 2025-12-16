# Hand Cricket 🏏
### Version 1.0

**Hand Cricket** is a modern, AI-powered digital version of the classic "Odd-Even" game. Built with Python and Pygame, it is available to play directly in your **Web Browser** or as a native **Windows Application**.

## 🚀 Play Now

### 🌐 [Click Here to Play in Browser] (https://hyper-crazy.github.io/Hand-Cricket/)

### 💻 [Download for Windows]
*(Go to the "Releases" section on the right to download `HandCricket.exe`)*

---

## ✨ Features

### 🤖 Smart AI Opponent
* **Adaptive Strategy:** The AI tracks your move history using probability analysis to predict your next throw.
* **Dynamic Gameplay:** It plays defensively when wickets are low and aggressively when chasing a target.

### 📊 Career Profile
* **Persistent Stats:** Automatically saves your total Runs, Wickets, Wins, and Losses.
* **Detailed Records:** Separate stats for matches against the **AI** vs. **Friends**.
* **Mode Tracking:** Tracks performance separately for **Standard** and **Hardcore** modes.

### 🎮 Game Modes
1.  **Standard Mode:**
    * Classic rules.
    * If you and the opponent show the **same number**, the batsman is **OUT**.
2.  **Hardcore Mode:**
    * Pro rules for advanced players.
    * To get a wicket, you must match the **Number AND the Exact Gesture** (e.g., Index+Middle vs. Ring+Pinky).
    * **No Ball Rule:** Playing the same gesture 6 times in a row results in a penalty.

---

## 🛠️ How to Run from Source

If you want to run the code yourself or modify it:

### Prerequisites
* Python 3.10+
* `pygame` library

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Hand-Cricket.git](https://github.com/YOUR_USERNAME/Hand-Cricket.git)
    cd Hand-Cricket
    ```
2.  **Install Dependencies:**
    ```bash
    pip install pygame
    ```
3.  **Run the Game:**
    ```bash
    python main.py
    ```

---

## 🕹️ Controls & Rules

### Controls
* **Mouse Only:** Click the hand icons to make your move.
* **Navigation:** Use the Back Arrow (Top-Left) to return to previous menus.

### Gameplay Rules
* **Scoring:** Choose a number (1-6). The thumb represents **6**.
* **Defense:** Choose **0** (Closed Fist) to block a ball without scoring runs.
* **Wicket:**
    * *Standard:* Match the number (1-6).
    * *Hardcore:* Match the exact finger pattern.
* **Free Hit:** Occurs after a No Ball (Hardcore only). You cannot get out, and the special **'5' gesture** is unlocked.

---

## 🏗️ Technology Stack

* **Engine:** Python (Pygame)
* **Web Build:** Pygbag (WebAssembly)
* **Windows Build:** PyInstaller
* **CI/CD:** GitHub Actions (Automated
