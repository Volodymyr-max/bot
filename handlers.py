from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from database import (
    add_user,
    get_user,
    update_user,
    delete_user,
    list_users,
)
import datetime

# Список вопросов для регистрации
QUESTIONS = [
    "Введите ваш игровой ID в PUBG:",
    "Введите ваше имя:",
    "Введите ваш возраст:",
    "Введите вашу область проживания:",
]

# Для отслеживания шагов регистрации
user_steps = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Введите /register чтобы пройти регистрацию.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_steps[user_id] = {"step": 0, "data": {}}
    await update.message.reply_text(QUESTIONS[0])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_steps:
        return

    step_info = user_steps[user_id]
    step = step_info["step"]
    data = step_info["data"]
    text = update.message.text.strip()

    if step == 0:
        data["game_id"] = text
    elif step == 1:
        data["name"] = text
    elif step == 2:
        data["age"] = text
    elif step == 3:
        data["region"] = text
        add_user(user_id, data["game_id"], data["name"], data["age"], data["region"])
        del user_steps[user_id]
        await update.message.reply_text("Регистрация завершена! Теперь вы можете использовать /me")
        return

    step_info["step"] += 1
    await update.message.reply_text(QUESTIONS[step_info["step"]])

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if user:
        response = (
            f"👤 <b>Ваши данные:</b>\n"
            f"🎮 ID: <code>{user[1]}</code>\n"
            f"🧑 Имя: {user[2]}\n"
            f"📅 Возраст: {user[3]}\n"
            f"📍 Область: {user[4]}"
        )
        await update.message.reply_html(response)
    else:
        await update.message.reply_text("Вы ещё не зарегистрированы. Введите /register.")

async def update_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_steps[user_id] = {"step": 0, "data": {}}
    await update.message.reply_text("Обновим информацию. " + QUESTIONS[0])

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_steps:
        del user_steps[user_id]
    await update.message.reply_text("Действие отменено.")

def register_handlers(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("update_me", update_me))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
