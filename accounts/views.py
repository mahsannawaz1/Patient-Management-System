from django.shortcuts import render, redirect, HttpResponse
from .models import (
    NewUser,
    Doctor,
    Patient,
    Disease,
    Nurse,
    Admin,
    Prescription,
    Medicine,
    Address,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


# Create your views here.


def home(request):
    context = {}
    if request.method == "POST":
        role = request.POST.get("role")

        return redirect("signup", role)
    return render(request, "accounts/home.html")


def signup(request, role):
    context = {}

    errors = []

    if request.method == "POST":
        names = NewUser.objects.all()
        names_of_users = []
        for name in names:
            names_of_users.append(f"{name.first_name} {name.last_name}")

        users = NewUser.objects.all().values("username")
        users = list(users)
        usernames = []
        for user in users:
            usernames.append(user["username"])
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

        if f"{first_name} {last_name}" in names_of_users:
            errors.append("First Name or Last Name is already in use")
        if username in usernames:
            errors.append("Username is already taken")
        if len(password1) < 8 or len(password2) < 8:
            errors.append("Password must be atleast 8 characters Long")
        if password1 != password2:
            errors.append("Password Does Not Match")
        if int(age) <= 0:
            errors.append("Age must be a Positive Integer")
        if not str(email).endswith("@gmail.com"):
            errors.append("Email Must end with @gmail.com")
        hashed_password = make_password(password1)

        if role == "Doctor":
            degree = request.POST.get("degree")
            specialization = request.POST.get("specialization")

            if not errors:
                user = NewUser(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    username=username,
                    password=hashed_password,
                    is_doctor=True,
                )
                doctor = Doctor(user=user, degree=degree, specialization=specialization)
                user.save()
                doctor.save()
                if request.user.is_authenticated and request.user.is_staff:
                    return redirect("dashboard", "Admin")
                return redirect("signin", role)
            else:
                context = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "degree": degree,
                    "email": email,
                    "specialization": specialization,
                    "age": age,
                    "username": username,
                    "role": role,
                }
                context["errors"] = errors

                return render(request, "accounts/signup.html", context)

        if role == "Patient":
            if request.user.is_authenticated and request.user.is_staff:
                doctor = request.POST.get("doctor")
                doctor = str(doctor).split()
                doctor = Doctor.objects.get(
                    user__first_name=doctor[0], user__last_name=doctor[1]
                )

            city = request.POST.get("address_city")
            state = request.POST.get("address_state")
            country = request.POST.get("address_country")
            house_address = request.POST.get("address")
            disease_name = request.POST.get("disease_name")
            disease_stage = request.POST.get("disease_stage")
            phone = request.POST.get("phone")

            if int(disease_stage) < 1 or int(disease_stage) > 5:
                errors.append("Enter Valid Disease Stage")
            if not errors:
                user = NewUser(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    username=username,
                    password=hashed_password,
                    is_patient=True,
                )
                address = Address(
                    city=city, state=state, country=country, house_address=house_address
                )
                new_user = NewUser.objects.get(id=request.user.id)
                if new_user.is_admin:
                    patient = Patient(
                        doctor=doctor, user=user, mobile_phone=phone, address=address
                    )
                elif new_user.is_doctor:
                    patient = Patient(
                        doctor=new_user.doctor,
                        user=user,
                        mobile_phone=phone,
                        address=address,
                    )
                disease = Disease(
                    name=disease_name, stage=disease_stage, patient=patient
                )
                user.save()
                patient.save()
                address.save()
                disease.save()
                if request.user.is_authenticated:
                    new_user = NewUser.objects.get(id=request.user.id)

                    if new_user.is_admin:
                        return redirect("dashboard", "Admin")
                    elif new_user.is_doctor:
                        return redirect("dashboard", "Doctor")
                else:
                    return redirect("signin", role)

            else:
                context = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "disease_name": disease_name,
                    "email": email,
                    "disease_stage": disease_stage,
                    "age": age,
                    "username": username,
                    "role": role,
                    "phone": phone,
                    "address_city": city,
                    "address_state": state,
                    "address_country": country,
                    "address": house_address,
                }
                context["errors"] = errors
                if user.is_authenticated:
                    new_user = NewUser.objects.get(id=request.user.id)
                    if new_user.is_admin:
                        doctors = Doctor.objects.all()
                        docs = []
                        for doctor in doctors:
                            docs.append(
                                f"{doctor.user.first_name} {doctor.user.last_name}"
                            )
                        context["docs"] = docs

                return render(request, "accounts/signup.html", context)

        if role == "Nurse":
            phone = request.POST.get("phone")
            if request.user.is_authenticated and request.user.is_staff:
                doctor = request.POST.get("doctor")
                doctor = str(doctor).split()
                doctor = Doctor.objects.get(
                    user__first_name=doctor[0], user__last_name=doctor[1]
                )

            if not errors:
                user = NewUser(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    username=username,
                    password=hashed_password,
                    is_nurse=True,
                )
                new_user = NewUser.objects.get(id=request.user.id)
                if new_user.is_admin:
                    nurse = Nurse(doctor=doctor, user=user, mobile_phone=phone)
                elif new_user.is_doctor:
                    nurse = Nurse(doctor=new_user.doctor, user=user, mobile_phone=phone)
                user.save()
                nurse.save()

                if request.user.is_authenticated:
                    new_user = NewUser.objects.get(id=request.user.id)

                    if new_user.is_admin:
                        return redirect("dashboard", "Admin")
                    elif new_user.is_doctor:
                        return redirect("dashboard", "Doctor")
                else:
                    return redirect("signin", role)
            else:
                context = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "age": age,
                    "username": username,
                    "role": role,
                    "phone": phone,
                }
                context["errors"] = errors
                doctors = Doctor.objects.all()
                docs = []
                for doctor in doctors:
                    docs.append(f"{doctor.user.first_name} {doctor.user.last_name}")
                    context["docs"] = docs

                return render(request, "accounts/signup.html", context)

        if role == "Admin":
            if not errors:
                user = NewUser(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    username=username,
                    password=hashed_password,
                    is_admin=True,
                    is_staff=True,
                )
                admin = Admin(user=user)
                user.save()
                admin.save()
                return redirect("signin", role)
            else:
                context = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "age": age,
                    "username": username,
                    "role": role,
                }
                context["errors"] = errors

                return render(request, "accounts/signup.html", context)

    doctors = Doctor.objects.all()
    docs = []
    for doctor in doctors:
        docs.append(f"{doctor.user.first_name} {doctor.user.last_name}")
    context["docs"] = docs

    context["role"] = role

    return render(request, "accounts/signup.html", context)


