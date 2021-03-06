from threading import current_thread
from django.contrib.auth.models import User
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm,UserProfileForm,CommentForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Comment,Like,Mark,UserProfile
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

#homepage,
def index(request): 
    #return top 3 most liked news category 
    category_list = Category.objects.order_by('-likes')[:3]
    context_dict = {} 
    context_dict['categories'] = category_list
    #return top 3 most viewed news
    page_list = Page.objects.order_by('-views')[:3]
    context_dict['pages'] = page_list
    
    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)

    return response

#about.html
def about(request):
    return render(request, 'rango/about.html')

# when user is authenticated, they can be able to detailed news page
@login_required
def show_page(request,category_name_slug,page_title_slug):
    context_dict = {}
    current_user = request.user
    # update the number of views of each news after they click and view the detailed news page
    page = Page.objects.get(slug = page_title_slug)
    page.views += 1
    page.save(update_fields=['views'])
    context_dict['page'] = page
    #return to the PageDetailed.html the status of the like and mark for this news given by current user
    like = Like.objects.filter(page=page,user=current_user)
    mark = Mark.objects.filter(page=page,user=current_user)

    if like.count == 0:
        context_dict['like'] = None
    else:
        context_dict['like'] = like
    if mark.count == 0:
        context_dict['mark'] = None
    else:
        context_dict['mark'] = mark

    form = CommentForm()
    #return to the PageDetailed.html the comments that given by all the users before for this news
    comments = Comment.objects.filter(page = page)
    context_dict['form'] = form
    context_dict['comments'] = comments
    return render(request,'rango/PageDetails.html',context = context_dict)

#show all the news of this category 
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        # update the number of views of this category
        category.views += 1
        category.save(update_fields=['views'])
        # get the corresponding news for this category 
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request,'rango/category.html',context = context_dict)

#Authenticated user can be able to write comment 
@login_required
def add_comment(request,category_name_slug,page_title_slug):
    form = CommentForm()
    if request.method == 'POST':
        current_user = request.user
        context_dict = {}
        page = Page.objects.get(slug = page_title_slug)
        context_dict['page'] = page
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category'] = category
    
        form = CommentForm()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.page = page
                comment.user = current_user
                #save the comment
                comment.save()
                #update the number of comments for this news
                page.comments += 1
                page.save(update_fields=['comments'])
                #update the form
                form = CommentForm()
                # update the new comment to PageDetail.html
                comments = Comment.objects.filter(page = page)
                context_dict['form'] = form
                context_dict['comments'] = comments
                return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_name_slug,'page_title_slug':page_title_slug}))
            else: 
                print(form.errors)
    return render(request,'rango/pageDetails.html',{'form':form})

#Only staff can be able to access this link 
@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if 'image' in request.FILES:
                category.image = request.FILES['image']
            category.save()
            return redirect(reverse('rango:index')) 
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})

#Only staff can be able to access this link 
@login_required
def add_page(request, category_name_slug): 
    category = Category.objects.get(slug=category_name_slug) 
    form = PageForm()
    if request.method == 'POST': 
        form = PageForm(request.POST)

        if form.is_valid(): 
            if category: 
                page = form.save(commit=False) 
                page.category = category 
                if 'image' in request.FILES:
                    page.image = request.FILES['image']
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else: 
            print(form.errors)
    context_dict = {'form': form, 'category': category} 
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html',context={'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}") 
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

#allow user to praise the news by clicking thumb-up icon
@login_required
def like_page(request):
    context_dict = {}
    page_id = request.POST.get('page_id', 0)
    page = Page.objects.get(id = page_id)
    category  = Category.objects.get(page = page)
    current_user = request.user
    try:
        #if like already exists,cancel this like
        like = Like.objects.get(page = page,user = current_user)
        like.delete()
        #update the number of likes for this news and corresponding category
        page.likes -=1
        category.likes -=1
        page.save(update_fields=['likes'])
        category.save(update_fields=['likes'])
        context_dict['like'] = None
    except Like.DoesNotExist:
        #if like didn't exists, add this like
        #update the number of likes for this news and corresponding category
        page.likes+=1
        category.likes+=1
        page.save(update_fields=['likes'])
        category.save(update_fields=['likes'])
        like = Like.objects.get_or_create(page = page,user = current_user)
        context_dict['like'] = like

    return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category.slug,'page_title_slug':page.slug}))

#allow user to mark the news by clicking star icon
@login_required
def mark_page(request):
    context_dict = {}
    page_id = request.POST.get('page_id', 0)
    page = Page.objects.get(id = page_id)
    category  = Category.objects.get(page = page)
    current_user = request.user
    try:
        #if mark already exists,cancel this mark
        mark = Mark.objects.get(page = page,user = current_user)
        mark.delete()
        #update the number of likes for this news
        page.marks -=1
        page.save(update_fields=['marks'])
        context_dict['mark'] = None
    except Mark.DoesNotExist:
        #if mark didn't exists,add this mark
        #update the number of likes for this news
        page.marks+=1
        page.save(update_fields=['marks'])
        mark = Mark.objects.get_or_create(page = page,user = current_user)
        context_dict['mark'] = mark

    return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category.slug,'page_title_slug':page.slug}))
