import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

ASKING = 0
load_dotenv()



# 1. Update the master list with your specific area question
QUESTIONS = [
    "Please enter the total area (in cm²):",
    "What griliato cell size do you want to use?"
]

GRILIATO_CELLS = [
    "Griliato 25x25",
    "Griliato 50x50",
    "Griliato 100x100",
    "Griliato 150x150",
    "Griliato 200x200",]



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['answers'] = []
    await update.message.reply_text("Hello! Let's collect your data. " + QUESTIONS[0])
    return ASKING

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers = context.user_data.get('answers', [])
    answers.append(update.message.text)
    context.user_data['answers'] = answers

    # Check if there are more questions left
    if len(answers) < len(QUESTIONS):
        next_question = QUESTIONS[len(answers)]
        await update.message.reply_text(next_question)
        if len(answers) == 1:
            button_layout = [[cell] for cell in GRILIATO_CELLS]
            markup = ReplyKeyboardMarkup(button_layout, one_time_keyboard = True, resize_keyboard = True)
            await update.message.reply_text(QUESTIONS[1], reply_markup = markup)
        return ASKING




    # All answers collected! Time for the calculations
    try:
        numbers = [float(x) for x in answers]
        
        # 2. Extract your specific variables by their position in the list
        area_cm2 = numbers[0]
        griliato_cell = answers[1]
        
        # --- DO YOUR ACTUAL CALCULATIONS HERE ---
        # Example: Let's say you multiply the area by the second number
        result = area_cm2 * griliato_cell
        
        response_text = (
            f"📊 **Calculation Results:**\n\n"
            f"• Provided Area: {area_cm2} cm²\n"
            f"• Griliato Cell: {griliato_cell}\n"
            f"• Final Result: {result}"
        )
        
        await update.message.reply_text(response_text, parse_mode="Markdown")
        
    except ValueError:
        await update.message.reply_text("Oops! One of your inputs wasn't a valid number. Resetting.")
    
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation canceled.")
    context.user_data.clear()
    return ConversationHandler.END


def main():
    TOKEN = os.getenv("MY_API_KEY")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    
    print("Bot is successfully running with area input...")
    app.run_polling()

if __name__ == "__main__":
    main()