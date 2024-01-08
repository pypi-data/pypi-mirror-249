from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


def index_view(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        print("name",name)
        # Calculate age
        today = datetime.now()
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # Get current time and determine greeting
        current_time = today.strftime('%H:%M:%S')
        time_greeting = determine_time_greeting(today.hour)

        response_data = {
            'name': name,
            'age': age,
            'current_time': current_time,
            'time_greeting': time_greeting,
        }

        return JsonResponse(response_data)
    title = "Django Boilerplate Generator"
    
    key_features = {
        "Quick Start": "Generate a Django project structure quickly",
        "Core App": "Create a core app with basic templates",
        "Configurations": "Configured architectural settings for a clean start",
        # Add more key features as needed
    }

    contact_info = [
        {"platform": "GitHub", "link": "https://github.com/httperror451/django_boilerplate_generator"},
        {"platform": "LinkedIn", "link": "https://linkedin.com/in/contactwasim"},
        # Add more contact info as needed
    ]

    server_response = """This is a initial boilerplate generated message,
    rendered via Django server\nModify views.index_view method and templates\index.html"""

    return render(request, 'index.html', {
        'title': title,
        'key_features': key_features,
        'contact_info': contact_info,
        'server_response': server_response
    })


def determine_time_greeting(hour):
    if 5 <= hour < 12:
        return 'Good morning'
    elif 12 <= hour < 18:
        return 'Good afternoon'
    else:
        return 'Good evening'