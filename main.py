import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("El token de la API no está configurado correctamente en el archivo .env.")

# Usuarios confirmados
confirmed_users = set()


# Función para manejar los botones
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()  # Confirma la interacción

    if query.data == "confirmado":
        if user_id not in confirmed_users:
            confirmed_users.add(user_id)
            chat_permissions = ChatPermissions(can_send_messages=True)
            await context.bot.restrict_chat_member(
                update.effective_chat.id, user_id, permissions=chat_permissions
            )
            await query.edit_message_text("¡Gracias por confirmar las reglas! 🎉")
        else:
            await query.edit_message_text("Ya confirmaste las reglas anteriormente. ¡Bienvenido! 🎉")
    elif query.data == "join_group":
        await query.edit_message_text(
    text=(
        "🔥 ¡Excelente decisión! Utiliza este enlace para unirte:\n"
        "¿Nos acompañas con unos fumes con Neumus? 😈\n\n"
        "https://bit.ly/neumuskink\n\n"
        "Meeting ID: 891 5220 5303\n"
        "Passcode: kink\n\n"
        "#zoomgay #gayzoom #fumesgay #morbo"
    ),
    parse_mode="Markdown",
)

    elif query.data == "decline_group":
        await query.edit_message_text("✨ No hay problema. Si cambias de opinión, usa /start.")


# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type != "private":
        return  # Ignorar si no es chat privado

    user_name = update.effective_user.first_name

    keyboard = [
        [
            InlineKeyboardButton("Sí, quiero unirme 😈", callback_data="join_group"),
            InlineKeyboardButton("No, gracias ❌", callback_data="decline_group"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"¡Bienvenido {user_name} a la Guarida de Neumus! 😈\n\n"
        "Aquí descubrirás un espacio para:\n"
        "😶‍🌫️ Divertirte sin límites\n"
        "😈 Disfrutar como nunca\n"
        "😏 Dejarte llevar y ser tú mismo\n\n"
        "¿Listo para vivir la experiencia? 🔥✨",
        reply_markup=reply_markup,
    )


# Función para dar la bienvenida en grupos
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        mention = f"@{member.username}" if member.username else member.first_name
        keyboard = [
            [InlineKeyboardButton("Confirmo que he leído las reglas ✅", callback_data="confirmado")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"✨ Bienvenido {mention}. Sucumbe ante el morbo y tus deseos 😈\n\n"
            "✨ **Por favor, preséntate**:\n"
            "👉 Dinos tu edad, dónde vives y comparte una foto o video presumiendo tus mejores nubes. ☁️📸🎥\n\n"
            "🔹 **Confirma que has leído todo** haciendo clic en el botón: ✅\n\n"
            "✨ ¡Disfruta tu estadía y explora los secretos de la noche! 🌙",
            reply_markup=reply_markup,
        )

        chat_permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(
            update.effective_chat.id, member.id, permissions=chat_permissions
        )


# Configurar y ejecutar el bot
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
