from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from .models import User,Task
from django.core.mail import send_mail,BadHeaderError
import random
from django.contrib.auth.hashers import make_password
from django.contrib import messages 
from django.contrib.auth import logout
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from taskapp.models import User,Task
from taskapp.serializers import UserSerializer,TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import re

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    #user/{userid}/tasks
    @action(detail=True,methods=['get'])
    def task(self,request,pk=None):
        try:
            user=User.objects.get(pk=pk)
            tasks=Task.objects.filter(user=user)
            task_serializer=TaskSerializer(tasks,many=True,context={'request':request})
            return Response(task_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message': 'User does not exists!! Error!!'
            })
        
class TaskViewSet(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    
def home(request):
    return render(request, 'home.html')
   

def login(request):
    if request.method == 'POST':
        email = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('taskList', user_id=user.id)
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'Invalid credentials. Please try again.'})
    return render(request, 'login.html')

def taskList(request, user_id):
    user_id_from_session = request.session.get('user_id')
    
    # Check if the user is accessing their own tasks
    if user_id_from_session and user_id_from_session == int(user_id):
        tasks = Task.objects.filter(user=user_id)
        context = {'tasks': tasks}
        return render(request, 'taskList.html', context)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')


def addTask(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        # Get the logged-in user instance
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # Handle the case where the user does not exist (e.g., redirect to login)
            return redirect('login')  # Adjust the URL name based on your login URL

        # Create a new task for the user
        Task.objects.create(
            user=user,
            title=title,
            description=description,
            date_created=timezone.now().date(),
            due_date=due_date,
            status=status
        )

        # Redirect to the task management page
        return redirect('taskList', user_id=user_id)

    return render(request, 'addTask.html')

def details(request, taskId):
    # Get the task object or return a 404 error if it doesn't exist
    task = get_object_or_404(Task, id=taskId)

    # You can customize the context based on what information you want to pass to the template
    context = {'task': task}

    # Render the task details template with the context
    return render(request, 'details.html', context)
    
def updateTask(request, taskId):
    task = get_object_or_404(Task, id=taskId)
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        # Update the task with the new data from the form
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.status = request.POST.get('status')

        # Save the updated task
        task.save()

        # Redirect to the task management page or any other page you prefer
        return redirect('taskList', user_id)

    # Render the update form with the current task data
    return render(request, 'updateTask.html', {'task': task, 'user_id': user_id})

def delTask(request, taskId):
    # Get the task to be deleted
    task = Task.objects.get(id=taskId)
    user_id = request.session.get('user_id')
    # Delete the task
    task.delete()

    # Redirect to the task management page after deletion
    return redirect('taskList', user_id)
 
def logoutUser(request):
    # Logout the user
    logout(request)

    # Redirect to the login page or any other desired page
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        # Get the form data from the request object
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Store the other fields to restore in case of validation failure
        other_fields = {'firstname': firstname, 'lastname': lastname, 'phone': phone}

        # Add validation for the email
        try:
            validate_email(email)
        except ValidationError:
            error_msg = "Please enter a valid email address."
            return render(request, 'signup.html', {'error_msg': error_msg, **other_fields})

        # Add validation for the password
        if not (len(password) >= 6 and any(char.isupper() for char in password) and
                any(char.islower() for char in password) and any(char.isdigit() for char in password) and
                any(char in "!@#$%^&*()-_+=<>,.?/:;{}[]~" for char in password)):
            error_msg = "Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return render(request, 'signup.html', {'error_msg': error_msg, **other_fields})

        # Insert the form data into the database using a model
        user = User(firstname=firstname, lastname=lastname, phone=phone, email=email, password=password)
        user.save()

        context = {
            'msg': "Thanks For Signing Up!! You can now Log In."
        }
        return render(request, 'signup.html', context)

    # Render the initial form
    return render(request, 'signup.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if user with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'There is no user with this email address.')
            return render(request, 'forgotPassword.html')
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        # Store OTP in session
        request.session['otp'] = otp
        request.session['email'] = email
        # Send OTP to user's email
        subject = 'OTP for password reset'
        message = f'Your OTP for password reset is {otp}. Do not share it with anyone.'
        from_email = "sia2121181@sicsr.ac.in"
        recipient_list = [email]
        print(subject," ",message," ",from_email," ",recipient_list)
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            print('Email sent successfully!')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        # Redirect to verify OTP view
        return redirect('verifyOtp')
    return render(request, 'forgotPassword.html')

def verifyOtp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            # OTP is valid, allow user to reset their password
            # Get user's email from session
            email = request.session.get('email')
            # Remove stored OTP and email from session
        
            # Redirect to reset password view
            messages.success(request, 'OTP verified. Please enter a new password.')
            return redirect('resetPassword')
        else:
            # OTP is invalid, show an error message
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verifyOtp.html')



def isValidPassword(password):
    # Check if the password has one uppercase, one lowercase, one digit, and one special character
    if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{6,}$', password):
        return True
    return False

def resetPassword(request):
    reset_success = False

    if request.method == 'POST':
        email = request.session.get('email')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif not isValidPassword(new_password):
            messages.error(request, 'Password must have one uppercase letter, one lowercase letter, one digit, one special character, and be at least 6 characters long.')
        else:
            try:
                # Get user with this email
                user = User.objects.get(email=email)

                # Set new password
                hashed_password = make_password(new_password)
                user.password = hashed_password
                user.save()

                # Authenticate and login user
                user = User.objects.get(email=email)

                if user:
                    reset_success = True
                    messages.success(request, 'Password reset successful. You can now login with your new password.')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User with the given email does not exist.')

    return render(request, 'resetPassword.html', {'reset_success': reset_success})