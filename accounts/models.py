from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Foydalanuvchi ma'lumotlari
    first_name = models.CharField(max_length=150, verbose_name="Ismingiz")
    last_name = models.CharField(max_length=150, verbose_name="Familiyangiz")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami", blank=True, null=True)
    position = models.CharField(max_length=100, verbose_name="Lavozimi", blank=True, null=True)
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.username})"

class Station(models.Model):
    # 1. Umumiy ma'lumotlar
    name = models.CharField(max_length=100, verbose_name="Bekat nomi")
    region = models.CharField(max_length=150, verbose_name="Hududiy joylashuvi")
    latitude = models.FloatField(verbose_name="Kenglik (Lat)")
    longitude = models.FloatField(verbose_name="Uzunlik (Long)")
    
    # 2. Mas'ul xodimlar
    manager_name = models.CharField(max_length=150, verbose_name="Mas'ul F.I.O")
    manager_phone = models.CharField(max_length=25, verbose_name="Mas'ul tel raqami")

    # 3. Yo'llar haqida texnik ma'lumotlar
    total_tracks = models.IntegerField(default=0, verbose_name="Yo'llar soni (jami)")
    main_tracks = models.IntegerField(default=0, verbose_name="Shundan asosiy yo'llar")
    receiving_sending_tracks = models.IntegerField(default=0, verbose_name="Qabul-jo'natish yo'llari")
    dead_end_tracks = models.IntegerField(default=0, verbose_name="Tupik yo'llar")
    total_track_length = models.FloatField(default=0.0, verbose_name="Jami masofa (metr)")

    # 4. Strelka va uskunalar
    switches_count = models.IntegerField(default=0, verbose_name="Strelkalar soni")
    switch_type_1_9 = models.IntegerField(default=0, verbose_name="1/9 turi")
    switch_type_1_11 = models.IntegerField(default=0, verbose_name="1/11 turi")
    insulating_joints = models.IntegerField(default=0, verbose_name="Izostiklar soni")

    description = models.TextField(blank=True, verbose_name="Qo'shimcha izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bekat"
        verbose_name_plural = "Bekatlar"

    def __str__(self):
        return self.name