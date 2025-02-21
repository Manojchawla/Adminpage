from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import User
from .forms import UserForm

# Create a new user
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/create_user.html', {'form': form})

# List all users with search and pagination
def user_list(request):
    query = request.GET.get('q', '')  # Get search query from URL

    # Fetch users and apply search filter
    users = User.objects.all()
    if query:
        users = users.filter(name__icontains=query) | users.filter(email__icontains=query) | users.filter(phone_no__icontains=query)

    # Paginate results (10 users per page)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)

    return render(request, 'users/user_list.html', {'users': page_users, 'query': query})

# Update a user
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form})

# Delete a user
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/delete_user.html', {'user': user})
