from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
import random

@login_required(login_url='signin')
def index(request):
    # Get the current user's profile
    current_user_profile = Profile.objects.get(user=request.user)

    # Get the usernames that the current user is following
    followed_usernames = FollowersCount.objects.filter(follower=request.user.username).values_list('user', flat=True)

    # Fetch posts from the users the current user is following
    followed_users_posts = Post.objects.filter(user__in=followed_usernames)

    # Fetch all users except the current user
    all_users_except_current = User.objects.exclude(username=request.user.username)
    
    # Fetch the users the current user is following
    followed_users = User.objects.filter(username__in=followed_usernames)

    # Get new suggestions by excluding the users the current user is already following
    suggested_users = all_users_except_current.exclude(id__in=followed_users.values_list('id', flat=True))
    
    # Shuffle the suggested users for randomness
    shuffled_suggestions = list(suggested_users)
    random.shuffle(shuffled_suggestions)

    # Get profiles for the suggested users
    suggested_user_profiles = Profile.objects.filter(user__in=shuffled_suggestions)

    # Render the result, limiting the suggestions to the top 4
    return render(request, 'index.html', {
        'user_profile': current_user_profile,
        'posts': followed_users_posts,
        'suggested_user_profiles': suggested_user_profiles[:4]
    })


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        img = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, img=img, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')    
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)


    if request.method == 'POST':
        username = request.POST['username']
        user_ids = User.objects.filter(username__icontains=username).values_list('id', flat=True)
        profile_list = Profile.objects.filter(id_user__in=user_ids)

        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': profile_list})


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if delete_follower := FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if not like_filter:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1 
        post.save()
    else:
        like_filter.delete()
        post.no_of_likes -= 1 
        post.save()
    return redirect('/')


@login_required(login_url='signin')
def profile(request, username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=username)

    follower = request.user.username
    user = username

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        btn_txt = 'unfollow' 
    else:
        btn_txt = 'Follow' 

    user_followers = len(FollowersCount.objects.filter(user=username)) 
    user_followings = len(FollowersCount.objects.filter(follower=username))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_count': len(user_posts),
        'btn_txt': btn_txt,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }
    return render(request, 'profile.html', context)
    

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if (img := request.FILES.get('image')) is None:
            img = user_profile.profileimg
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = img
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    return render(request, 'settings.html', { 'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a profile object for the new user and redirect them to settings page
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(f"suer is {user}")
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
