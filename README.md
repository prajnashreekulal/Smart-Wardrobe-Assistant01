# 👗 Smart Wardrobe Assistant

An AI-powered **outfit recommendation system** built with **Flask + TensorFlow**, designed to classify clothing items and suggest perfect outfit combinations based on type, occasion, and user preferences.

---

## ⚙️ Tech Stack

- 🐍 **Python 3.10+**
- 🤖 **TensorFlow / Keras** – for machine learning model training  
- 🌐 **Flask** – lightweight backend framework for web interface  
- 🖼️ **OpenCV & PIL** – image preprocessing and analysis  
- 🗄️ **SQLite3** – lightweight local database  
- 🎨 **Bootstrap / CSS** – responsive and clean UI  
- 📊 **Matplotlib & NumPy** – data visualization and processing  

---

## 🧩 Installation & Setup

Follow these simple steps to run the project locally 👇

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/prajnashreekulal/Smart-Wardrobe-Assistant01.git
cd Smart-Wardrobe-Assistant01/py

**Step 2: Create & Activate Virtual Environment**
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate


Step 3: Install Dependencies

Requirements are defined at the project root level.

pip install -r ../requirements.txt

Step 4: Locate Model Files

Before running, make sure your pretrained models are correctly placed inside the following folder:

Outfit_Recommendation_Project/models/
├── model_top/
├── model_bottom/
├── model_sub/
└── model_shoes/


⚠️ These folders contain the .h5 or .keras files used by the recognition_module.py for outfit classification.

Step 5: Run the Flask Web App
cd ../
python py/app.py


Then open your browser and visit:
👉 http://127.0.0.1:5000/

You’ll see your Smart Wardrobe Dashboard appear!``



Outfit_Recommendation_Project/
├── venv/                     # Virtual environment (ignored in .gitignore)
├── LICENSE
├── README.md
├── requirements.txt

├── models/                   # Pretrained ML models (required before running)
│   ├── model_sub/
│   ├── model_top/
│   ├── model_bottom/
│   └── model_shoes/

├── data/                     # Training and sample data
├── train_module.py           # Training logic for custom datasets
├── training.py               # Model training runner

├── pictures/                 # Demo and visualization images
│   ├── tutorial.png
│   ├── IMG_0159.jpg
│   ├── top_question.png
│   └── 51109bb074d95c059f716e48786568f.jpg

├── proposal.md               # Project proposal and documentation

└── py/                       # Main Flask application folder
    ├── app.py                # Flask app entry point
    ├── recognition_module.py # ML prediction logic
    ├── ui_module.py          # Frontend rendering and routing
    ├── static/               # CSS, JS, and static assets
    ├── templates/            # HTML templates
    └── __pycache__/          # Cached Python files (ignored)

