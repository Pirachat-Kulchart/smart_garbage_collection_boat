from django.db import models
from django.contrib.auth.models import User


MODE_CHOICES = [
    ('idle', 'Idle'),
    ('manual', 'Manual'),
    ('auto', 'Autonomous'),
]


class Vessel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BoatStatus(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    lat = models.FloatField(default=0.0, verbose_name="latitude")
    lon = models.FloatField(default=0.0, verbose_name="longitude")
    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default='idle'
    )  # idle, auto, manual
    speed = models.FloatField(default=0.0, verbose_name="speed")  # m/h
    heading = models.FloatField(default=0.0, verbose_name="heading")  # degree
    battery = models.IntegerField(
        default=0, verbose_name="battery")  # percentage
    source = models.CharField(
        max_length=50, default="system", verbose_name="source")  # system, user, auto
    message = models.TextField(
        default="Default Settings", verbose_name="message")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="timestamp")
    status = models.BooleanField(default=False, verbose_name="status")

    def __str__(self):
        return f"[{self.timestamp}] {self.vessel.name} | mode: {self.mode} | battery: {self.battery}% | location: ({self.lat}, {self.lon})"

    class Meta:
        verbose_name = "BoatStatus"
        verbose_name_plural = "BoatStatus"
        ordering = ['-timestamp']


class SensorData(models.Model):
    vessel = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, related_name='sensor_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    gps_lat = models.FloatField()
    gps_lng = models.FloatField()
    speed = models.FloatField()
    heading = models.FloatField()
    imu_pitch = models.FloatField(null=True, blank=True)
    imu_roll = models.FloatField(null=True, blank=True)
    imu_yaw = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    battery_voltage = models.FloatField(null=True, blank=True)
    battery_current = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Sensor data {self.vessel.name} at {self.timestamp}"


class SystemStatus(models.Model):
    vessel = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, related_name='system_status')
    timestamp = models.DateTimeField(auto_now_add=True)
    controller_status = models.CharField(max_length=50, default='MANUAL')
    is_emergency_stop = models.BooleanField(default=False)
    motor_left_speed = models.FloatField(default=0.0)
    motor_right_speed = models.FloatField(default=0.0)

    def __str__(self):
        return f"System status {self.vessel.name} at {self.timestamp}"


class VideoStream(models.Model):
    vessel = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, related_name='video_streams')
    timestamp = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=255, blank=True)  # หรือ URL สตรีม
    # [{"label":..., "confidence":...}]
    detected_objects = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Video stream {self.vessel.name} at {self.timestamp}"


class PathLog(models.Model):
    vessel = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, related_name='path_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    path_points = models.JSONField()  # [{"lat":..., "lng":...}, ...]
    method_used = models.CharField(max_length=50, default='manual')

    def __str__(self):
        return f"PathLog {self.vessel.name} at {self.timestamp}"


class ErrorLog(models.Model):
    vessel = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, related_name='error_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    error_code = models.CharField(max_length=100)
    error_message = models.TextField()

    def __str__(self):
        return f"Error {self.error_code} at {self.timestamp} for {self.vessel.name}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"
