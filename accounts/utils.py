import requests

# Bot ma'lumotlari
TOKEN = "8232486475:AAGg0AioUjsPd8prO4davvMkj0IEmapvp2o"
ADMIN_CHAT_ID = "236431306"

def send_admin_notification(user):
    """
    Superadminga yangi foydalanuvchi haqida to'liq ma'lumot yuboradi.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Tasdiqlash va Rad etish tugmalari
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Tasdiqlash", "callback_data": f"approve_{user.id}"},
            {"text": "❌ Rad etish", "callback_data": f"reject_{user.id}"}
        ]]
    }
    
    # Botda ko'rinadigan xabar matni (Emoji bilan bezatilgan)
    text = (
        f"🚀 **Yangi foydalanuvchi so'rovi!**\n\n"
        f"👤 **F.I.O:** {user.last_name} {user.first_name}\n"
        f"📞 **Tel:** {user.phone}\n"
        f"💼 **Lavozim:** {user.position}\n"
        f"🔑 **Login:** {user.username}\n"
        f"🆔 **ID:** {user.id}\n\n"
        f"Ushbu foydalanuvchiga tizimga kirishga ruxsat beramizmi?"
    )
    
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram yuborishda xatolik: {e}")
        return False