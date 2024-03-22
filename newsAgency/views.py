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
        # debugging purposes
        print(data)
        user = authenticate(username=username, password=password)
        # hmm = User.objects.filter(is_superuser=True).values_list('username')
        print("jsanfjfn")


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
    
        if request.user.is_authenticated:
            # If authenticated, get the username from the session data
            username = request.session.get('username')
            if not username:
                return HttpResponse("Username not found in session data", status=400)

            # Get the user object
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse("User not found", status=400)
            
        data = json.loads(request.body.decode())
        print(data)
        # get all the story info
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')

        # get the current datetime
        date = timezone.now()
        

        try:
            author = Author.objects.get(user=user)
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

        # Serialize the queryset
        serialized_stories = serialize('json', stories)

        return HttpResponse(serialized_stories, content_type='application/json')


@csrf_exempt
def delete_story(request, story_id):
    if request.method == "DELETE":
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
    