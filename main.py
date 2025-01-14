from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os
import asyncio

# Carga el token desde el archivo
TOKEN = "8092436564:AAG0AsALo5K8RDX1h6Z4bFF_6l_70r01ktU"

# Inicializar Flask
app = Flask(__name__)

# Función de inicio del bot de Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manda un mensaje cuando se usa el comando /start."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Desde las sombras eternas, yo, Nix, saludo a {user_name}. "
        "Disfruta y sucumbe de los placeres y el morbo de mi noche. 😈✨🌙"
    )

# Función de bienvenida para nuevos miembros
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida a los nuevos usuarios que se unen al grupo."""
    for member in update.message.new_chat_members:
        if member.username:
            mention = f"@{member.username}"
        else:
            mention = member.first_name
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

# Función para manejar la confirmación de lectura de las reglas
async def confirm_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja la confirmación de lectura de reglas al hacer clic en el botón."""
    query = update.callback_query
    if query.data == 'confirmado':
        await query.answer()  # Acknowledge the callback query
        await query.edit_message_text(
            text="¡Gracias por confirmar que has leído las reglas! 🎉 ¡Bienvenido/a a la familia!"
        )
    else:
        await query.answer()
        await query.edit_message_text(
            text="Por favor, confirma que has leído las reglas haciendo clic en el botón."
        )

# Función para crear el servidor Flask (esto engañará a Render)
@app.route('/')
def index():
    return 'Bot is running...'

# Función principal para iniciar el bot
async def main():
    """Inicia el bot de Telegram y el servidor Flask."""
    app_telegram = ApplicationBuilder().token(TOKEN).build()

    # Agregar los manejadores de comandos y mensajes
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app_telegram.add_handler(CallbackQueryHandler(confirm_reading))

    # Iniciar el bot de Telegram en un hilo separado
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        app_telegram.run_polling(),
        run_flask()
    )

def run_flask():
    """Inicia el servidor Flask en el bucle de eventos actual"""
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == "__main__":
    asyncio.run(main())
