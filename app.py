import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# יצירת לקוח Gemini
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


@app.route("/", methods=["GET"])
def health():
    return "Bot is running!"


@app.route("/", methods=["POST"])
def google_chat():
    data = request.get_json()

    # טיפול באירוע הוספת הבוט לחדר
    if data.get("type") == "ADDED_TO_SPACE":
        return jsonify({
            "text": "שלום! אני מחובר ל-Gemini ומוכן לענות על שאלות."
        })

    # קבלת הודעת המשתמש
    message = data.get("message", {}).get("text", "")

    if not message:
        return jsonify({"text": "לא התקבלה הודעה."})

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        return jsonify({
            "text": response.text
        })

    except Exception as e:
        return jsonify({
            "text": f"שגיאה: {str(e)}"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
