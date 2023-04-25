from django.shortcuts import render, redirect
from .models import NewUser, Doctor, Patient, Disease, Nurse, Admin
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
# Create your views here.


def home(request):

    context = {}
    if request.method == 'POST':
        role = request.POST.get("role")

        print('Role:', role)

        return redirect('signup', role)
    return render(request, 'accounts/home.html')


def signup(request, role):
    context = {}

    errors = []

    if request.method == 'POST':
        names = NewUser.objects.all()
        names_of_users = []
        for name in names:
            names_of_users.append(
                f'{name.first_name} {name.last_name}')

        users = NewUser.objects.all().values('username')
        users = list(users)
        usernames = []
        for user in users:
            usernames.append(user['username'])
        role = request.POST.get("role")
        first_name = request.POST.get("first_name")
        first_name = str(first_name).strip()
        last_name = request.POST.get("last_name")
        last_name = str(last_name).strip()
        username = request.POST.get("username")
        age = request.POST.get("age")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if f'{first_name} {last_name}' in names_of_users:
            errors.append('First Name or Last Name is already in use')
        if username in usernames:
            errors.append('Username is already taken')
        if len(password1) < 8 or len(password2) < 8:
            errors.append('Password must be atleast 8 characters Long')
        if password1 != password2:
            errors.append('Password Does Not Match')
        if int(age) <= 0:
            errors.append('Age must be a Positive Integer')
        if not str(email).endswith('@gmail.com'):
            errors.append('Email Must end with @gmail.com')
        hashed_password = make_password(password1)
        if role == 'Doctor':

            degree = request.POST.get("degree")
            specialization = request.POST.get("specialization")

            if not errors:

                user = NewUser(
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=hashed_password, is_doctor=True)
                doctor = Doctor(
                    user=user, degree=degree, specialization=specialization)
                user.save()
                doctor.save()
                if request.user.is_authenticated and request.user.is_staff:
                    return redirect('dashboard', 'Admin')
                return redirect('signin', role)
            else:
                context = {'first_name': first_name, 'last_name': last_name, 'degree': degree,
                           'email': email, 'specialization': specialization, 'age': age, 'username': username, "role": role}
                context['errors'] = errors

                return render(request, 'accounts/signup.html', context)

        if role == 'Patient':
            disease_name = request.POST.get("disease_name")
            disease_stage = request.POST.get("disease_stage")
            phone = request.POST.get("phone")
            doctor = request.POST.get("doctor")
            doctor = str(doctor).split()
            doctor = Doctor.objects.get(
                user__first_name=doctor[0], user__last_name=doctor[1])

            if int(disease_stage) < 1 or int(disease_stage) > 5:
                errors.append('Enter Valid Disease Stage')
            if not errors:

                user = NewUser(
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=hashed_password, is_patient=True)
                patient = Patient(doctor=doctor, user=user, mobile_phone=phone)
                disease = Disease(name=disease_name,
                                  stage=disease_stage, patient=patient)
                user.save()
                patient.save()
                disease.save()
                if request.user.is_authenticated and request.user.is_staff:
                    return redirect('dashboard', 'Admin')
                return redirect('signin', role)

            else:
                context = {'first_name': first_name, 'last_name': last_name, 'disease_name': disease_name,
                           'email': email, 'disease_stage': disease_stage, 'age': age, 'username': username, "role": role, 'phone': phone}
                context['errors'] = errors
                doctors = Doctor.objects.all()
                docs = []
                for doctor in doctors:
                    docs.append(
                        f'{doctor.user.first_name} {doctor.user.last_name}')
                    context['docs'] = docs

                return render(request, 'accounts/signup.html', context)

        if role == 'Nurse':

            phone = request.POST.get("phone")
            doctor = request.POST.get("doctor")
            doctor = str(doctor).split()
            doctor = Doctor.objects.get(
                user__first_name=doctor[0], user__last_name=doctor[1])

            if not errors:
                user = NewUser(
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=hashed_password, is_nurse=True)

                nurse = Nurse(doctor=doctor, user=user, mobile_phone=phone)
                user.save()
                nurse.save()
                if request.user.is_authenticated and request.user.is_staff:
                    return redirect('dashboard', 'Admin')
                return redirect('signin', role)
            else:
                context = {'first_name': first_name, 'last_name': last_name,
                           'email': email, 'age': age, 'username': username, "role": role, 'phone': phone}
                context['errors'] = errors
                doctors = Doctor.objects.all()
                docs = []
                for doctor in doctors:
                    docs.append(
                        f'{doctor.user.first_name} {doctor.user.last_name}')
                    context['docs'] = docs

                return render(request, 'accounts/signup.html', context)

        if role == 'Admin':
            if not errors:
                user = NewUser(
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=hashed_password, is_admin=True, is_staff=True)
                admin = Admin(
                    user=user)
                user.save()
                admin.save()
                return redirect('signin', role)
            else:
                context = {'first_name': first_name, 'last_name': last_name,
                           'email': email, 'age': age, 'username': username, "role": role}
                context['errors'] = errors

                return render(request, 'accounts/signup.html', context)

    doctors = Doctor.objects.all()
    docs = []
    for doctor in doctors:
        docs.append(f'{doctor.user.first_name} {doctor.user.last_name}')
    context['docs'] = docs
    context['role'] = role

    return render(request, 'accounts/signup.html', context)


def signin(request, role):
    context = {
        'role': role
    }

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard", role)
        else:
            context['username'] = username
            context['error'] = 'Incorrect Username or Password'
            return render(request, 'accounts/signin.html', context)

    return render(request, 'accounts/signin.html', context)


def dashboard(request, role):
    if role == 'Admin':
        doctors = Doctor.objects.all()
        nurses = Nurse.objects.all()
        patients = Patient.objects.all()

        context = {
            'role': role,
            'doctors': list(doctors),
            'nurses': list(nurses),
            'patients': list(patients)
        }

    return render(request, 'accounts/dashboard.html', context)


def delete(request, user, pk, role):
    print(role)
    print(user)
    if role == 'Admin' and user == 'Doctor':
        User = Doctor.objects.get(id=pk)
    if role == 'Admin' and user == 'Patient':
        User = Patient.objects.get(id=pk)
    if role == 'Admin' and user == 'Nurse':
        User = Nurse.objects.get(id=pk)
    context = {
        "role": role,
        "user_role": user,
        "User": User

    }
    if request.method == 'POST':
        User.delete()
        return redirect('dashboard', role)

    return render(request, 'accounts/delete.html', context)
