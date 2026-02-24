import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Station
from .utils import send_admin_notification

# --- BOT SOZLAMALARI ---
# utils.py dagi TOKEN bilan bir xil ekanligiga ishonch hosil qiling
BOT_TOKEN = "8232486475:AAGg0AioUjsPd8pr04davvMkj0IEmapvp2o"

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        ph = request.POST.get('phone')
        pos = request.POST.get('position') 
        
        if not all([u, p, f, l, pos]):
            messages.error(request, "Barcha maydonlarni to'ldirish shart!")
            return redirect('register')

        try:
            if User.objects.filter(username=u).exists():
                messages.error(request, "Ushbu login band, boshqa tanlang.")
                return redirect('register')
                
            new_user = User.objects.create_user(
                username=u, 
                password=p, 
                first_name=f, 
                last_name=l, 
                phone=ph, 
                position=pos, 
                is_approved=False
            )
            # Admin botiga xabar yuborish
            send_admin_notification(new_user)
            messages.success(request, "Ro'yxatdan o'tdingiz! Admin tasdiqlashini kiting.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")
            return redirect('register')

    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_approved:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Hisobingiz Superadmin tomonidan tasdiqlanmagan!")
        else:
            messages.error(request, "Login yoki parol xato!")
            
    return render(request, 'login.html')

@login_required
def home_view(request):
    if not request.user.is_approved:
        logout(request)
        messages.error(request, "Hisobingiz tasdiqlanmagan!")
        return redirect('login')

    stations = Station.objects.all()
    stations_data = []
    for s in stations:
        stations_data.append({
            "name": s.name,
            "region": s.region,
            "lat": s.latitude,
            "lng": s.longitude,
            "manager": s.manager_name,
            "phone": s.manager_phone,
            "total_tracks": s.total_tracks,
            "main_tracks": s.main_tracks,
            "rec_send_tracks": s.receiving_sending_tracks,
            "dead_tracks": s.dead_end_tracks,
            "track_len": s.total_track_length,
            "switches": s.switches_count,
            "type_1_9": s.switch_type_1_9,
            "type_1_11": s.switch_type_1_11,
            "izostik": s.insulating_joints,
            "desc": s.description
        })
    
    context = {
        'stations_json': json.dumps(stations_data)
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        
        if new_username != user.username and User.objects.filter(username=new_username).exists():
            messages.error(request, "Bu login allaqachon band!")
            return redirect('home')

        user.username = new_username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.position = request.POST.get('position')
        user.save()
        
        messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
    return redirect('home')

# --- TELEGRAM WEBHOOK (Tugmalar ishlashi uchun) ---
@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body)
            
            if 'callback_query' in update:
                callback_query = update['callback_query']
                data = callback_query['data']  # Masalan: 'approve_2'
                chat_id = callback_query['message']['chat']['id']
                message_id = callback_query['message']['message_id']
                original_text = callback_query['message']['text']

                action, user_id = data.split('_')
                user = User.objects.filter(id=user_id).first()

                if user:
                    if action == 'approve':
                        user.is_approved = True
                        user.save()
                        status_msg = f"✅ {user.get_full_name()} tasdiqlandi!"
                    elif action == 'reject':
                        user.delete()
                        status_msg = f"❌ {user_id}-ID dagi so'rov rad etildi."
                else:
                    status_msg = "⚠️ Xatolik: Foydalanuvchi topilmadi."

                # Telegramdagi xabarni tahrirlash (tugmalarni olib tashlash)
                edit_url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
                requests.post(edit_url, json={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": f"{original_text}\n\n📝 **Natija:** {status_msg}",
                    "parse_mode": "Markdown"
                })

            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
            
    return HttpResponse("Method not allowed", status=405)