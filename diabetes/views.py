import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Patient

# Register User
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User registered successfully'})

# Login User and get JWT tokens
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

# Protected Route
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return JsonResponse({'message': f'Hello {request.user.username}, you accessed a protected route!'})

# MariaDB Database Read/Update
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mariadb_data(request):
    with connection.cursor() as cursor:
        if request.method == 'GET':
            cursor.execute("SELECT id, username FROM auth_user")
            rows = cursor.fetchall()
            return JsonResponse({'data': rows})
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            cursor.execute("UPDATE my_table SET value=%s WHERE id=%s", [data['value'], data['id']])
            return JsonResponse({'message': 'Record updated'})



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patients(request):
    if request.method == 'GET':
        patients = list(Patient.objects.values())  # Fetch all patients
        return JsonResponse({'patients': patients})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        patient = Patient.objects.create(
            name=data['name'],
            age=data['age'],
            diabetes_type=data['diabetes_type']
        )
        return JsonResponse({'message': 'Patient added successfully', 'id': patient.id})
