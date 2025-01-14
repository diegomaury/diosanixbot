import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
import os
import signal
import sys

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8092436564:AAG0AsALo5K8RDX1h6Z4bFF_6l_70r01ktU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manda un mensaje cuando se usa el comando /start."""
    try:
        user_name = update.effective_user.first_name  # Obtiene el nombre del usuario
        await update.message.reply_text(
            f"Desde las sombras eternas, yo, Nix, saludo a {user_name}. "
            "Disfruta y sucumbe de los placeres y el morbo de mi noche. 😈✨🌙"
        )
    except Exception as e:
        logger.error(f"Error en el comando /start: {e}")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida a los nuevos usuarios que se unen al grupo."""
    try:
        for member in update.message.new_chat_members:
            mention = f"@{member.username}" if member.username else member.first_name
            keyboard = [
                [InlineKeyboardButton("Confirmo que he leído las reglas", callback_data='confirmado')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"✨ Las estrellas brillan para dar la bienvenida a {mention}. "
                "Los misterios de la noche te aguardan. 🌌✨ Sucumbe ante el morbo y tus deseos 😈\n\n"
                "🔹 **Reglas Básicas de Conducta:**\n"
                "1️⃣ Sé respetuoso con todos los miembros.\n"
                "2️⃣ Evita lenguaje ofensivo o inapropiado.\n"
                "3️⃣ No compartas spam o enlaces no solicitados.\n"
                "4️⃣ Participa de forma constructiva y amistosa.\n\n"
                "✨ **Por favor, preséntate**:\n"
                "👉 Dinos tu edad, dónde vives y comparte una foto o video presumiendo tus mejores nubes. ☁️📸🎥\n\n"
                "🔹 **Confirma que has leído todo** haciendo clic en el botón: ✅\n\n"
                "✨ ¡Disfruta tu estadía y explora los secretos de la noche! 🌙",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Error al dar la bienvenida a nuevos usuarios: {e}")

async def confirm_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja la confirmación de lectura de reglas al hacer clic en el botón."""
    try:
        query = update.callback_query
        if query.data == 'confirmado':
            await query.answer()
            await query.edit_message_text(
                text="¡Gracias por confirmar que has leído las reglas! 🎉 ¡Bienvenido/a a la familia!"
            )
        else:
            await query.answer()
            await query.edit_message_text(
                text="Por favor, confirma que has leído las reglas haciendo clic en el botón."
            )
    except Exception as e:
        logger.error(f"Error al manejar la confirmación de lectura: {e}")

def shutdown(signal, frame):
    """Maneja el apagado limpio del bot."""
    logger.info("Bot apagado.")
    sys.exit(0)

def main():
    """Inicia el bot."""
    signal.signal(signal.SIGINT, shutdown)
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CallbackQueryHandler(confirm_reading))

    app.run_polling()

if __name__ == "__main__":
    main()
