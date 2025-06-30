from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, permissions
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import BoatStatus
from .serializers import BoatStatusSerializer


class YourModelView(APIView):
    # GET request สำหรับดึงข้อมูลทั้งหมดจาก BoatStatus
    def get(self, request, *args, **kwargs):
        data = BoatStatus.objects.all()
        serializer = BoatStatusSerializer(data, many=True)
        return Response(serializer.data)  # ส่งข้อมูลแบบ JSON กลับไป

    # POST request สำหรับสร้างข้อมูลใหม่
    def post(self, request, *args, **kwargs):
        serializer = BoatStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # ส่งข้อมูลที่สร้างสำเร็จกลับไป
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)  # ถ้าข้อมูลไม่ถูกต้อง

# GET(ALL) / POST สำหรับ BoatStatus
class BoatListCreate(generics.ListCreateAPIView):
    queryset = BoatStatus.objects.all()
    serializer_class = BoatStatusSerializer
    
    # Authenticate this view
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]  # Allow any user to access this view

# GET(1) / PUT / PATCH / DELETE สำหรับ BoatStatus
class BoatDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoatStatus.objects.all()
    serializer_class = BoatStatusSerializer
    
    # Authenticate this view
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]  # Allow any user to access this view
    

# แยกออกจาก API ให้แต่ละฟังก์ชันแสดงหน้า HTML ได้อย่างถูกต้อง


def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # ตรวจสอบว่ารหัสผ่านตรงกันหรือไม่
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # ตรวจสอบว่า email ถูกใช้ไปแล้วหรือยัง
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('signup')

        # สร้างผู้ใช้ใหม่และทำการ hash password
        user = User(username=username, email=email)
        user.set_password(password)  # <-- ทำให้รหัสผ่านถูก hash
        user.save()

        messages.success(request, "Sign up successful. You can now login.")
        return redirect('login')  # ไปหน้า login หลังสมัครเสร็จ

    return render(request, 'api/signUp.html')  # แสดงหน้า signUp.html


def login(request):
    if request.method == 'POST':
        # 1. รับค่าจากฟอร์ม
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 2. ตรวจสอบข้อมูลผู้ใช้
        # :contentReference[oaicite:1]{index=1}
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 3. สร้าง session ให้ผู้ใช้
            auth_login(request, user)  # :contentReference[oaicite:2]{index=2}
            # :contentReference[oaicite:3]{index=3}
            messages.success(request, f'Welcome back, {user.username}!')
            # 4. เปลี่ยนเส้นทางไปหน้าโปรไฟล์ (URL name “profile”)
            return redirect('profile')  # :contentReference[oaicite:4]{index=4}
        else:
            # 5. กรณีข้อมูลไม่ถูกต้อง
            # :contentReference[oaicite:5]{index=5}
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    # GET request: แสดงฟอร์ม login
    return render(request, 'api/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # ส่งอีเมลรีเซ็ตรหัสผ่าน (สามารถแก้ไขรายละเอียดการส่งอีเมลได้)
            send_mail(
                'Password Reset Request',
                'Click on the link below to reset your password:\n\n http://yourdomain.com/reset-password/{user.id}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(
                request, "Password reset link has been sent to your email.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')
    # แสดงหน้า forgotPassword.html
    return render(request, 'forgotPassword.html')


# :contentReference[oaicite:10]{index=10}
@login_required
def profile(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    return render(request, 'api/profile.html', {'user': request.user})


def home(request):
    return render(request, 'api/home.html')  # แสดงหน้า home.html


def about(request):
    return render(request, 'api/about.html')  # แสดงหน้า about.html


@login_required
def location(request):
    return render(request, 'api/location.html')  # แสดงหน้า location.html


@login_required
def get_status(request):
    boat_status = None
    list_boats = None
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')
        boat_name = request.POST.get('boat')
        
        if action == 'get_status':
            boat_name = request.POST.get('boat')
            try:
                boat_status = BoatStatus.objects.get(name=boat_name)
            except BoatStatus.DoesNotExist:
                error_message = "ไม่พบข้อมูลเรือที่คุณระบุ"
                boat_status = None

        elif action == 'list_boats':
            list_boats = BoatStatus.objects.all()

    return render(request, 'api/status.html', {
        'boat_status': boat_status,
        'list_boats': list_boats,
        'error_message': error_message,
    })

