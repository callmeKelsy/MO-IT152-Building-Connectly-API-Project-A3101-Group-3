# connectly_project/views.py
from django.shortcuts import render

def admin_view(request):
    return render(request, 'admin_view.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return render(request, 'protected_view.html')  # Render the template for the protected page
