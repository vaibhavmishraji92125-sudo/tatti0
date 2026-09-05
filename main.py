# main.py

import math
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from api import API_ID, API_HASH, BOT_TOKEN

# Initialize the bot
app = Client(
    "AdvancedCalcBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Safe execution environment for math calculations
MATH_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,       # Base 10 Logarithm
    "ln": math.log,          # Natural Logarithm
    "fac": math.factorial,   # Factorial
    "pi": math.pi,
    "e": math.e,
}

def calc_keyboard():
    """Generates the interactive Inline Keyboard UI for the calculator."""
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
    """Sends the calculator UI when the user starts the bot."""
    message.reply_text(
        "🧮 **Advanced Scientific Calculator**\n\n`0`",
        reply_markup=calc_keyboard()
    )

@app.on_callback_query()
def calculator_logic(client, callback_query: CallbackQuery):
    """Handles button presses and performs calculations."""
    data = callback_query.data
    
    # Extract the current math expression from the message text
    current_text = callback_query.message.text.split("\n\n")[-1].replace("`", "")
    
    if current_text in ["0", "Error"]:
        current_text = ""
        
    if data == "AC":
        new_text = "0"
    elif data == "DEL":
        new_text = current_text[:-1] if len(current_text) > 1 else "0"
    elif data == "=":
        try:
            # Evaluate the mathematical expression
            result = eval(current_text, {"__builtins__": {}}, MATH_FUNCTIONS)
            
            # Format the result to avoid overly long decimals
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
                
            new_text = str(result)
        except Exception:
            new_text = "Error"
    else:
        new_text = current_text + data
        
    # Update the UI with the new text
    try:
        callback_query.message.edit_text(
            f"🧮 **Advanced Scientific Calculator**\n\n`{new_text}`",
            reply_markup=calc_keyboard()
        )
    except Exception:
        # Ignore pyrogram's "MessageNotModified" error if the user clicks the same button rapidly
        pass 
        
    callback_query.answer()

if __name__ == "__main__":
    print("🤖 Bot is starting...")
    app.run()
