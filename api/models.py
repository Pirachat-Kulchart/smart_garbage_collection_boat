from django.db import models
from django.contrib.auth.models import User


class BoatStatus(models.Model):
    name = models.CharField(
        max_length=50,  # กำหนดขีดจำกัดความยาวของชื่อเรือ
        unique=True,     # ป้องกันไม่ให้ชื่อซ้ำ
        default="Boat",
        verbose_name="name of the boat"
    )
    lat = models.FloatField(default=0.00, verbose_name="latitude")  # lat
    lon = models.FloatField(default=0.00, verbose_name="longitude")  # lon
    mode = models.TextField(max_length=35, default="idle",
                            verbose_name="mode")  # idle, auto, manual
    speed = models.IntegerField(default=0, verbose_name="speed")  # m/h
    heading = models.IntegerField(
        default=0, verbose_name="direction")  # degree
    battery = models.IntegerField(
        default=0, verbose_name="battery")  # percentage
    source = models.TextField(
        max_length=50, default="system", verbose_name="source")  # system, user, auto
    # message display to user
    message = models.TextField(
        default="Default Settings", verbose_name="message")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="timestamp")
    # status of the boat (True/False)
    status = models.BooleanField(default=None, verbose_name="status")

    def __str__(self):
        return f"[{self.timestamp}] name:{self.name} | mode: {self.mode} | battery: {self.battery} | message: {self.message} | location: ({self.lat}, {self.lon})"

    class Meta:
        verbose_name = "BoatStatus"
        verbose_name_plural = "BoatStatus"


class Profile(models.Model):
    # :contentReference[oaicite:0]{index=0}
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    # :contentReference[oaicite:1]{index=1}
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg'  # รูปนี้จะใช้ถ้ายังไม่อัปโหลด
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
