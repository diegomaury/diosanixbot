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

# Carga el token desde el archivo
TOKEN = "8092436564:AAG0AsALo5K8RDX1h6Z4bFF_6l_70r01ktU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manda un mensaje cuando se usa el comando /start."""
    user_name = update.effective_user.first_name  # Obtiene el nombre del usuario que usa el comando
    await update.message.reply_text(
        f"Desde las sombras eternas, yo, Nix, saludo a {user_name}. "
        "Disfruta y sucumbe de los placeres y el morbo de mi noche. 😈✨🌙"
    )

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida a los nuevos usuarios que se unen al grupo."""
    for member in update.message.new_chat_members:
        # Si el usuario tiene username, lo usamos para mencionarlo; de lo contrario, usamos su nombre.
        if member.username:
            mention = f"@{member.username}"
        else:
            mention = member.first_name

        # Crear un botón de confirmación
        keyboard = [
            [InlineKeyboardButton("Confirmo que he leído las reglas", callback_data='confirmado')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar mensaje de bienvenida con las reglas y el botón de confirmación
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

async def confirm_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja la confirmación de lectura de reglas al hacer clic en el botón."""
    query = update.callback_query
    # Asegúrate de que solo sea una respuesta de 'confirmado'
    if query.data == 'confirmado':
        await query.answer()  # Acknowledge the callback query
        await query.edit_message_text(
            text="¡Gracias por confirmar que has leído las reglas! 🎉 ¡Bienvenido/a a la familia!"
        )
    else:
        await query.answer()  # Si la respuesta no es válida, no pasa nada
        await query.edit_message_text(
            text="Por favor, confirma que has leído las reglas haciendo clic en el botón."
        )

def main():
    """Inicia el bot."""
    # Construye la aplicación
    app = ApplicationBuilder().token(TOKEN).build()

    # Agrega el comando /start
    app.add_handler(CommandHandler("start", start))

    # Agrega un manejador para nuevos miembros
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Agrega el manejador de callback_query
    app.add_handler(CallbackQueryHandler(confirm_reading))

    # Inicia el bot
    app.run_polling()

if __name__ == "__main__":
    main()
