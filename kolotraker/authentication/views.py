import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
from django.contrib import auth
from django.shortcuts import redirect


class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        field_contents = {
            'field_values': request.POST
        }
        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Password must be 8 characters or more')
                    return render(request, 'authentication/register.html', field_contents)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account has been successfully created')
                return render(request, 'authentication/register.html')

        messages.success(request, 'Success')
        return render(request, 'authentication/login.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = str(data['username'])

        if not username.isalnum():
            return JsonResponse({'username_error': 'username should be alpahnumeric characters only'},
                                status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username has been taken'},
                                status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = str(data['email'])

        if not validate_email(email):
            return JsonResponse({'email_error': 'E-mail invalid'},
                                status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'E-mail has been taken'},
                                status=409)
        return JsonResponse({'email_valid': True})

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome, {user.get_username()} Login Successful')
                    return redirect('transactions')
            
            messages.error(request, 'You username or password is incorect')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please enter a username and password')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
