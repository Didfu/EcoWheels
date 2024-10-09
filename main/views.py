from django.shortcuts import render,redirect
from datetime import date, datetime,timedelta
from django.utils.safestring import mark_safe
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
from django.db.models import F,Sum
import plotly.graph_objects as go

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
    "bus": 50,          # Conventional bus
    "ebus": 10,        # Electric bus (estimated)
    "acbus": 80,       # AC bus
    "eacbus": 10,      # Electric AC bus (estimated)
    "train": 41,       # Conventional train
    "etrain": 10,      # Electric train (estimated)
    "actrain": 50,     # AC train
    "eactrain": 10,    # Electric AC train (estimated)
    "car1": 128,       # Car (1 passenger)
    "ecar1": 20,       # Electric car (1 passenger)
    "car2": 64,        # Car (2 passengers)
    "ecar2": 20,       # Electric car (2 passengers)
    "car3": 48,        # Car (3 passengers)
    "ecar3": 20,       # Electric car (3 passengers)
    "car4": 32,        # Car (4 passengers)
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

    travellog = TravelLog.objects.filter(user=user).order_by('-date', '-log_time')

    context = {
        'travellog': travellog,
        'OLAMAPS_API': OLAMAPS_API
    }
    return render(request, 'main/logtrip.html', context)


