from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

# Retrieve All Users (GET)
def get_users(request):
    try:
        users = list(User.objects.values('id', 'username', 'email', 'created_at'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create a User (POST)
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Ensure username and email are provided
            if 'username' not in data or 'email' not in data:
                return JsonResponse({'error': 'Username and email are required'}, status=400)

            # Check if the username or email already exists
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            user = User.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Update a User (PUT)
@csrf_exempt
def update_user(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')

            # Ensure at least one field (email or username) is provided
            if not email and not username:
                return JsonResponse({'error': 'At least email or username must be provided'}, status=400)

            # Get the user to update
            user = User.objects.filter(id=id).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Update the user fields if present
            if email:
                user.email = email
            if username:
                user.username = username
            user.save()

            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Delete a User (DELETE)
@csrf_exempt
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            user = User.objects.filter(id=id).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