def signin(request, role):
    context = {"role": role}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard", role)
        else:
            context["username"] = username
            context["error"] = "Incorrect Username or Password"
            return render(request, "accounts/signin.html", context)

    return render(request, "accounts/signin.html", context)


def loggingout(request):
    logout(request)
    return redirect("/")


def dashboard(request, role):
    if role == "Admin":
        medicines = Medicine.objects.all()
        doctors = Doctor.objects.all()
        nurses = Nurse.objects.all()
        patients = Patient.objects.all()
        context = {
            "role": role,
            "medicines": list(medicines),
            "doctors": list(doctors),
            "nurses": list(nurses),
            "patients": list(patients),
        }
    if role == "Doctor":
        medicines = Medicine.objects.all()
        doctor = Doctor.objects.get(user=request.user)
        nurses = Nurse.objects.filter(doctor=doctor)
        patients = Patient.objects.filter(doctor=doctor)
        context = {
            "medicines": list(medicines),
            "doctor": doctor,
            "role": role,
            "nurses": list(nurses),
            "patients": list(patients),
        }
    if role == "Nurse":
        medicines = Medicine.objects.all()
        nurse = Nurse.objects.get(user=request.user)
        doctor = Doctor.objects.get(nurse=nurse)
        patients = Patient.objects.filter(doctor=doctor)
        context = {
            "medicines": list(medicines),
            "doctor": doctor,
            "role": role,
            "patients": list(patients),
        }
    if role == "Patient":
        patient = Patient.objects.get(user=request.user)
        doctor = Doctor.objects.get(patient=patient)
        prescriptions = Prescription.objects.filter(patient=patient)
        context = {
            "prescriptions": list(prescriptions),
            "patient": patient,
            "role": role,
            "doctor": doctor,
        }
    return render(request, "accounts/dashboard.html", context)


