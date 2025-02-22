from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import User
from .forms import UserForm

# Create a new user with validation
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone_no = form.cleaned_data.get('phone_no')

            # Validate email and phone number uniqueness
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
            elif User.objects.filter(phone_no=phone_no).exists():
                messages.error(request, "This phone number is already registered.")
            elif not phone_no.isdigit() or len(phone_no) != 10:
                messages.error(request, "Phone number must be exactly 10 digits.")
            else:
                form.save()
                messages.success(request, "User created successfully!")
                return redirect('user_list')
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
    else:
        form = UserForm()

    return render(request, 'users/create_user.html', {'form': form})

# List all users with search and pagination
def user_list(request):
    query = request.GET.get('q', '').strip()
    users = User.objects.all().order_by('-id')

    if query:
        users = users.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone_no__icontains=query)
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)

    return render(request, 'users/user_list.html', {'users': page_users, 'query': query})

# Update an existing user with validation
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone_no = form.cleaned_data.get('phone_no')

            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "This email is already registered.")
            elif User.objects.filter(phone_no=phone_no).exclude(id=user.id).exists():
                messages.error(request, "This phone number is already registered.")
            elif not phone_no.isdigit() or len(phone_no) != 10:
                messages.error(request, "Phone number must be exactly 10 digits.")
            else:
                form.save()
                messages.success(request, "User updated successfully!")
                return redirect('user_list')
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
    else:
        form = UserForm(instance=user)

    return render(request, 'users/update_user.html', {'form': form, 'user': user})

# Delete a user (Only via POST request for safety)
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('user_list')
    return render(request, 'users/delete_user.html', {'user': user})
