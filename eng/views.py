import json
from pyexpat.errors import messages
from django.shortcuts import render,redirect,HttpResponse
from .models import *

from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')
def chatbot(request):
    return render(request,'chatbot.html')
def home(request):
    if 'useremail' in request.session:
        email = request.session['useremail']
        try:
            same = UserReg.objects.get(Email=email)
            name = same.Name
            return render(request, 'home.html',{'name': name}) 
        except:
            return redirect('login')
          
    else:
        return redirect('login')
def RegisterUser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')   
        password = request.POST.get('password')
        phone = request.POST.get('phone') 
        try:
            same = UserReg.objects.get(Email=email)
            if same:
                alert = "<script> alert('User Already exist'); window.location.href = '/register/';</script>"
                return HttpResponse(alert)

        except:    
            User = UserReg(Name=name,Email=email,Password=password,Phone=phone)
            User.save()
            return redirect('login')
    else:
        return render(request, 'register.html')

def LoginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')   
        password = request.POST.get('password')
        try:
            check = UserReg.objects.get(Email=email,Password=password)
            if check:
                request.session['useremail'] = check.Email
                return redirect('home') 
        except Exception as e:
            print(e)
            alert = "<script> alert('invalid Username or password'); window.location.href = '/login/';</script>"      
            return HttpResponse(alert)
    else:
         return render(request, 'login.html')
def logout(request):
    request.session.flush()
    return redirect('login')
    
def adlogin(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        u = 'admin'
        p = 'admin'
        if name==u:
            if password==p:
                return redirect('adhome')
            else:
             return render(request,"adlogin.html")
        else:
             return render(request,"adlogin.html")
    else:
         return render(request,"adlogin.html")
def adhome(request):
    return render(request,'adhome.html')
def profile(request):
    email = request.session.get('useremail')
    
    if email is not None:
        try:
            user = UserReg.objects.get(Email=email)
            return render(request, 'profile.html', {'user': user})
        except UserReg.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')  
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('login') 
    
def editprofile(request):
    email = request.session.get('useremail') 
    try:
        user = UserReg.objects.get(Email=email)  # Ensure 'Email' matches the field name in the model
    except UserReg.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')  # Redirect to login if user is not found

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        level=request.POST.get('level')
        profile_picture = request.FILES.get('profile_pic')

        # Update user profile fields
        user.Name = name
        user.Email = email
        user.Phone = phone
        user.level=level
        
        # Update profile picture if provided
        if profile_picture:
            user.profile_pic = profile_picture

        # Save the updated User
        user.save()

        # Send success message
        messages.success(request, 'Profile updated successfully!')

        return redirect('profile')  

    return render(request, 'profile.html', {'user': user})

# views.py
# views.py
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyttsx3
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os



def userlist(request):
    user=UserReg.objects.all()
    return render(request,'userlist.html',{'user':user})
def deleteuser(request,id):
    data=UserReg.objects.filter(id=id)
    data.delete()
    return redirect('userlist')


from django.contrib import messages


def feedback_rate(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'feedback.html')

        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value. Please select a valid rating.")
            return render(request, 'feedback.html')

        # Create and save the Feedback instance
        feedback = Feedback(
            feedback_text=feedback_text,
            rating=rating
        )
        feedback.save()

        # Set a success message
        messages.success(request, "Thank you for your feedback!")
        return redirect('feedback')  # Redirect to refresh the form page and display the success message
    
    # Render the feedback form
    return render(request, 'feedback.html')

def feedbacklist(request):
    data=Feedback.objects.all()
    return render(request,'feedbacklist.html',{'data':data})

# import csv
# import os
# import json
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pyttsx3

# # Load dataset at the start to avoid repeated I/O operations
# data_path = os.path.join(settings.BASE_DIR, 'data.csv')
# responses = {}

# with open(data_path, 'r') as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip header row
#     for row in reader:
#         request, response = row
#         responses[request.lower()] = response

# @csrf_exempt
# def process_voice(request):
#     if request.method == 'POST':
#         try:
#             # Get the message from the frontend
#             data = json.loads(request.body)
#             user_message = data.get('message', '').strip().lower()

#             # Check for a matching response in the dataset
#             bot_response = responses.get(user_message, "Sorry, I didn't understand that. Could you try asking another way?")

#             # Generate speech (audio file)
#             engine = pyttsx3.init()
#             audio_file_name = "bot_response.mp3"
#             audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)

#             # Ensure the directory exists, if not create it
#             if not os.path.exists(settings.MEDIA_ROOT):
#                 os.makedirs(settings.MEDIA_ROOT)

#             # Save the speech to the file
#             engine.save_to_file(bot_response, audio_file_path)
#             engine.runAndWait()

#             # Return the bot response and the audio URL
#             audio_url = os.path.join(settings.MEDIA_URL, audio_file_name)
#             return JsonResponse({
#                 'response': bot_response,
#                 'audio_url': audio_url
#             })

#         except Exception as e:
#             print("Error in processing voice:", e)
#             return JsonResponse({'response': 'An error occurred, please try again.'})
import csv
import os
import json
import pyttsx3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from django.conf import settings


import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stemmer and stopwords
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load the dataset into memory
data_path = os.path.join(settings.BASE_DIR, 'data.csv')
responses = {}

with open(data_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        if len(row) == 3:  # Ensure the row has exactly 3 values
            request, response, keywords = row
            keywords = keywords.lower().split(', ')  # Convert keywords into a list
            responses[request.lower()] = {
                'response': response,
                'keywords': keywords
            }
        else:
            print(f"Skipping invalid row: {row}")

# Tokenize and preprocess user input
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())  # Tokenize and convert to lower case
    filtered_tokens = [ps.stem(word) for word in tokens if word not in stop_words]  # Remove stopwords and apply stemming
    return filtered_tokens

# Function to find a match
def find_best_match(user_input):
    user_tokens = preprocess_input(user_input)
    best_match = None
    best_match_score = 0

    for request, data in responses.items():
        keyword_matches = 0
        for keyword in data['keywords']:
            if keyword in user_tokens:
                keyword_matches += 1
        if keyword_matches > best_match_score:
            best_match_score = keyword_matches
            best_match = data['response']
    
    return best_match if best_match else "Sorry, I didn't understand that. Could you try asking another way?"

@csrf_exempt
def process_voice(request):
    if request.method == 'POST':
        try:
            # Get the message from the frontend
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            # Find the best match response
            bot_response = find_best_match(user_message)

            # Generate speech (audio file)
            engine = pyttsx3.init()
            audio_file_name = "bot_response.mp3"
            audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)

            # Ensure the directory exists, if not create it
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # Save the speech to the file
            engine.save_to_file(bot_response, audio_file_path)
            engine.runAndWait()

            # Return the bot response and the audio URL
            audio_url = os.path.join(settings.MEDIA_URL, audio_file_name)
            return JsonResponse({
                'response': bot_response,
                'audio_url': audio_url
            })

        except Exception as e:
            print("Error in processing voice:", e)
            return JsonResponse({'response': 'An error occurred, please try again.'})
