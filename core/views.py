# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import ContactMessage, Contact, BlogPost, User, NewsletterSubscriber
from .forms import ContactMessageForm, UserSignupForm, UserLoginForm, NewsletterSubscriptionForm
from django.contrib import messages
from product.models import Product


def index(request):
    products = Product.objects.filter(featured=True)
    for index, product in enumerate(products): 
        product.delay = (index + 1) * 100
    return render(request, 'core/index.html', {'products':products})

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email already exists in the newsletter list
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, "This email is already subscribed.")
            else:
                # Save the new subscriber
                form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")

            # Redirect to the homepage or another page
            return redirect('index')  # Change this to your desired page

    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'subscribe_newsletter.html', {'form': form})       
            

# Signup View
class SignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('home')  # Redirect to home after signup

    def form_valid(self, form):
        if not NewsletterSubscriber.objects.filter(email=email).exists():
            NewsletterSubscriber.objects.create(email=email)
        user = form.save()
        login(self.request, user)  # Authenticate user immediately after signup
        return super().form_valid(form)


# Login View
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})


# Contact Message View
class ContactMessageView(CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


# Blog Post List View
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'core/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


# Blog Post Detail View
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'core/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if not post.is_published:
            raise Http404("This post is not published yet.")
        return post


# About Page View
#def about_view(request):
#    contact_info = Contact.objects.first()
#    return render(request, 'core/about.html', {'contact_info': contact_info})

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html')
