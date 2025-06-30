from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import BoatStatus, Vessel, SensorData, SystemStatus, VideoStream
from django.contrib.auth.models import User
from .serializers import BoatStatusSerializer
from django.shortcuts import render, get_object_or_404, redirect


def testPage(request):
    # ดึงค่าจาก GET
    boat_name = request.GET.get("boat_name", None)
    user = request.user  
    vessel_user = Vessel.objects.filter(owner=user)

    vessel = None
    boat_status = None
    all_vessels = Vessel.objects.all()

    # เช็คว่ามีชื่อเรือใน URL
    if boat_name != 'no_option':
        try:
            vessel = Vessel.objects.get(name=boat_name)
            boat_status = BoatStatus.objects.filter(vessel=vessel).order_by('-timestamp').first()
        except Vessel.DoesNotExist:
            vessel = None
            boat_status = None

    if request.method == "POST":
        battery = request.POST.get("battery")
        speed = request.POST.get("speed")
        mode = request.POST.get("mode")
        heading = request.POST.get("heading")
        status = request.POST.get("status")

    else:
        battery = speed = mode = heading = status = None

    context = {
        'vessel': vessel,
        'boat_status': boat_status,
        'battery': battery,
        'speed': speed,
        'mode': mode,
        'heading': heading,
        'status': status,
        'all_vessels': all_vessels,
        'vessel_user': vessel_user,
    }

    return render(request, 'api/testPage.html', context)


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
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "รายการเรือทั้งหมด",
            "total": len(serializer.data),
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "สร้างเรือใหม่สำเร็จ",
                "boat": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "เกิดข้อผิดพลาดในการสร้าง",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# GET(1) / PUT / PATCH / DELETE สำหรับ BoatStatus


class BoatDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoatStatus.objects.all()
    serializer_class = BoatStatusSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "message": f"ข้อมูลเรือ ID {instance.id}",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # เช็คว่าเป็น PATCH หรือ PUT
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "อัปเดตข้อมูลเรือสำเร็จ",
                "data": serializer.data
            })
        return Response({
            "message": "อัปเดตล้มเหลว",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        boat_name = instance.name
        instance.delete()
        return Response({
            "message": f"ลบเรือชื่อ: {boat_name} เรียบร้อยแล้ว"
        }, status=status.HTTP_204_NO_CONTENT)

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
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    return render(request, 'api/location.html', {'lat': lat, 'lon': lon})  # แสดงหน้า location.html


def get_status(request):
    context = {}
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')
        boat_name = request.POST.get('boat')

        if action == 'boat_status':
            boat_name = request.POST.get('boat')
            try:
                boat_status = BoatStatus.objects.get(name=boat_name)
                context['boat_status'] = boat_status
            except BoatStatus.DoesNotExist:
                error_message = "ไม่พบข้อมูลเรือที่คุณระบุ"
                context['error_message'] = error_message

        elif action == 'list_boats':
            list_boats = BoatStatus.objects.all()
            context['list_boats'] = list_boats

    return render(request, 'api/status.html', context)


def dashboard(request):
    return render(request, 'api/dashboard.html')  # แสดงหน้า dashboard.html
