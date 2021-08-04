from django.http.response import FileResponse
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm,UserProfileForm,CommentForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Comment
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request): 
    #chapter2 url = "<a href='/rango/about'>About</a>"
    category_list = Category.objects.order_by('-likes')[:3]
    context_dict = {} 
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!' 
    context_dict['categories'] = category_list
    page_list = Page.objects.order_by('-views')[:3]
    context_dict['pages'] = page_list
    
    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)

    return response


def about(request):
    #chapter2 url = "<a href='/rango/'>Index</a>"
    visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    context_dict['boldmessage'] = 'This tutorial has been put together by Yongyan Lin'
    return render(request, 'rango/about.html', context=context_dict)

def show_page(request,category_name_slug,page_title_slug):
    context_dict = {}
    try:
        page = Page.objects.get(slug = page_title_slug)
        # update the number of views of each News
        page.views += 1
        page.save(update_fields=['views'])
        context_dict['page'] = page
    except Page.DoesNotExist:
        page = None
        context_dict['page'] = None
    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        category = None
    if page is None:
        return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_name_slug,'page_title_slug':page_title_slug}))
    if category is None:
        return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_name_slug,'page_title_slug':page_title_slug}))
    
    form = CommentForm()
    comments = Comment.objects.filter(page = page)
    context_dict['form'] = form
    context_dict['comments'] = comments
    return render(request,'rango/PageDetails.html',context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        # update the number of views of each Category
        category.views += 1
        category.save(update_fields=['views'])
        
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request,'rango/category.html',context = context_dict)

@login_required
def add_comment(request,category_name_slug,page_title_slug):
    current_user = request.user
    context_dict = {}
    try:
        page = Page.objects.get(slug = page_title_slug)
        context_dict['page'] = page
    except Page.DoesNotExist:
        page = None
    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        category = None
    if page is None:
        return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_name_slug,'page_title_slug':page_title_slug}))
    if category is None:
        return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_name_slug,'page_title_slug':page_title_slug}))
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if category and page:
                comment = form.save(commit=False)
                comment.page = page
                comment.user = current_user
                comment.save()
                page.comments += 1
                page.save(update_fields=['comments'])
            else: 
                print(form.errors)
    form = CommentForm()
    comments = Comment.objects.filter(page = page)
    context_dict['form'] = form
    context_dict['comments'] = comments
    return render(request,'rango/PageDetails.html',context = context_dict)

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

@login_required
def add_page(request, category_name_slug): 
    try: 
        category = Category.objects.get(slug=category_name_slug) 
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))
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


