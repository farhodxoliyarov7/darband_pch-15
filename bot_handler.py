import os
import django
import asyncio
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes

# 1. Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

# Bot tokenini bu yerda saqlang
TOKEN = "8232486475:AAGg0AioUjsPd8prO4davvMkj0IEmapvp2o"

# 2. Bazadagi amallarni bajaruvchi sinxron funksiya
@sync_to_async
def process_user_action(user_id, action):
    try:
        user = User.objects.get(id=user_id)
        
        if action == "approve":
            user.is_approved = True
            user.save()
            return {
                "status": "approved",
                "text": (
                    f"✅ **TASDIQLANDI**\n\n"
                    f"👤 F.I.O: {user.last_name} {user.first_name}\n"
                    f"🔑 Login: {user.username}\n"
                    f"💼 Lavozimi: {user.position}\n"
                    f"📞 Tel: {user.phone}\n\n"
                    f"📅 Holat: Tizimga kirishga ruxsat berildi."
                )
            }
        
        elif action == "reject":
            username = user.username
            user.delete()
            return {
                "status": "rejected",
                "text": f"❌ **RAD ETILDI**\n\nFoydalanuvchi ({username}) so'rovi bazadan o'chirib tashlandi."
            }
            
    except User.DoesNotExist:
        return {"status": "error", "text": "⚠️ Xato: Foydalanuvchi topilmadi yoki allaqachon o'chirilgan."}
    except Exception as e:
        return {"status": "error", "text": f"⚠️ Xatolik: {str(e)}"}

# 3. Asosiy tugma handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Callback ma'lumotlarini ajratib olish
    try:
        data = query.data
        if "_" not in data:
            return
            
        action, user_id = data.split('_')
        
        # Bazadagi amalni bajarish
        result = await process_user_action(user_id, action)
        
        # Admin xabarini yangilash
        await query.edit_message_text(text=result["text"], parse_mode="Markdown")
        
    except Exception as e:
        print(f"Handler error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("---------------------------------------")
    print("🚀 PCH-15 Bot Handler muvaffaqiyatli ishga tushdi")
    print("📡 Admin tasdiqlari kutilmoqda...")
    print("---------------------------------------")
    app.run_polling()