def delete(request, user, pk, role):
    if role == "Admin" and user == "Doctor":
        User = NewUser.objects.get(id=pk)

    if (role == "Admin" or role == "Doctor") and user == "Patient":
        User = NewUser.objects.get(id=pk)
    if (role == "Admin" or role == "Doctor") and user == "Nurse":
        User = NewUser.objects.get(id=pk)
    context = {"role": role, "user_role": user, "User": User}
    if request.method == "POST":
        User.delete()
        return redirect("dashboard", role)

    return render(request, "accounts/delete.html", context)


def update(request, user, pk, role):
    errors = []
    docs = Doctor.objects.all()

    if role == "Admin" and user == "Doctor":
        User = Doctor.objects.get(id=pk)

    if (role == "Admin" or role == "Doctor") and user == "Patient":
        User = Patient.objects.get(id=pk)

    if (role == "Admin" or role == "Doctor") and user == "Nurse":
        User = Nurse.objects.get(id=pk)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        age = request.POST.get("age")
        email = request.POST.get("email")

        if user == "Doctor":
            degree = request.POST.get("degree")
            specialization = request.POST.get("specialization")
            newuser = NewUser.objects.get(doctor__id=pk)
            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.username = username
            newuser.email = email
            newuser.age = age
            User.degree = degree
            User.specialization = specialization
            newuser.save()
            User.save()

        if user == "Patient":
            disease_name = request.POST.get("disease_name")
            disease_stage = request.POST.get("disease_stage")
            phone = request.POST.get("phone")
            doctor = request.POST.get("doctor")
            doctor = str(doctor)

            doctor = Doctor.objects.get(patient__id=pk)
            newuser = NewUser.objects.get(patient__id=pk)
            disease = Disease.objects.get(patient__id=pk)

            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.username = username
            newuser.email = email
            newuser.age = age

            disease.name = disease_name
            disease.stage = disease_stage

            User.mobile_phone = phone
            User.disease = disease
            User.doctor = doctor

            disease.save()
            newuser.save()
            User.save()

        if user == "Nurse":
            phone = request.POST.get("phone")
            doctor = request.POST.get("doctor")
            doctor = str(doctor)

            doctor = Doctor.objects.get(nurse__id=pk)
            newuser = NewUser.objects.get(nurse__id=pk)

            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.username = username
            newuser.email = email
            newuser.age = age

            User.mobile_phone = phone
            User.doctor = doctor

            newuser.save()
            User.save()

        if request.user.is_authenticated:
            return redirect("dashboard", user)
        elif request.user.is_staff and request.user.is_authenticated:
            return redirect("dashboard", "Admin")

    context = {
        "role": role,
        "user_role": user,
        "User": User,
        "docs": list(docs),
        "pk": pk,
    }

    return render(request, "accounts/update.html", context)


