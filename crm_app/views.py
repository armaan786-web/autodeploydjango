import requests
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from .models import CustomUser, LoginLog, Employee, Agent, OutSourcingAgent, Admin
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from rest_framework import viewsets
import random
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from .whatsapp_api import send_whatsapp_message
from django.http import JsonResponse


def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return None


def agent_signup(request):
    if request.method == "POST":
        user_type = request.POST.get("type")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        password = request.POST.get("password")

        existing_agent = CustomUser.objects.filter(email=email)

        try:
            if existing_agent:
                messages.warning(request, f'"{email}" already exists.')
                return render(request, "Login/Signuppage.html")

            if user_type == "Outsourcing partner":
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="5",
                )

                user.outsourcingagent.type = user_type
                user.outsourcingagent.contact_no = contact_no

                user.save()
                messages.success(request, "OutsourceAgent Added Successfully")

                mobile = contact_no
                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )  # Custo
                response = send_whatsapp_message(mobile, message)
                if response.status_code == 200:
                    print("Request was successful!")
                    print("Response:", response.text)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    print("Response:", response.text)

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an Outsource Agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )  # Customize this message as needed

                # Change this to your email
                recipient_list = [email]  # List of recipient email addresses

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                request.session["username"] = email
                request.session["password"] = password

            else:
                user2 = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="4",
                )

                user2.agent.type = user_type
                user2.agent.contact_no = contact_no

                user2.save()

                messages.success(request, "Agent Added Successfully")

                mobile = contact_no
                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )  # Customize this message as needed

                response = send_whatsapp_message(mobile, message)
                if response.status_code == 200:
                    print("Request was successful!")
                    print("Response:", response.text)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    print("Response:", response.text)

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )  # Customize this message as needed

                # Change this to your email
                recipient_list = [email]  # List of recipient email addresses

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                request.session["username"] = email
                request.session["password"] = password

            # Send OTP via SMS for both user types
            random_number = random.randint(0, 999)
            send_otp = str(random_number).zfill(4)
            request.session["sendotp"] = send_otp

            if user_type == "4":
                contact_no = user2.agent.contact_no
            elif user_type == "5":
                contact_no = user.outsourcingagent.contact_no

            url = "http://sms.txly.in/vb/apikey.php"
            payload = {
                "apikey": "lbwUbocDLNFjenpa",
                "senderid": "SKTRAL",
                "templateid": "1007338024565017323",
                "number": contact_no,
                "message": f"Use this OTP {send_otp} to login to your theskytrails account",
            }
            response = requests.post(url, data=payload)

            return redirect("verify_otp")

        except Exception as e:
            # Handle exceptions if any
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "Login/Signuppage.html")


def verify_otp(request):
    if request.method == "POST":
        num1 = request.POST.get("num1")
        num2 = request.POST.get("num2")
        num3 = request.POST.get("num3")
        num4 = request.POST.get("num4")
        submitted_otp = num1 + num2 + num3 + num4

        username = request.session.get(
            "username", "Default value if key does not exist"
        )
        password = request.session.get(
            "password", "Default value if key does not exist"
        )
        sendotp = request.session.get("sendotp", "Default value if key does not exist")

        print("sendddd otp is:", sendotp)

        # submitted_otp = request.POST.get("submitted_otp")

        if submitted_otp == sendotp:
            user = authenticate(request, username=username, password=password)

            if user != None:
                login(request, user)
                user_type = user.user_type
                if user_type == "1":
                    return redirect("dashboard")
                if user_type == "2":
                    return redirect("travel_dashboards")
                if user_type == "3":
                    return redirect("employee_dashboard")
                if user_type == "4":
                    return redirect("agent_dashboard")
                if user_type == "5":
                    return redirect("agent_dashboard")

                public_ip = get_public_ip()
                LoginLog.objects.create(
                    user=user,
                    ip_address=public_ip if public_ip else None,
                    login_datetime=timezone.now(),
                    # date = timezone.now()
                )

        else:
            messages.error(request, "Wrong Otp")
            print("not success")

    return render(request, "Login/Otp.html")


def CustomLoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        request.session["username"] = username
        request.session["password"] = password

        try:
            user = CustomUser.objects.get(username=username)
            print("userrrr", user)

            if check_password(password, user.password):
                user_type = user.user_type

                if user_type == "1":
                    # If user_type is "1" (HOD), log in directly
                    user = authenticate(request, username=username, password=password)

                    if user is not None:
                        login(request, user)
                        return redirect("/crm/dashboard/")

                elif user_type in ("2", "3", "4", "5"):
                    public_ip = get_public_ip()
                    LoginLog.objects.create(
                        user=user,
                        ip_address=public_ip if public_ip else None,
                        login_datetime=timezone.now(),
                        # date = timezone.now()
                    )
                    # If user_type is "2" (Admin) or "3" (Employee), proceed with OTP verification
                    request.session["username"] = username
                    request.session["password"] = password
                    user_id = user.id
                    mob = ""
                    customeruser = CustomUser.objects.get(id=user_id)
                    user_type = customeruser.user_type
                    if user_type == "2":
                        print("helooooo")
                        mob = customeruser.admin.contact_no

                    if user_type == "3":
                        mob = customeruser.employee.contact_no

                    if user_type == "4":
                        mob = customeruser.agent.contact_no

                    if user_type == "5":
                        mob = customeruser.outsourcingagent.contact_no

                    random_number = random.randint(0, 999)
                    send_otp = str(random_number).zfill(4)
                    request.session["sendotp"] = send_otp
                    print("senddddd ot", send_otp)
                    url = "http://sms.txly.in/vb/apikey.php"
                    payload = {
                        "apikey": "lbwUbocDLNFjenpa",
                        "senderid": "SKTRAL",
                        "templateid": "1007338024565017323",
                        "number": mob,
                        "message": f"Use this OTP {send_otp} to login to your. theskytrails account",
                    }
                    response = requests.post(url, data=payload)

                    # send_otp_and_redirect(request, user_id, user_type)
                    # return redirect("verify_otp")
                    return redirect("verify_otp")
                else:
                    return HttpResponse("User type not supported")

            else:
                messages.error(request, "Username and Password Incorrect")
                return redirect("login")

        except CustomUser.DoesNotExist:
            messages.error(request, "User Does Not Exist")
            return redirect("login")
            # return HttpResponse("Username and Password Incorrect")

    return render(request, "Login/Login.html")


