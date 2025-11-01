⚙️ Tech Stack

Python 3.10+

TensorFlow / Keras

Flask (for web app)

OpenCV & PIL (for image handling)

SQLite3 (for local data storage)

Bootstrap / CSS (for UI)

Matplotlib & Numpy (for processing)

🧩 Installation & Setup
Step 1: Clone the Repository
git clone https://github.com/<your-username>/Smart-Wardrobe-Assistant.git
cd Smart-Wardrobe-Assistant/py

Step 2: Create & Activate Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

Step 3: Install Dependencies
pip install -r ../requirements.txt



Flask Web App run:

If you’re using the Flask version (with app.py inside py/):

cd ../
python py/app.py


Then open your browser and go to:

http://127.0.0.1:5000/


Outfit_Recommendation_Project/
├── venv/                      # Virtual environment (ignored in .gitignore)
├── LICENSE
├── README.md
├── requirements.txt
│
├── models/
│   ├── data/
│   ├── models/
│   │   ├── model_sub/
│   │   ├── model_top/
│   │   ├── model_bottom/
│   │   └── model_shoes/
│   ├── train_module.py
│   └── training.py
│
├── pictures/
│   ├── tutorial.png
│   ├── IMG_0159.jpg
│   ├── top_question.png
│   └── 51109bb074d95c059f716e48786568f.jpg
│
├── proposal.md
│
└── py/                        # Main app folder
    ├── app.py                 # Flask app entry point
    ├── recognition_module.py
    ├── ui_module.py
    ├── static/                # CSS, JS, and images
    ├── templates/             # HTML files
    └── __pycache__/           # Ignored automatically