def addPrescription(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        doc = Doctor.objects.get(id=pk)
    elif request.user.is_authenticated and not request.user.is_staff:
        new_user = NewUser.objects.get(id=pk)
        doc = Doctor.objects.get(user=new_user)
    num_of_meds = 3
    errors = []
    patients = Patient.objects.filter(doctor=doc)
    context = {"patients": list(patients), "num": range(1, num_of_meds + 1)}

    if request.method == "POST":
        description = request.POST.get("description")
        patient = request.POST.get("patient")
        patient = str(patient)
        pat = Patient.objects.get(user__username=patient)

        medicines = []

        for i in range(1, num_of_meds + 1):
            medicine_name = request.POST.get(f"medicine_name_{i}")
            medicine_dose = request.POST.get(f"medicine_dose_{i}")
            medicine_manufacturer = request.POST.get(f"medicine_manufacturer_{i}")

            if medicine_name and medicine_dose and medicine_manufacturer:
                medicine = Medicine(
                    name=medicine_name,
                    dose=medicine_dose,
                    manufacturer=medicine_manufacturer,
                )
                medicine.save()
                medicines.append(medicine)
        if medicines:
            prescription = Prescription.objects.create(
                patient=pat, doctor=doc, description=description
            )
            if len(medicines) == 1:
                prescription.medicines.add(medicines[0])
            elif len(medicines) == 2:
                prescription.medicines.add(medicines[0], medicines[1])
            else:
                prescription.medicines.add(medicines[0], medicines[1], medicines[2])

            if request.user.is_authenticated and request.user.is_staff:
                return redirect("dashboard", "Admin")
            elif request.user.is_authenticated and not request.user.is_staff:
                return redirect("dashboard", "Doctor")

        else:
            errors.append(" Please Add atleast 1 Medicine")
            context["errors"] = errors
            return render(request, "accounts/add_prescription.html", context)

    return render(request, "accounts/add_prescription.html", context)


def addMedicine(request, role):
    num_of_meds = 3
    errors = []
    context = {"num": range(1, num_of_meds + 1)}
    if request.method == "POST":
        medicines = []
        for i in range(1, num_of_meds + 1):
            medicine_name = request.POST.get(f"medicine_name_{i}")
            medicine_dose = request.POST.get(f"medicine_dose_{i}")
            medicine_manufacturer = request.POST.get(f"medicine_manufacturer_{i}")

            if medicine_name and medicine_dose and medicine_manufacturer:
                medicine = Medicine.objects.create(
                    name=medicine_name,
                    dose=medicine_dose,
                    manufacturer=medicine_manufacturer,
                )

                medicines.append(medicine)
            elif (
                medicine_name is ""
                and medicine_dose is ""
                and medicine_manufacturer is ""
            ):
                pass
            elif (
                medicine_name is ""
                or medicine_dose is ""
                or medicine_manufacturer is ""
            ):
                errors.append(f"Please Fill out every field for Medicine {i}")

        if medicines:
            for medicine in medicines:
                medicine.save()
            return redirect("dashboard", role)
        else:
            errors.append("Please Add atlease 1 Medicine")

            context["errors"] = errors

            return render(request, "accounts/add_medicine.html", context)

    return render(request, "accounts/add_medicine.html", context)


def updateMedicine(request, role, pk):
    errors = []
    medicine = Medicine.objects.get(id=pk)
    context = {}
    context["medicine_name"] = medicine.name
    context["medicine_dose"] = medicine.dose
    context["medicine_manufacturer"] = medicine.manufacturer
    if request.method == "POST":
        medicine_name = request.POST.get("medicine_name")
        medicine_dose = request.POST.get("medicine_dose")
        medicine_manufacturer = request.POST.get("medicine_manufacturer")
        if medicine_name and medicine_dose and medicine_manufacturer:
            medicine.name = medicine_name
            medicine.dose = medicine_dose
            medicine.manufacturer = medicine_manufacturer
            medicine.save()
            return redirect("dashboard", role)

        elif medicine_name is "" or medicine_dose is "" or medicine_manufacturer is "":
            errors.append("Please Fill out all fields")

        if errors:
            context["errors"] = errors
            context["medicine_name"] = medicine_name
            context["medicine_dost"] = medicine_dose
            context["medicine_manufacturer"] = medicine_manufacturer
            return render(request, "accounts/add_medicine.html", context)

    return render(request, "accounts/update_medicine.html", context)


def deleteMedicine(request, role, pk):
    medicine = Medicine.objects.get(id=pk)
    context = {"medicine": medicine, "role": role}
    if request.method == "POST":
        medicine.delete()
        return redirect("dashboard", role)
    return render(request, "accounts/delete_medicine.html", context)


def showProfile(request, pk, role):
    newuser = NewUser.objects.get(id=pk)
    if role == "Admin":
        user = Admin.objects.get(user=newuser)
    elif role == "Doctor":
        user = Doctor.objects.get(user=newuser)
    elif role == "Patient":
        user = Patient.objects.get(user=newuser)
    elif role == "Nurse":
        user = Nurse.objects.get(user=newuser)
    context = {"role": role, "user": user}
    return render(request, "accounts/profile.html", context)
