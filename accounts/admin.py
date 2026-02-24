from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Station

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Mavjud ustunlar saqlandi
    list_display = ('username', 'last_name', 'first_name', 'position', 'is_approved', 'is_staff')
    list_editable = ('is_approved',)
    search_fields = ('username', 'last_name', 'first_name')
    list_filter = ('is_approved', 'position', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('phone', 'position', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('phone', 'position', 'is_approved')}),
    )

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """Bekatlarni barcha texnik ma'lumotlari bilan boshqarish"""
    
    # Ro'yxatda ko'rinadigan ustunlar
    list_display = ('name', 'region', 'manager_name', 'manager_phone', 'total_tracks')
    # Bekat nomi va hududi bo'yicha qidirish
    search_fields = ('name', 'region', 'manager_name')
    # Hudud bo'yicha filtrlash
    list_filter = ('region',)

    # Ma'lumotlarni tahrirlash oynasida guruhlarga ajratish (Fieldsets)
    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('name', 'region', ('latitude', 'longitude'))
        }),
        ("Mas'ul xodim", {
            'fields': (('manager_name', 'manager_phone'),)
        }),
        ("Yo'llar haqida texnik ma'lumotlar", {
            'description': "Bekatdagi mavjud yo'llarning texnik ko'rsatkichlari",
            'fields': (
                'total_tracks', 
                ('main_tracks', 'receiving_sending_tracks', 'dead_end_tracks'),
                'total_track_length'
            )
        }),
        ("Strelka va moslamalar", {
            'fields': (
                'switches_count', 
                ('switch_type_1_9', 'switch_type_1_11'),
                'insulating_joints'
            )
        }),
        ("Qo'shimcha", {
            'fields': ('description',)
        }),
    )