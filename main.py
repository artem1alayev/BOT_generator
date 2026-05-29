import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

QUESTION_ONE, QUESTION_TWO = range(2)

# This starts the conversation when a user types /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hello! Let's do some math. What is the first number?")
    return QUESTION_ONE

# This catches the first number
async def get_first_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['num1'] = update.message.text
    await update.message.reply_text("Got it. Now, what is the second number?")
    return QUESTION_TWO

# This catches the second number and does the calculation
async def get_second_and_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    num2 = update.message.text
    num1 = context.user_data['num1']
    
    try:
        n1 = float(num1)
        n2 = float(num2)
        
        # --- DO YOUR CALCULATIONS HERE ---
        result = n1 + n2  # Example calculation
        
        await update.message.reply_text(f"Calculation complete!\n\n{n1} + {n2} = {result}")
        
    except ValueError:
        await update.message.reply_text("Oops! One of those wasn't a valid number. Let's stop here.")
    
    context.user_data.clear()
    return ConversationHandler.END

# A safety exit if the user types /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation canceled.")
    context.user_data.clear()
    return ConversationHandler.END

def main():
    # Grab your token (or paste it straight as a string here for testing)
    TOKEN = "8775044535:AAEO5u8tnFn1HdtAKgIYvDqXdOLb80QV6IM"
    
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION_ONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_first_number)],
            QUESTION_TWO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_second_and_calculate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    
    print("Bot is successfully running...")
    app.run_polling()

if __name__ == "__main__":
    main()