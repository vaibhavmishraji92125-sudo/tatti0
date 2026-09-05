# main.py

import asyncio
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import math

# --- 1. ASYNCIO PATCH (Fixes the Python 3.14 crash) ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ------------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from api import API_ID, API_HASH, BOT_TOKEN

# --- 2. DUMMY WEB SERVER (Satisfies Render's Port binding requirement) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
        
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Start the web server in a background thread
threading.Thread(target=run_dummy_server, daemon=True).start()
# -------------------------------------------------------------------------

# --- 3. BOT LOGIC ---
app = Client(
    "AdvancedCalcBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

MATH_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,       
    "ln": math.log,          
    "fac": math.factorial,   
    "pi": math.pi,
    "e": math.e,
}

def calc_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("sin(", callback_data="sin("), 
            InlineKeyboardButton("cos(", callback_data="cos("), 
            InlineKeyboardButton("tan(", callback_data="tan("), 
            InlineKeyboardButton("DEL", callback_data="DEL")
        ],
        [
            InlineKeyboardButton("log(", callback_data="log("), 
            InlineKeyboardButton("ln(", callback_data="ln("), 
            InlineKeyboardButton("antilog", callback_data="10**"), 
            InlineKeyboardButton("n!", callback_data="fac(")
        ],
        [
            InlineKeyboardButton("(", callback_data="("), 
            InlineKeyboardButton(")", callback_data=")"), 
            InlineKeyboardButton("^", callback_data="**"), 
            InlineKeyboardButton("AC", callback_data="AC")
        ],
        [
            InlineKeyboardButton("7", callback_data="7"), 
            InlineKeyboardButton("8", callback_data="8"), 
            InlineKeyboardButton("9", callback_data="9"), 
            InlineKeyboardButton("÷", callback_data="/")
        ],
        [
            InlineKeyboardButton("4", callback_data="4"), 
            InlineKeyboardButton("5", callback_data="5"), 
            InlineKeyboardButton("6", callback_data="6"), 
            InlineKeyboardButton("×", callback_data="*")
        ],
        [
            InlineKeyboardButton("1", callback_data="1"), 
            InlineKeyboardButton("2", callback_data="2"), 
            InlineKeyboardButton("3", callback_data="3"), 
            InlineKeyboardButton("-", callback_data="-")
        ],
        [
            InlineKeyboardButton("0", callback_data="0"), 
            InlineKeyboardButton(".", callback_data="."), 
            InlineKeyboardButton("=", callback_data="="), 
            InlineKeyboardButton("+", callback_data="+")
        ]
    ])

@app.on_message(filters.command("start") | filters.command("calc"))
def start_calc(client, message):
    message.reply_text(
        "🧮 **Advanced Scientific Calculator**\n\n`0`",
        reply_markup=calc_keyboard()
    )

@app.on_callback_query()
def calculator_logic(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    current_text = callback_query.message.text.split("\n\n")[-1].replace("`", "")
    
    if current_text in ["0", "Error"]:
        current_text = ""
        
    if data == "AC":
        new_text = "0"
    elif data == "DEL":
        new_text = current_text[:-1] if len(current_text) > 1 else "0"
    elif data == "=":
        try:
            result = eval(current_text, {"__builtins__": {}}, MATH_FUNCTIONS)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
            new_text = str(result)
        except Exception:
            new_text = "Error"
    else:
        new_text = current_text + data
        
    try:
        callback_query.message.edit_text(
            f"🧮 **Advanced Scientific Calculator**\n\n`{new_text}`",
            reply_markup=calc_keyboard()
        )
    except Exception:
        pass 
        
    callback_query.answer()

if __name__ == "__main__":
    print("🤖 Bot and dummy web server are starting...")
    app.run()
