from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Author, newsStory
from django.contrib.auth import authenticate, login, logout
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
def login_user(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # cosntruct data
        data = 'user name: ' + username + ' password: ' + password
        # debugging purposes
        print(data)
        user = authenticate(username=username, password=password)
        hmm = User.objects.filter(is_superuser=True).values_list('username')
        print(hmm)


    if user is not None:
        if user.is_active:
            login(request, user)
            
            return HttpResponse('login successful')
        else:
            return HttpResponse('login failed')
    else:
        return HttpResponse('login failed')
    
@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        user = request.POST.get('username')

        if request.user.is_authenticated:
            logout(request)
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

        data = json.loads(request.body.decode())
        print(data)
        # get all the story info
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')
        username = data.get('username')

        # get the current datetime
        date = timezone.now()
        user = User.objects.get(username=username)

        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            return  HttpResponse("Author doesnt exist", status=400)
        
        # error checks
        story = newsStory(headline=headline, category=category, region=region, details=details, author=author, date = date)
        story.save()
        
        hmm = newsStory.objects.all()
        print(hmm)
        return HttpResponse("you can post a story", status = 201)
    
    elif request.method == "GET":

        # implement a message which is returned if there are no stories found
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
        print(stories)

        serialized_stories = [{
            'key': story.id,
            'headline': story.headline, 
            'story_cat': story.category, 
            'story_region': story.region, 
            'story_date': story.date,
            'author': str(story.author),
            'story_details': story.details} 
            for story in stories]

        return JsonResponse(serialized_stories, safe=False)

@csrf_exempt
def delete_story(request, story_id):
    if request.method == "DELETE":
        try:
            # Retrieve the story object from the database based on the story_id
            story = newsStory.objects.get(pk=story_id)
        except newsStory.DoesNotExist:
            return HttpResponse("Story not found", status=404)

        # Fetch the current logged-in user directly
        user = request.user  

        # Compare the author of the story with the current user
        if story.author.user != user:  # Assuming Author.user is a ForeignKey to User
            return HttpResponse("You are not the author of this story", status=403)

        # Delete the story
        story.delete()
        return HttpResponse("Story deleted successfully", status=200)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    
    

@csrf_exempt
def storyManager(request):
    if request.method == "GET":
        return HttpResponse("Welcome to the story manager")
    elif request.method == "POST":
        return HttpResponse("Welcome to the story manager")
    