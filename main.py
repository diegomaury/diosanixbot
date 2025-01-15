from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,  # Correct filters import
)
import os
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener el token de la variable de entorno
TOKEN = os.getenv("TOKEN")

# Verifica si el token fue cargado correctamente
if not TOKEN:
    raise ValueError("El token de la API no está configurado correctamente en el archivo .env.")

confirmed_users = set()  # Usar un conjunto para almacenar IDs de usuarios confirmados

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manda un mensaje cuando se usa el comando /start en chat privado."""
    if update.effective_chat.type != "private":
        return  # Ignora el comando si no es un chat privado

    user_name = update.effective_user.first_name  # Obtiene el nombre del usuario que usa el comando

    # Crear botones para la respuesta
    keyboard = [
        [
            InlineKeyboardButton("Sí, quiero unirme 😈", callback_data='join_group'),
            InlineKeyboardButton("No, gracias ❌", callback_data='decline_group')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar el mensaje con los botones
    await update.message.reply_text(
        f"Soy la Diosa primordial de la noche, Nyx, bienvenido {user_name}. "
        "Disfruta y sucumbe de los placeres y el morbo de mi oscuridad. 😈✨🌙\n\n"
        "¿Te gustaría acceder a mi grupo privado?",
        reply_markup=reply_markup
    )

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía el mensaje con las reglas cuando se usa el comando /reglas."""
    reglas_texto = (
        "🔹 **Reglas Básicas de Conducta:**\n"
        "1️⃣ Sé respetuoso con todos los miembros.\n"
        "2️⃣ Evita lenguaje ofensivo o inapropiado.\n"
        "3️⃣ No compartas spam o enlaces no solicitados.\n"
        "4️⃣ Participa de forma constructiva y amistosa.\n\n"
    )

    # Envía las reglas como un mensaje
    await update.message.reply_text(reglas_texto)

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
            [InlineKeyboardButton("Confirmo que he leído las reglas ✅", callback_data='confirmado')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar mensaje de bienvenida con las reglas y el botón de confirmación
        await update.message.reply_text(
            f"✨ Bienvenido a mi noche {mention}. "
            "Sucumbe ante el morbo y tus deseos 😈\n\n"
            "✨ **Por favor, preséntate**:\n"
            "👉 Dinos tu edad, dónde vives y comparte una foto o video presumiendo tus mejores nubes. ☁️📸🎥\n\n"
            "🔹 **Confirma que has leído todo** haciendo clic en el botón: ✅\n\n"
            "✨ ¡Disfruta tu estadía y explora los secretos de la noche! 🌙",
            reply_markup=reply_markup
        )

        # Bloquea al nuevo usuario hasta que confirme las reglas
        chat_permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            member.id,
            permissions=chat_permissions
        )

async def confirm_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja las respuestas de los botones."""
    query = update.callback_query
    user_id = update.effective_user.id

    if query.data == 'confirmado':
        if user_id not in confirmed_users:
            confirmed_users.add(user_id)
            # Libera al usuario para enviar mensajes
            chat_permissions = ChatPermissions(can_send_messages=True)
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                user_id,
                permissions=chat_permissions
            )
            await query.edit_message_text(
                text="¡Gracias por confirmar que has leído las reglas! 🎉 ¡Perverso!😈"
            )
        else:
            await query.edit_message_text(
                text="Ya has confirmado que has leído las reglas. ¡Bienvenido de nuevo!"
            )
    elif query.data == 'join_group':
        await query.edit_message_text(
            text="🔥 ¡Excelente decisión! Utiliza el siguiente enlace para acceder y no olvides dejarte pervertir: "
                 "[Únete al grupo privado aquí](https://t.me/+G-zJhLhJCxU2Nzgx)",
            parse_mode="Markdown"
        )
    elif query.data == 'decline_group':
        await query.edit_message_text(
            text="✨ No hay problema. Si cambias de opinión, siempre puedes usar el comando /start nuevamente."
        )

def main():
    """Inicia el bot."""
    try:
        # Construye la aplicación
        app = ApplicationBuilder().token(TOKEN).build()

        # Agrega el comando /start solo para chats privados
        app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))

        # Agrega el comando /reglas
        app.add_handler(CommandHandler("reglas", reglas))

        # Agrega un manejador para nuevos miembros con el filtro adecuado
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

        # Agrega el manejador de callback_query
        app.add_handler(CallbackQueryHandler(confirm_reading))

        # Inicia el bot
        app.run_polling()

    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

if __name__ == "__main__":
    main()
