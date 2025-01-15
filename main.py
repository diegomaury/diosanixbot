from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

# Carga el token desde el archivo
TOKEN = "8092436564:AAESiYr_8K-fJ8nligTZTfwd1tZ8c1vy5Ng"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manda un mensaje cuando se usa el comando /start."""
    user_name = update.effective_user.first_name  # Obtiene el nombre del usuario que usa el comando

    # Crear botones para la respuesta
    keyboard = [
        [
            InlineKeyboardButton("Sí, quiero unirme 🌌", callback_data='join_group'),
            InlineKeyboardButton("No, gracias ❌", callback_data='decline_group')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar el mensaje con los botones
    await update.message.reply_text(
        f"Desde las sombras eternas, yo, Nix, saludo a {user_name}. "
        "Disfruta y sucumbe de los placeres y el morbo de mi noche. 😈✨🌙\n\n"
        "¿Te gustaría acceder a nuestro grupo privado?",
        reply_markup=reply_markup
    )

async def confirm_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja las respuestas de los botones."""
    query = update.callback_query
    user_id = update.effective_user.id

    if query.data == 'join_group':
        await query.edit_message_text(
            text="🌟 ¡Genial! Aquí está el enlace a nuestro grupo privado: "
                 "[Únete al grupo privado aquí](https://t.me/+bW_7SxYwTb5mYzQ5)",
            parse_mode="Markdown"
        )
    elif query.data == 'decline_group':
        await query.edit_message_text(
            text="✨ No hay problema. Si cambias de opinión, siempre puedes usar el comando /start nuevamente."
        )

def main():
    """Inicia el bot."""
    # Construye la aplicación
    app = ApplicationBuilder().token(TOKEN).build()

    # Agrega el comando /start
    app.add_handler(CommandHandler("start", start))

    # Agrega el manejador de callback_query
    app.add_handler(CallbackQueryHandler(confirm_reading))

    # Inicia el bot
    app.run_polling()

if __name__ == "__main__":
    main()
