from django.http import HttpResponse
from firebase_admin import credentials
from firebase_admin import db
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def logout_view(request):
    logout(request)
    # Redirect to the login page after logout
    return redirect('login') 


@login_required
def bin_view(request):
    # Fetch data from Firebase
    ref = db.reference('bin')
    bins_data = ref.get()
    print(bins_data)
    # Prepare data for rendering
    bins = []
    if bins_data:
        for bin_id, bin_info in bins_data.items():
            fill_level = bin_info.get('level', 0)
            status = ''
            if fill_level > 85 and fill_level < 95:
                status = 'Critical'
            elif fill_level > 95:
                status = 'Full'
            bin_dict = {
                'id': bin_id,
                'name': bin_info.get('Name', ''),
                'type': bin_info.get('type', ''),  # Ensure 'type' is correctly extracted
                'fill_level': fill_level,
                'status': status
            }
            bins.append(bin_dict)
            print("Fill level:", bin_dict['fill_level'])
    return render(request, 'smartbin/bin_view.html', {'bins': bins})


def create_bin(request):
    if request.method == 'POST':
        # Extract data from the POST request
        bin_id = request.POST.get('bin_id')
        name = request.POST.get('name')
        bin_type = request.POST.get('bin_type')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        level = request.POST.get('level')
        is_open = 0
        weight = 0

        # Create a dictionary with bin data
        bin_data = {
            'Name': name,
            'type': bin_type,
            'latitude': latitude,
            'longitude': longitude,
            'level': level,
            'IsOpen': is_open,
            'weight': weight
        }

        # Add the new bin data to the Realtime Database
        ref=db.reference(f'bin/{bin_id}')
        ref.set(bin_data)
        print(bin_data)

        # Redirect to a success page or back to the form
        return redirect('binview')
    else:
        return HttpResponse("No data received.")