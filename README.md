Eternal Space Simulator (ESS) 🚀✨

Eternal Space Simulator is a 3D space exploration game developed in Python using Pygame and OpenGL. Embark on an interstellar journey, navigate through a vast universe filled with stars, planets, and other celestial bodies. Monitor your progress with real-time HUD displays showing your playtime and distance traveled.

Table of Contents
Features
System Requirements
Installation
How to Play
Controls
Saving and Loading
Contributing
License
Acknowledgements
Contact
Features
3D Space Exploration: Navigate through a dynamically generated universe with diverse celestial objects.
Real-Time HUD: Monitor your playtime and distance traveled with a sleek Heads-Up Display.
Customizable Spaceship: Control your spaceship's movement and rotation with intuitive keyboard inputs.
Persistent Progress: Save and load your game progress seamlessly.
Modern Logging: Robust logging system to track game events and errors.
System Requirements
Minimum Requirements
Operating System:
Windows 7 (64-bit) or higher
macOS 10.12 (Sierra) or higher
Linux (Ubuntu 18.04 LTS or similar)
Processor: Intel Core i3-2100 or equivalent (3.1 GHz)
Memory: 4 GB RAM
Graphics:
NVIDIA GeForce GTX 650 or AMD Radeon HD 7750 with OpenGL 3.3 support
Storage: 500 MB available space
Additional Software: Python 3.7 or higher
Recommended Requirements
Operating System:
Windows 10 (64-bit)
macOS 10.15 (Catalina) or higher
Linux (Ubuntu 20.04 LTS or similar)
Processor: Intel Core i5-7400 or equivalent (3.0 GHz+)
Memory: 8 GB RAM
Graphics:
NVIDIA GeForce GTX 1060 or AMD Radeon RX 580 with OpenGL 4.0 support
Storage: 1 GB available space (SSD recommended)
Additional Software: Python 3.8 or higher
Installation
Clone the Repository

Use the following command to clone the repository:

git clone https://github.com/gabrielrocca369/ESS-eternal-space-simulator-ia.git

Navigate to the project directory:

cd ESS-eternal-space-simulator-ia

Create a Virtual Environment (Optional but Recommended)

Create a virtual environment to manage dependencies:

python3 -m venv env

Activate the virtual environment:

On Windows: env\Scripts\activate
On macOS/Linux: source env/bin/activate
Install Dependencies

Install the required Python libraries:

pip install -r requirements.txt

If you don't have a requirements.txt, install the necessary libraries manually:

pip install pygame PyOpenGL

Run the Game

Start the game using the following command:

python main.py

How to Play
Eternal Space Simulator thrusts you into the role of a space explorer navigating the cosmos. Start by entering your name, and then pilot your spaceship through an expansive universe. Keep an eye on your HUD to track how long you've been playing and the distance you've traveled.

Controls
Movement:

W - Move Forward
S - Move Backward
A - Move Left
D - Move Right
Rotation:

Q - Rotate Left
E - Rotate Right
Other Controls:

Enter - Start New Game or Confirm Actions
K - View Keyboard Instructions
Esc - Pause Game / Return to Menu
Saving and Loading
Automatic Saving: Your game progress is automatically saved upon exiting the game. This includes your spaceship's position, velocity, acceleration, rotation angle, total distance traveled, and playtime.
Loading Progress: When you restart the game, it will automatically load your last saved progress, allowing you to continue your journey seamlessly.
Contributing
Contributions are welcome! Whether it's reporting bugs, suggesting features, or submitting pull requests, your input is valuable to the development of Eternal Space Simulator.

Fork the Repository

Create a New Branch

git checkout -b feature/YourFeatureName

Commit Your Changes

git commit -m "Add some feature"

Push to the Branch

git push origin feature/YourFeatureName

Open a Pull Request

License
This project is licensed under the MIT License.

Acknowledgements
Pygame: For providing a robust library for game development in Python.
PyOpenGL: For enabling OpenGL support in Python, allowing for 3D rendering.
