import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Diagnosis
from .services import predict_diabetes  # Import the business logic function

User = get_user_model()  # Use the custom user model

# Register User
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        terms_accepted = data.get('termsAccepted')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # creates user
        User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            terms_accepted=terms_accepted
        )

        return JsonResponse({'message': 'User registered successfully'})

# Login User and get JWT tokens
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def diagnoses(request):
    if request.method == 'GET':
        # Fetch only diagnoses that belong to the authenticated user
        diagnosis_list = list(Diagnosis.objects.filter(user=request.user).values())  
        return JsonResponse({'Diagnosis': diagnosis_list})
    
    elif request.method == 'POST':
        data = json.loads(request.body)

        # Extract input data
        pregancies = data.get('pregancies', 0)
        glucose = data.get('glucose', 0.0)
        blood_pressure = data.get('blood_pressure', 0.0)
        skin_thickness = data.get('skin_thickness', 0.0)
        insulin = data.get('insulin', 0.0)
        bmi = data.get('bmi', 0.0)
        diabetes_pedigree_function = data.get('diabetes_pedigree_function', 0.0)
        age = data.get('age', 0)

    
        prediction_value = predict_diabetes(pregancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age)
        has_diabetes = prediction_value > 0.5

        diagnosis = Diagnosis.objects.create(
            user=request.user,
            pregancies=pregancies,
            glucose=glucose,
            blood_pressure=blood_pressure,
            skin_thickness=skin_thickness,
            insulin=insulin,
            bmi=bmi,
            diabetes_pedigree_function=diabetes_pedigree_function,
            age=age,
            has_diabetes=has_diabetes
        )

        return JsonResponse({
            'message': 'Diagnosis added successfully',
            'id': diagnosis.id,
            'prediction': prediction_value,
            'has_diabetes': has_diabetes
        })
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        diagnosis_id = data.get('id')
        
        try:
            # Ensure the user can only delete their own diagnoses
            diagnosis = Diagnosis.objects.get(id=diagnosis_id, user=request.user)
            diagnosis.delete()
            return JsonResponse({'message': 'Diagnosis deleted successfully', 'diagnosis_id': diagnosis_id})
        except Diagnosis.DoesNotExist:
            return JsonResponse({'error': 'Diagnosis not found or unauthorized'}, status=404)