#user profile html
@login_required
def profile(request):
    profile_form = UserProfileForm()
    context_dict = {}
    current_user = request.user
    try:
        profile = UserProfile.objects.get(user = current_user)
        context_dict['profile'] = profile
    except UserProfile.DoesNotExist:
        #if the user is log in by third-party, we will automatically create the profile for him/her
        profile = UserProfile.objects.get_or_create(user = current_user)
        context_dict['profile'] = profile
    #return the userprofile information back to profile.html
    context_dict['profile_form'] = profile_form
    return render(request,'rango/profile.html',context = context_dict)

#allow users to update some of their personal information
@login_required
def update_profile(request):
    current_user = request.user
    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if username == "":
           return redirect(reverse('rango:profile_page'))
        email = request.POST.get('email')
        profile_form = UserProfileForm(request.POST)
        current_user.email = email
        current_user.username = username
        current_user.save(update_fields=['email','username'])
        if profile_form.is_valid():
            #delete the old profile
            old_profile = UserProfile.objects.filter(user = current_user)
            old_profile.delete()
            new_profile = profile_form.save(commit=False)
            new_profile.user = current_user
            if 'picture' in request.FILES:
                new_profile.picture = request.FILES['picture']
            #update a new one for the user according to the information they give
            new_profile.save()
            context_dict['profile'] = new_profile
            profile_form = UserProfileForm()
            context_dict['profile_form'] = profile_form
        return render(request,'rango/profile.html',context = context_dict) 
    profile = UserProfile.objects.get(user= current_user)
    profile_form = UserProfileForm()
    context_dict['profile'] = profile
    context_dict['profile_form'] = profile_form
    return render(request,'rango/profile.html',context = context_dict)

#show all the marked news of this user
@login_required
def marklist(request):
    current_user = request.user
    context_dict = {}
    marks = Mark.objects.filter(user = current_user)
    context_dict['marks'] = marks
    profile = UserProfile.objects.get(user= current_user)
    profile_form = UserProfileForm()
    context_dict['profile'] = profile
    context_dict['profile_form'] = profile_form
    return render(request,'rango/show_marklist.html',context = context_dict)

#show all the liked news of this user
@login_required
def likelist(request):
    current_user = request.user
    context_dict = {}
    likes = Like.objects.filter(user = current_user)
    context_dict['likes'] = likes
    profile_form = UserProfileForm()
    profile = UserProfile.objects.get(user= current_user)
    context_dict['profile_form'] = profile_form
    context_dict['profile'] = profile
    return render(request,'rango/show_likelist.html',context = context_dict)

#show all the comments of this user
@login_required
def commentlist(request):
    current_user = request.user
    context_dict = {}
    comments = Comment.objects.filter(user = current_user)
    context_dict['comments'] = comments
    profile_form = UserProfileForm()
    profile = UserProfile.objects.get(user= current_user)
    context_dict['profile_form'] = profile_form
    context_dict['profile'] = profile
    return render(request,'rango/show_commentlist.html',context = context_dict)

#allow user to delete their own comments
@login_required
def deletecomment(request):
    comment_id = request.POST.get('id', 0)
    print(comment_id)
    comment = Comment.objects.get(id = comment_id)
    page = comment.page
    #update the number of comments of this news
    page.comments -= 1
    if page.comments <= 0:
        page.comments = 0
    page.save(update_fields=['comments'])
    comment.delete()
    return redirect(reverse('rango:profile_page'))

#allow user to delete their own likes
@login_required
def deletelike(request):
    like_id = request.POST.get('id', 0)
    like = Like.objects.get(id = like_id)
    page = like.page
    #update the number of likes of this news and corresponding category
    page.likes -= 1
    if page.likes <= 0:
        page.likes = 0
    page.save(update_fields=['likes'])
    category = page.category
    category.likes -=1
    category.save(update_fields=['likes'])
    like.delete()
    return redirect(reverse('rango:profile_page'))

#allow user to delete their own marks
@login_required
def deletemark(request):
    mark_id = request.POST.get('id', 0)
    mark = Mark.objects.get(id = mark_id)
    page = mark.page
    #update the number of marks of this news
    page.marks -= 1
    if page.marks <= 0:
        page.marks = 0
    page.save(update_fields=['marks'])
    mark.delete()
    return redirect(reverse('rango:profile_page'))



def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    return render(request,'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie) 
    if not val: 
        val = default_val 
    return val


def visitor_cookie_handler(request): 
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now())) 
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0: 
        visits = visits + 1 
        request.session['last_visit'] = str(datetime.now())  
    else: 
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

