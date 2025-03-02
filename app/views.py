from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def send_order_to_admins(context: CallbackContext, user, location):
    keyboard = [[InlineKeyboardButton("✅ Buyurtma olindi", callback_data=f"order_taken:{user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"🚖 **Yangi Buyurtma** 🚖\n\n"
    message += f"🛣 Yo'nalish: {user.direction}\n"
    message += f"📞 Telefon: {user.phone}\n"
    message += f"👥 Yo'lovchilar: {user.passengers} ({user.gender})"

    admin_message = await context.bot.send_location(chat_id='admin_chat_id', latitude=location.latitude, longitude=location.longitude)
    context.user_data['order_message_id'] = admin_message.message_id

    await context.bot.send_message(chat_id='admin_chat_id', text=message, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("order_taken"):
        user_id = data.split(":")[1]
        if 'taken_by' in context.bot_data and context.bot_data['taken_by'] == user_id:
            return

        context.bot_data['taken_by'] = user_id
        keyboard = [[InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_order:{user_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"✅ Buyurtma olindi: {query.from_user.first_name}"

        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif data.startswith("cancel_order"):
        user_id = data.split(":")[1]
        if str(query.from_user.id) == user_id:
            await query.edit_message_text(text="🚖 **Yangi Buyurtma** 🚖\n\n🛣 Yo'nalish: {user.direction}\n📞 Telefon: {user.phone}\n👥 Yo'lovchilar: {user.passengers} ({user.gender})")
            del context.bot_data['taken_by']
        else:
            await query.answer("Siz bu buyurtmani bekor qila olmaysiz")

async def error_handler(update: object, context: CallbackContext) -> None:
    print(f"Update {update} caused error {context.error}")
