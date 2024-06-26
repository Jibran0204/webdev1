from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Author, newsStory
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the newsAgency index.")

def test(request):
    return HttpResponse("this is a test.")

@csrf_exempt
def login(request):
    if request.method == "POST":

        if request.user.is_authenticated:
            return HttpResponse('User is already logged in')

        username = request.POST.get('username')
        password = request.POST.get('password')

        # cosntruct data
        data = 'user name: ' + username + ' password: ' + password
        
        # print(data)
        user = authenticate(username=username, password=password)
        # hmm = User.objects.filter(is_superuser=True).values_list('username')
        # print("jsanfjfn")


    if user is not None:
        if user.is_active:
            django_login(request, user)
            request.session['username'] = username
            return HttpResponse('login successful', status=200)
        else:
            return HttpResponse('login failed', status=401)
    else:
        return HttpResponse('login failed', status=401)
    
@csrf_exempt
def logout(request):
    if request.method == "POST":
        
        if request.user.is_authenticated:
            django_logout(request)
            return HttpResponse("logged out", status=200)
        else:
            return HttpResponse("Not logged in")

@csrf_exempt
def check_login(request):
    if request.user.is_authenticated:
        print(request)
        return HttpResponse("already logged in", status = 200)
    else:
        return HttpResponse("You are not logged in", status = 404)
    
@csrf_exempt
def stories(request):
    if request.method == "POST":
        # print("BEFORE")
        if request.user.is_authenticated:
            # If authenticated, get the username from the session data
            # print("AFTER")
            username = request.session.get('username')
            # print(username)
            if not username:
                return HttpResponse("Username not found in session data", status=400)

            # Get the user object
            try:
                user = User.objects.get(username=username)
                # print(user)
            except User.DoesNotExist:
                return HttpResponse("User not found", status=400)
            
        data = json.loads(request.body.decode())
        # print(data)
        # get all the story info
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')

        # Validate headline length
        if not (1 <= len(headline) <= 64):
            return HttpResponse("Headline length must be between 1 and 64 characters", status=503)

        # Validate category
        valid_cats = ['pol', 'art', 'tech', 'trivia']
        if category not in valid_cats:
            return HttpResponse("Invalid category", status=503)

        # Validate region
        valid_regs = ['uk', 'eu', 'w']
        if region not in valid_regs:
            return HttpResponse("Invalid region", status=503)

        # Validate details length
        if not (1 <= len(details) <= 128):
            return HttpResponse("Details length must be between 1 and 128 characters", status=503)


        # get the current datetime
        date = timezone.now()
        # print(date)
        
        try:
            author = Author.objects.get(user=user)
            # print(author)
        except Author.DoesNotExist:
            return  HttpResponse("Author doesnt exist", status=400)
        
        # error checks
        story = newsStory(headline=headline, category=category, region=region, details=details, author=author, date = date)
        story.save()
        
        return HttpResponse("you can post a story", status = 201)
    
    elif request.method == "GET":
        # Implement a message which is returned if there are no stories found
        category = request.GET.get('story_cat')
        region = request.GET.get('story_region')
        date = request.GET.get('story_date')
        stories = newsStory.objects.all()

        if category != '*':
            stories = stories.filter(category=category)
        if region != '*':
            stories = stories.filter(region=region)
        if date != '*':
            stories = stories.filter(date=date)

        serialized_stories = [{
            'key': story.id,
            'headline': story.headline, 
            'story_cat': story.category, 
            'story_region': story.region, 
            'story_date': story.date,
            'author': str(story.author),
            'story_details': story.details} 
            for story in stories]

        if not serialized_stories:
            # If no stories found, return a 404 response
            return HttpResponse("No stories found", status=404)

        return JsonResponse({"stories": serialized_stories}, safe=False)



@csrf_exempt
def delete_story(request, story_id):
    if request.method == "DELETE":
        if request.user.is_authenticated:
            # If authenticated, get the username from the session data
            # print("AFTER")
            username = request.session.get('username')
            # print(username)
            if not username:
                return HttpResponse("Username not found in session data", status=400)

            # Get the user object
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse("User not found", status=400)

        try:
            # Retrieve the story object from the database based on the story_id
            story = newsStory.objects.get(pk=story_id)
        except newsStory.DoesNotExist:
            return HttpResponse("Story not found", status=501)
        # Fetch the current logged-in user directly
        user = request.user  
        # Compare the author of the story with the current user
        if story.author.user != user:  # Assuming Author.user is a ForeignKey to User
            return HttpResponse("You are not the author of this story", status=501)
        # Delete the story
        story.delete()
        return HttpResponse("Story deleted successfully", status=200)
    else:
        return HttpResponse("Method Not Allowed", status=501)
    
    

@csrf_exempt
def storyManager(request):
    if request.method == "GET":
        return HttpResponse("Welcome to the story manager")
    elif request.method == "POST":
        return HttpResponse("Welcome to the story manager")
    