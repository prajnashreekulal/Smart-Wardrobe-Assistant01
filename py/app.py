from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os, random, sqlite3
from recognition_module import single_classification  # your ML model

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ---------------------------
# Upload folder
# ---------------------------
BASE_UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

# ---------------------------
# DB
# ---------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "wardrobe.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def index():
    return render_template("index.html", user=session.get("user_id"))

# ---------------------------
# Login/Register
# ---------------------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password)).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)", (username,email,password))
            conn.commit()
            user_id = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
        except:
            conn.close()
            return render_template("register.html", error="Username or email already exists")
        conn.close()
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ---------------------------
# Upload route
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload():
    user_id = session.get("user_id", "guest")
    user_folder = os.path.join(BASE_UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    file = request.files["file"]
    filepath = os.path.join(user_folder, file.filename)
    file.save(filepath)

    subtype, info_str, details = single_classification(filepath)

    # Save to DB
    conn = get_db_connection()
    conn.execute("INSERT INTO clothes (user_id,file_path,subtype,color,season,occasion) VALUES (?,?,?,?,?,?)",
                 (user_id, filepath, subtype, details[2], details[3], details[4]))
    conn.commit()
    conn.close()

    return jsonify({
        "file_url": f"/static/uploads/{user_id}/{file.filename}",
        "subtype": subtype,
        "season": details[3],
        "occasion": details[4],
        "info": info_str
    })

# ---------------------------
# Recommendation
# ---------------------------
@app.route("/recommend")
def recommend():
    user_id = session.get("user_id", "guest")
    user_folder = os.path.join(BASE_UPLOAD_FOLDER, str(user_id))
    files = os.listdir(user_folder) if os.path.exists(user_folder) else []

    outfits = []
    for f in files:
        filepath = os.path.join(user_folder, f)
        subtype, info, details = single_classification(filepath)
        outfits.append({
            "file": f,
            "subtype": subtype,
            "details": details,
            "url": f"/static/uploads/{user_id}/{f}"
        })
       
    tops = [o for o in outfits if o["subtype"]=="top"]
    bottoms = [o for o in outfits if o["subtype"]=="bottom"]
    shoes = [o for o in outfits if o["subtype"]=="foot"]

    if not tops or not bottoms or not shoes:
        return jsonify({"error": "Need at least one top, bottom, and shoe."})

    random.shuffle(tops)
    random.shuffle(bottoms)
    random.shuffle(shoes)

    for t in tops:
        for b in bottoms:
            for s in shoes:
                if t["details"][3]==b["details"][3]==s["details"][3] and t["details"][4]==b["details"][4]==s["details"][4]:
                    return jsonify({
                        "top": t["url"],
                        "bottom": b["url"],
                        "shoe": s["url"],
                        "season": t["details"][3],
                        "occasion": t["details"][4]
                    })

    # fallback
    return jsonify({
        "top": tops[0]["url"],
        "bottom": bottoms[0]["url"],
        "shoe": shoes[0]["url"],
        "season": tops[0]["details"][3],
        "occasion": tops[0]["details"][4]
    })


# ---------------------------
# Wardrobe page
# ---------------------------
@app.route("/wardrobe")
def wardrobe():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    clothes = conn.execute("SELECT * FROM clothes WHERE user_id=?", (user_id,)).fetchall()
    conn.close()

    # Organize clothes by subtype
    wardrobe = {"top": [], "bottom": [], "foot": []}
    for c in clothes:
        wardrobe[c["subtype"]].append({
            "file_name": os.path.basename(c["file_path"]),
            "url": f"/static/uploads/{user_id}/{os.path.basename(c['file_path'])}",
            "subtype": c["subtype"]
        })

    return render_template("wardrobe.html", wardrobe=wardrobe, user=user_id)


#delete warrobe image 
@app.route("/delete_item", methods=["POST"])
def delete_item():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"})

    user_id = session["user_id"]
    data = request.get_json()
    file_name = data.get("file")
    file_path = os.path.join(BASE_UPLOAD_FOLDER, str(user_id), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        # Remove from DB
        conn = get_db_connection()
        conn.execute("DELETE FROM clothes WHERE user_id=? AND file_path=?", (user_id, file_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "File not found"})

# ---------------------------
# Run
# ---------------------------
if __name__=="__main__":
    app.run(debug=True, port=5000)
