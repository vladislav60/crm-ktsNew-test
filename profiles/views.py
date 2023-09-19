from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm, AvatarForm
from .models import *


# @login_required
# def edit_profile(request):
#     # profile = request.user.profile
#     if request.method == 'POST':
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('edit_profile')
#     else:
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'edit_profile.html', {'profile_form': profile_form})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('edit_profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'profile_form': profile_form})





