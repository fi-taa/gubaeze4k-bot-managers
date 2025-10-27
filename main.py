import logging
from os import getenv
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
GROUP_CHAT_ID = getenv("GROUP_CHAT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

user_to_group_message = {}
group_to_user_message = {}


async def handle_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        await update.message.reply_text("Only text messages are supported.")
        return

    user_id = update.message.chat.id
    message_text = update.message.text

    try:
        sent_message = await context.bot.send_message(
            chat_id=GROUP_CHAT_ID, text=f"User {user_id}: {message_text}"
        )

        user_to_group_message[user_id] = sent_message.message_id
        group_to_user_message[sent_message.message_id] = user_id

        await update.message.reply_text("Message sent to the group!")

    except Exception as e:
        logger.error(f"Error forwarding message: {e}")
        await update.message.reply_text("Failed to send message to group.")


async def handle_group_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.reply_to_message:
        return

    if str(update.message.chat.id) != GROUP_CHAT_ID:
        return

    replied_message_id = update.message.reply_to_message.message_id
    user_id = group_to_user_message.get(replied_message_id)

    if not user_id:
        return

    reply_text = update.message.text
    if not reply_text:
        return

    try:
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        logger.info(f"Replied to user {user_id}")

    except Exception as e:
        logger.error(f"Error sending reply: {e}")


async def post_init(application: Application) -> None:
    logger.info("Bot started")
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID not set. Bot will not forward messages.")
    if not TOKEN:
        logger.error("BOT_TOKEN not set. Bot cannot start.")


def main() -> None:
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set")

    application = Application.builder().token(TOKEN).post_init(post_init).build()

    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, handle_bot_message))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.ChatType.PRIVATE), handle_group_reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

