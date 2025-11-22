from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

# ✅ Always get the correct user model dynamically
User = get_user_model()


# -------------------------------
# Register new users
# -------------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validation checks
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            # ✅ Create user using your custom user model
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")

    return render(request, "users/register.html")


# -------------------------------
# Login existing users
# -------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("chat_page")  # Redirect to chatbot after login
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "users/login.html")


# -------------------------------
# Logout
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect("login")
