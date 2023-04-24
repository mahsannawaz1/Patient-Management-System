from django.shortcuts import render, redirect
from .models import NewUser, Doctor, Patient, Disease

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

        if role == 'Doctor':

            degree = request.POST.get("degree")
            specialization = request.POST.get("specialization")

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
                    first_name=first_name, last_name=last_name, age=age, email=email, username=username, password=password1, is_patient=True)
                patient = Patient(doctor=doctor, user=user, mobile_phone=phone)
                disease = Disease(name=disease_name,
                                  stage=disease_stage, patient=patient)
                user.save()
                patient.save()
                disease.save()
                return redirect('home')
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

    doctors = Doctor.objects.all()
    docs = []
    for doctor in doctors:
        docs.append(f'{doctor.user.first_name} {doctor.user.last_name}')
    context['docs'] = docs
    context['role'] = role

    return render(request, 'accounts/signup.html', context)