def resend_otp(request):
    username = request.session.get("username")
    password = request.session.get("password")
    print("kkkkkkkkkkk", username)

    if username and password:
        try:
            user = CustomUser.objects.get(username=username)

            # Verify the user's password
            if check_password(password, user.password):
                user_type = user.user_type

                # Rest of your logic for user types and sending OTP
                if user_type in ("2", "3", "4", "5"):
                    mob = ""

                    if user_type == "2":
                        mob = user.admin.contact_no
                    elif user_type == "3":
                        mob = user.employee.contact_no
                    elif user_type == "4":
                        mob = user.agent.contact_no
                    elif user_type == "5":
                        mob = user.outsourcingagent.contact_no

                    random_number = random.randint(0, 999)
                    send_otp = str(random_number).zfill(4)
                    request.session["sendotp"] = send_otp

                    url = "http://sms.txly.in/vb/apikey.php"
                    payload = {
                        "apikey": "lbwUbocDLNFjenpa",
                        "senderid": "SKTRAL",
                        "templateid": "1007338024565017323",
                        "number": mob,
                        "message": f"Use this OTP {send_otp} to login to your. theskytrails account",
                    }
                    print("New OTp ", send_otp)
                    response = requests.post(url, data=payload)
                    return redirect("verify_otp")

        except CustomUser.DoesNotExist:
            pass  # Handle the case where the user does not exist


def forgot_psw(request):
    if request.method == "POST":
        mob_no = request.POST.get("mob_no")
        user = None
        try:
            admin_profile = Admin.objects.get(contact_no=mob_no)
            user = admin_profile.users
            request.session["admin_profile"] = admin_profile.id

        except Admin.DoesNotExist:
            pass

        try:
            employee_profile = Employee.objects.get(contact_no=mob_no)
            user = employee_profile.users
        except Employee.DoesNotExist:
            pass

        try:
            agent_profile = Agent.objects.get(contact_no=mob_no)
            user = agent_profile.users
        except Agent.DoesNotExist:
            pass

        try:
            outsourceagent_profile = OutSourcingAgent.objects.get(contact_no=mob_no)
            user = outsourceagent_profile.users
        except OutSourcingAgent.DoesNotExist:
            pass

        if user is not None:
            request.session["user_id"] = user.id

            random_number = random.randint(0, 999)
            forgetsend_otp = str(random_number).zfill(4)
            request.session["forgotsendotp"] = forgetsend_otp

            url = "http://sms.txly.in/vb/apikey.php"
            payload = {
                "apikey": "lbwUbocDLNFjenpa",
                "senderid": "SKTRAL",
                "templateid": "1007338024565017323",
                "number": mob_no,
                "message": f"Use this OTP {forgetsend_otp} to login to your. theskytrails account",
            }
            response = requests.post(url, data=payload)

            return redirect("forget_otp")

        else:
            messages.error(request, "Mobile number does not match any user.")

    return render(request, "Login/forgot_psw.html")

    # return render(request, "Authentication/forgot_psw.html")


def forget_otp(request):
    sendotp = request.session.get(
        "forgotsendotp", "Default value if key does not exist"
    )
    print("sendd otp", sendotp)
    if request.method == "POST":
        num1 = request.POST.get("num1")
        num2 = request.POST.get("num2")
        num3 = request.POST.get("num3")
        num4 = request.POST.get("num4")
        submitted_otp = num1 + num2 + num3 + num4
        # submitted_otp = request.POST.get("submitted_otp")
        if submitted_otp == sendotp:
            return redirect("reset_psw")
        else:
            messages.error(request, "OTP not matched..")

    return render(request, "Login/Forgot_otp_verify.html")


def reset_psw(request):
    user_id = request.session.get("user_id", "Default value if key does not exist")

    if request.method == "POST":
        new_psw = request.POST.get("new_psw")
        confirm_psw = request.POST.get("confirm_psw")

        if new_psw == confirm_psw:
            user_instance = CustomUser.objects.get(id=user_id)

            try:
                # Use set_password to properly hash and save the password
                # print("Before setting password:", user_instance.password)
                user_instance.set_password(confirm_psw)
                # print("After setting password:", user_instance.password)
                user_instance.save()

                messages.success(request, "Password Reset Successfully....")

                return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        else:
            messages.error(request, "Password Not Match")

    return render(request, "Login/change_psw.html")
