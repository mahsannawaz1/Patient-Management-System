from django.shortcuts import redirect, render
from .models import NewUser
from django.http import HttpResponse


def unauthenticatedUser(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            role = ""
            new_user = NewUser.objects.get(id=request.user.id)
            if new_user.is_admin and new_user.is_staff:
                role = "Admin"
                return redirect("dashboard", role)
            elif new_user.is_doctor:
                role = "Doctor"
                return redirect("dashboard", role)
            elif new_user.is_patient:
                role = "Patient"
                return redirect("dashboard", role)
            elif new_user.is_nurse:
                role = "Nurse"
                return redirect("dashboard", role)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowedUsers(allowedUsers):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            flag = _checkGroup(request, allowedUsers)
            if flag == 1:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "accounts/unauthorized.html")

        return wrapper

    return decorator


def updateUsers(allowedUsers):
    def decorator(view_func):
        def wrapper(request, user, *args, **kwargs):
            flag = _checkGroup(request, allowedUsers)
            new_user = NewUser.objects.get(id=request.user.id)
            if flag == 1:
                if new_user.is_admin and (
                    user == "Nurse" or user == "Patient" or user == "Doctor"
                ):
                    return view_func(request, user, *args, **kwargs)

                elif new_user.is_doctor and (user == "Doctor" or user == "Patient"):
                    return view_func(request, user, *args, **kwargs)

                elif new_user.is_nurse and (user == "Nurse"):
                    return view_func(request, *args, **kwargs)
                elif new_user.is_patient and (user == "Patient"):
                    return view_func(request, user, *args, **kwargs)
                else:
                    return render(request, "accounts/unauthorized.html")

            else:
                return render(request, "accounts/unauthorized.html")

        return wrapper

    return decorator


def deleteUsers(allowedUsers):
    def decorator(view_func):
        def wrapper(request, user, *args, **kwargs):
            flag = _checkGroup(request, allowedUsers)
            if flag == 1:
                if user == "Nurse" or user == "Admin" or user == "Doctor":
                    return render(request, "accounts/unauthorized.html")
                else:
                    return view_func(request, *args, **kwargs)
            else:
                return render(request, "accounts/unauthorized.html")

        return wrapper

    return decorator


def profileUsers(allowedUsers):
    def decorator(view_func):
        def wrapper(request, pk, role, *args, **kwargs):
            flag = _checkGroup(request, allowedUsers)
            new_user = NewUser.objects.get(id=request.user.id)
            if flag == 1:
                if new_user.is_admin and role == "Admin":
                    return view_func(request, pk, role, *args, **kwargs)

                elif new_user.is_doctor and role == "Doctor":
                    return view_func(request, pk, role, *args, **kwargs)

                elif new_user.is_nurse and role == "Nurse":
                    return view_func(request, *args, **kwargs)
                elif new_user.is_patient and role == "Patient":
                    return view_func(request, pk, role, *args, **kwargs)
                else:
                    return render(request, "accounts/unauthorized.html")

            else:
                return render(request, "accounts/unauthorized.html")

        return wrapper

    return decorator


def _checkGroup(request, allowedUsers):
    flag = 0
    if request.user.groups.exists():
        list_of_groups = request.user.groups.all()
        list_of_groups = list(list_of_groups)
        if list_of_groups:
            for group in list_of_groups:
                if group.name in allowedUsers:
                    flag = 1
                    break
                else:
                    flag = 0
    return flag
