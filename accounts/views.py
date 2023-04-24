from django.shortcuts import render, redirect
from .models import NewUser, Doctor
from django.contrib.auth import authenticate
# Create your views here.


def home(request):
    context = {}
    if request.method == 'POST':
        role = request.POST.get("role")
        print('Role:', role)
        context = {
            'role': role
        }
        return render(request, 'accounts/signup.html', context)
    return render(request, 'accounts/home.html')


def signup(request):
    errors = []
    users = NewUser.objects.all().values('username')
    users = list(users)
    usernames = []
    for user in users:
        usernames.append(user['username'])

    if request.method == 'POST':

        role = request.POST.get("role")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        age = request.POST.get("age")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if role == 'Doctor':
            degree = request.POST.get("degree")
            specialization = request.POST.get("specialization")
            if username in usernames:
                errors.append('Username is already in use')
            if len(password1) < 8 or len(password2) < 8:
                errors.append('Password must be atleast 8 characters Long')
            if password1 != password2:
                errors.append('Password Does Not Match')
            if int(age) <= 0:
                errors.append('Age must be a Positive Integer')
            if not str(email).endswith('@gmail.com'):
                errors.append('Email Must end with @gmail.com')

            if not errors:

                user = NewUser(
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=password1, is_doctor=True)
                doctor = Doctor(
                    user=user, degree=degree, specialization=specialization)
                user.save()
                doctor.save()
                return redirect('home')
            else:
                context = {'first_name': first_name, 'last_name': last_name, 'degree': degree,
                           'email': email, 'specialization': specialization, 'age': age, 'username': username, "role": role}
                context['errors'] = errors

                return render(request, 'accounts/signup.html', context)
    return render(request, 'accounts/signup.html')
