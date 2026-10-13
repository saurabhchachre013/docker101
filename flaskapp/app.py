from flask import Flask, request
import random

app = Flask(__name__)

secret_number = random.randint(1, 100)

@app.route("/", methods=["GET", "POST"])
def home():
    message = "🎮 Guess a number between 1 and 100!"
    guess = ""

    if request.method == "POST":
        guess = request.form.get("guess", "")

        try:
            number = int(guess)

            if number < 1 or number > 100:
                message = "⚠️ Enter a number from 1 to 100!"
            elif number < secret_number:
                message = "📈 Too low! Try a higher number."
            elif number > secret_number:
                message = "📉 Too high! Try a lower number."
            else:
                message = "🎉 Correct! You won! Refresh to play again."
        except ValueError:
            message = "❌ Please enter a valid number!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guess the Number</title>
        <style>
            body {{
                font-family: Arial;
                background: #151515;
                color: white;
                text-align: center;
                padding-top: 100px;
            }}
            .game {{
                background: #292929;
                padding: 30px;
                border-radius: 15px;
                display: inline-block;
            }}
            input, button {{
                padding: 12px;
                border-radius: 8px;
                border: none;
                margin: 5px;
            }}
            button {{
                background: #00c896;
                cursor: pointer;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="game">
            <h1>🐳 Docker Number Game</h1>
            <p>{message}</p>
            <form method="POST">
                <input type="number" name="guess"
                       min="1" max="100" required
                       placeholder="Enter your guess">
                <button type="submit">Guess!</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)