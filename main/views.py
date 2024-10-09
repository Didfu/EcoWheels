from django.shortcuts import render,redirect
from datetime import date, datetime,timedelta

from authapp.models import UserProfile
from .models import TravelLog
from django.utils.dateparse import parse_duration
import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages

OLAMAPS_API = settings.OLAMAPS

@login_required(login_url='/login/')
def logtrip(request):
    user = request.user

    if request.method == 'POST':
        # Retrieve form data
        source_add = request.POST.get('source')
        dest_add = request.POST.get('destination')
        source_lat = request.POST.get('source_lat')
        source_lon = request.POST.get('source_lng')
        destination_lat = request.POST.get('dest_lat')
        destination_lon = request.POST.get('dest_lng')
        is_electric = request.POST.get('is_electric')
        mode_of_transport = request.POST.get('mode_of_transport')
        time_taken = request.POST.get('time_taken')
        date = request.POST.get('date')
        log_time = datetime.now().strftime('%H:%M:%S')

        # Debugging form input
        print(f"[DEBUG] Log Trip Form Data: Source={source_add}, Destination={dest_add}, Mode={mode_of_transport}")

        # If the vehicle is electric, adjust the mode of transport
        if is_electric == "yes":
            mode_of_transport = "e" + mode_of_transport

        # API request setup
        params = {
            'origin': f'{source_lat},{source_lon}',
            'destination': f'{destination_lat},{destination_lon}',
            'mode': 'driving',
            'alternatives': 'false',
            'steps': 'true',
            'overview': 'full',
            'language': 'en',
            'traffic_metadata': 'true',
            'api_key': OLAMAPS_API
        }

        # Make the API request
        try:
            response = requests.post('https://api.olamaps.io/routing/v1/directions', params=params)

            # Check if the API request was successful
            if response.status_code == 200:
                data = response.json()

                # Ensure the 'routes' key exists and has valid data
                if 'routes' in data and len(data['routes']) > 0:
                    legs = data['routes'][0]['legs']

                    total_distance = sum(leg['distance'] for leg in legs) / 1000  # Convert to km
                    total_duration_fetched = sum(leg['duration'] for leg in legs) / 60  # Convert to minutes

                    total_distance = round(total_distance, 2)
                    total_duration_fetched = round(total_duration_fetched, 2)

                    # Calculate carbon footprint
                    list_of_transport = {
    "bus": 68,          # Conventional bus
    "ebus": 10,        # Electric bus (estimated)
    "acbus": 80,       # AC bus
    "eacbus": 10,      # Electric AC bus (estimated)
    "train": 41,       # Conventional train
    "etrain": 10,      # Electric train (estimated)
    "actrain": 50,     # AC train
    "eactrain": 10,    # Electric AC train (estimated)
    "car1": 180,       # Car (1 passenger)
    "ecar1": 20,       # Electric car (1 passenger)
    "car2": 90,        # Car (2 passengers)
    "ecar2": 20,       # Electric car (2 passengers)
    "car3": 60,        # Car (3 passengers)
    "ecar3": 20,       # Electric car (3 passengers)
    "car4": 45,        # Car (4 passengers)
    "ecar4": 20,       # Electric car (4 passengers)
    "bike1": 50,        # Bicycle
    "ebike1": 20,       # Electric bicycle
    "bike2": 40,        # Bicycle (2 passengers)
    "ebike2": 20,       # Electric bicycle (2 passengers)
    "rickshaw1": 100,  # Rickshaw (1 passenger)
    "erickshaw1": 10,  # Electric rickshaw (1 passenger)
    "rickshaw2": 80,   # Rickshaw (2 passengers)
    "erickshaw2": 10,  # Electric rickshaw (2 passengers)
    "rickshaw3": 70,   # Rickshaw (3 passengers)
    "erickshaw3": 10,  # Electric rickshaw (3 passengers)
    "scooter1": 50,    # Scooter (1 passenger)
    "escooter1": 20,   # Electric scooter (1 passenger)
    "scooter2": 40,    # Scooter (2 passengers)
    "escooter2": 20,
    "walk":0,
    "bicycle":0          # Electric scooter (2 passengers)
}
                    if mode_of_transport not in list_of_transport:
                        messages.error(request, 'Invalid mode of transport selected.')
                        return redirect('logtrip')

                    carbonfootprint = list_of_transport[mode_of_transport] * total_distance
                    if total_duration_fetched < float(time_taken):
                        extra_time = float(time_taken) - total_duration_fetched
                        carbonfootprint_per_min = carbonfootprint / total_duration_fetched
                        extra_co2 = extra_time * carbonfootprint_per_min
                        carbonfootprint += extra_co2

                    carbonfootprint = round(carbonfootprint, 2)

                    # Save the trip data to the database
                    TravelLog.objects.create(
                        user=user,
                        source_address=source_add,
                        destination_address=dest_add,
                        source_latitude=source_lat,
                        source_longitude=source_lon,
                        destination_latitude=destination_lat,
                        destination_longitude=destination_lon,
                        distance=total_distance,
                        date=date,
                        time_taken=time_taken,
                        time_duration_fetched=str(total_duration_fetched),  # Save fetched duration
                        is_electric=is_electric == "yes",
                        mode_of_transport=mode_of_transport,
                        carbon_footprint=carbonfootprint,
                        log_time=log_time
                    )

                    # Check if this is the first trip of the day
                    today = timezone.now().date() 
                    print(f"[DEBUG] Today's Date: {today}")

                    existing_trips = TravelLog.objects.filter(user=user, date=today)
                    print(f"[DEBUG] Existing trips for today: {[trip.id for trip in existing_trips]}")
                    if existing_trips.count() == 1:
                        print("[DEBUG] No previous trips found for today, awarding coins.")
                        try:
                            user_profile = UserProfile.objects.get(user=user)
                            print(f"[DEBUG] Current Coins: {user_profile.coins}")
                            user_profile.coins += 50 
                            user_profile.save()
                            print(f"[DEBUG] New Coins after Award: {user_profile.coins}")
                            messages.success(request, 'You earned 50 coins for your first trip today!')
                        except UserProfile.DoesNotExist:
                            messages.error(request, 'User profile not found. Contact support.')
                            return redirect('logtrip')
                    else:
                        print("[DEBUG] Trip already logged for today.")
                        messages.success(request, 'Trip logged successfully!')

                else:
                    messages.error(request, 'Invalid data received from API.')
                    print(f"[DEBUG] API response error: {data}")

            else:
                messages.error(request, 'Error fetching data from API')
                print(f"[DEBUG] API Request failed with status code: {response.status_code}")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            print(f"[DEBUG] Error during API request: {str(e)}")

        return redirect('logtrip')

    travellog = TravelLog.objects.filter(user=user).order_by('date', '-log_time')

    context = {
        'travellog': travellog,
        'OLAMAPS_API': OLAMAPS_API
    }
    return render(request, 'main/logtrip.html', context)

def home(request):
    return render (request,'main/home.html')

def redeem(request):
    return render (request,'main/redeem.html')

def leaderboard(request):
    return render (request,'main/leaderboard.html')

def carpooling(request):
    return render (request,'main/carpooling.html')

def tips(request):
    return render (request,'main/tips.html')