@login_required(login_url='/login/')
def home(request):
    user = request.user
    today = datetime.now().date()

    # Adjust week start and end dates for a week starting on Sunday and ending on Saturday
    start_of_week = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
    end_of_week = start_of_week + timedelta(days=6)

    # Query to get the total distance and carbon footprint for each mode of transport this week
    data = TravelLog.objects.filter(user=user, date__range=[start_of_week, end_of_week]) \
        .values('mode_of_transport') \
        .annotate(total_distance=Sum('distance'), total_carbon_footprint=Sum('carbon_footprint'))

    # Check if there is any data
    if not data:
        message = "No data available for this week. Please log your trips to see graphs."
        return render(request, 'main/home.html', {'message': message})

    # Calculate the overall total distance and total carbon footprint
    total_distance = sum(item['total_distance'] for item in data)
    total_carbon_footprint = sum(item['total_carbon_footprint'] for item in data)

    # Round the total values to two decimal places
    total_distance = round(total_distance, 2)
    total_carbon_footprint = round(total_carbon_footprint, 2)

    # Prepare data for pie charts
    modes_of_transport = [item['mode_of_transport'] for item in data]
    total_distances = [round(item['total_distance'], 2) for item in data]
    total_carbon_footprints = [round(item['total_carbon_footprint'], 2) for item in data]

    # Set colors for each mode of transport to ensure consistency between the two charts
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]

    # Create the distance pie chart
    distance_pie = go.Figure(data=[go.Pie(
        labels=modes_of_transport,
        values=total_distances,
        marker=dict(colors=colors),
        textinfo='label+percent',  # Show labels and percentages
        showlegend=True
    )])
    distance_pie.update_layout(
        title={
            'text': "Distance (km)",
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.0,
            'yanchor': 'top',
            'font': {
                'size': 16,
                'color': '#00563B'
            }
        },
        margin=dict(t=40, b=0, l=0, r=0),
        height=400,
        width=400
    )

    # Create the carbon footprint pie chart
    carbon_footprint_pie = go.Figure(data=[go.Pie(
        labels=modes_of_transport,
        values=total_carbon_footprints,
        marker=dict(colors=colors),
        textinfo='label+percent',  # Show labels and percentages
        showlegend=True
    )])
    carbon_footprint_pie.update_layout(
        title={
            'text': "Carbon Footprint (kg CO2)",
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.0,
            'yanchor': 'top',
            'font': {
                'size': 16,
                'color': '#00563B'
            }
        },
        margin=dict(t=40, b=0, l=0, r=0),
        height=400,
        width=400
    )

    # Data for previous weeks
    start_of_last_week = start_of_week - timedelta(weeks=1)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    start_of_week_before_last = start_of_last_week - timedelta(weeks=1)
    end_of_week_before_last = start_of_week_before_last + timedelta(days=6)

    this_week_data = TravelLog.objects.filter(user=user, date__range=[start_of_week, end_of_week]) \
        .values('mode_of_transport') \
        .annotate(total_distance=Sum('distance'), total_carbon_footprint=Sum('carbon_footprint'))

    last_week_data = TravelLog.objects.filter(user=user, date__range=[start_of_last_week, end_of_last_week]) \
        .values('mode_of_transport') \
        .annotate(total_distance=Sum('distance'), total_carbon_footprint=Sum('carbon_footprint'))

    week_before_last_data = TravelLog.objects.filter(user=user, date__range=[start_of_week_before_last, end_of_week_before_last]) \
        .values('mode_of_transport') \
        .annotate(total_distance=Sum('distance'), total_carbon_footprint=Sum('carbon_footprint'))

    def calculate_totals(data):
        total_distance = sum(item['total_distance'] for item in data)
        total_carbon_footprint = sum(item['total_carbon_footprint'] for item in data)
        return total_distance, total_carbon_footprint

    # Calculate the totals for the past three weeks
    try:
        this_week_total_distance, this_week_total_carbon_footprint = calculate_totals(this_week_data)
        last_week_total_distance, last_week_total_carbon_footprint = calculate_totals(last_week_data)
        week_before_last_total_distance, week_before_last_total_carbon_footprint = calculate_totals(week_before_last_data)

        # Round totals to two decimal places
        this_week_avg = round((this_week_total_carbon_footprint) / this_week_total_distance, 2) if this_week_total_distance != 0 else 0
        last_week_avg = round((last_week_total_carbon_footprint) / last_week_total_distance, 2) if last_week_total_distance != 0 else 0
        week_before_avg = round((week_before_last_total_carbon_footprint) / week_before_last_total_distance, 2) if week_before_last_total_distance != 0 else 0
    except ZeroDivisionError:
        this_week_avg = last_week_avg = week_before_avg = 0

    # Prepare data for bar chart
    weeks = ['This Week', 'Last Week', 'Week Before Last']
    averages = [this_week_avg, last_week_avg, week_before_avg]

    # Create a simple bar chart
    avg_plot = go.Figure(data=[go.Bar(
        x=weeks,
        y=averages,
        marker_color='#1f77b4',
        text=[f"{avg:.2f}" for avg in averages],  # Display average values on bars
        textposition='auto'
    )])

    avg_plot.update_layout(
        height=450,
        width=400,
        margin=dict(t=50, b=50, l=0, r=0),
        title_text="Average CO2 per Meter of Travel (g/km)",
        title_x=0.5,
        paper_bgcolor='#E5F6DF',
        plot_bgcolor='#E5F6DF',
        font=dict(
            family="Arial, sans-serif",
            color='#00563B',
            size=14
        ),
        title_font=dict(
            family="Arial, sans-serif",
            color='#00563B',
            size=16
        )
    )

    # Convert the figures to HTML
    distance_pie_html = distance_pie.to_html(full_html=False, include_plotlyjs='cdn')
    carbon_footprint_pie_html = carbon_footprint_pie.to_html(full_html=False, include_plotlyjs='cdn')
    avg_plot_html = avg_plot.to_html(full_html=False, include_plotlyjs='cdn')

    context = {
        'distance_pie': mark_safe(distance_pie_html),
        'carbon_footprint_pie': mark_safe(carbon_footprint_pie_html),
        'avg_plot': mark_safe(avg_plot_html),
        'total_distance': total_distance,
        'total_carbon_footprint': total_carbon_footprint
    }

    return render(request, 'main/home.html', context)

    

def redeem(request):
    return render (request,'main/redeem.html')

def leaderboard(request):
    return render (request,'main/leaderboard.html')

def carpooling(request):
    return render (request,'main/carpooling.html')

def tips(request):
    return render (request,'main/tips.html')