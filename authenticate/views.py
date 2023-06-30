from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


from authenticate.models import CustomUser

from .forms import ChangePasswordForm, SignUpForm
from authenticate.forms import SignUpForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {}
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            
            password = request.POST.get("password1")
            print(password)
            user.set_password(password)
            user.save()
                
        
            return redirect('/auth/login')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'authenticate/signup.html', context)



def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(username=username, password=password)

        if auth is not None:
            auth_login(request, auth)
            message, new = LoginMessage.objects.get_or_create(id=1)
            if request.user.is_superuser or request.user.is_admin:
                messages.success(request, message.message)  # <-
            else:
                messages.success(request, message.basic)
            
            # print(next_)
            # if next_ is not None and next_ is not "":
            #     return redirect(next_)
            
            user = CustomUser.objects.get(username=username)
            if user.is_admin:
                return redirect(reverse('control_panel'))

            else:
                return redirect(reverse('superuser_home'))
        messages.success(request, f'Username and Password provided did not match. Try again')
    return render(request, 'authenticate/login.html', context)







from authenticate.models import CustomUser

def reset(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:

            messages.success(request, 'User Not Found. Try Again') 
   
    return render(request, 'authentication/reset.html')



def confirm(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {}
    return render(request, 'authentication/confirm.html', context)




from django.contrib.auth.decorators import login_required
from main.forms import PaymentPicForm, RDPFIleForm
from .models import LoginMessage, WhatsappNumber, BannerMessage
from .forms import LoginMessageForm, ProfileForm, WhatsAppForm, BannerMessageForm

@login_required()
def profile(request):
    context = {}
    password_form = ChangePasswordForm(instance=request.user)
    message, new =  LoginMessage.objects.get_or_create(id=1)
    banner, new =  BannerMessage.objects.get_or_create(id=1)
    n, new =  WhatsappNumber.objects.get_or_create(id=1)
    context = {
        "password_form": password_form,  
        "paymentform": PaymentPicForm(),
        "rdpfileform": RDPFIleForm(),
        "whatsapp_form": WhatsAppForm(instance=n),
        "documents": "",
        "message":message,
        "notifications": "",
        "profile_form": ProfileForm(instance=request.user),
        "activities": "",
        "banner_form": BannerMessageForm(instance=banner),
        "message_form": LoginMessageForm(instance=message)

    }
    return render(request, 'authenticate/profile.html', context)

@login_required()
def change_password(request):
    context = {}
    if request.method == 'POST':
        user = CustomUser.objects.get(phone_number__iexact=request.user)

        form = ChangePasswordForm(request.POST, request.FILES, instance=user)
        if form.is_valid():

            user.set_password(form.password)
            user.save()

    return redirect('/auth/profile')

@login_required()
def user_logout(request):
    logout(request)
    messages.success(request, 'Session Closed') 
    return redirect('/auth/login')

from main.models import PaymentPic, RDPFile
from main.forms import PaymentPicForm, RDPFIleForm

@login_required()
def update_banner(request):
    print(request.POST)
    print(request.FILES)
    context = {}
    if request.method == 'POST':
        pic, new = PaymentPic.objects.get_or_create(id=1)
        form = PaymentPicForm(request.POST, request.FILES, instance=pic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image added successfully')
    return redirect(reverse('settings'))

@login_required()
def update_rdp(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        rdp, new = RDPFile.objects.get_or_create(id=1)
        form = RDPFIleForm(request.POST, request.FILES, instance=rdp)
        if form.is_valid():
            form.save()
            messages.success(request, 'File Upload is successfully')
    return redirect(reverse('settings'))

@login_required()
def update_banner_text(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        rdp, new = BannerMessage.objects.get_or_create(id=1)
        form = BannerMessageForm(request.POST, instance=rdp)
        if form.is_valid():
            form.save()
            messages.success(request, 'saved is successfully')
    return redirect(reverse('settings'))

@login_required()
def update_password(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        print(request.user.username)
        form = ChangePasswordForm(request.POST, request.FILES, instance=request.user)
        user = request.user
        if form.is_valid():
            user.set_password(request.POST.get('new_password'))
            user.save()
            messages.success(request, 'Password Update is successfully')
        messages.error(request, form.errors)
    return redirect(reverse('settings'))



@login_required()
def login_message(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        print(request.user.username)
        user = CustomUser.objects.get(username__iexact=request.user.username)
        form = ChangePasswordForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.set_password(form.password)
            user.save()
    return redirect(reverse('settings'))


@login_required()
def update_message(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        print(request.user.username)
        user, new = LoginMessage.objects.get_or_create(id=1)
        form = LoginMessageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Message Updayed Successfully")
    return redirect(reverse('settings'))



@login_required()
def update_profile(request):
    context = {}
    form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    return redirect(reverse('settings'))



from main.models import VPS

@login_required
def light_update_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        print(password)
        print("TTTTTTTTTTTTTT")
        if request.user.is_seller or request.user.is_superuser:
            # instance = VPS.objects.get(user=request.user)
            user = CustomUser.objects.get(id=request.user.id)
            print(user)
            user.set_password(password)
            user.save()
            user.set_password_vps(password)
            # instance.password = password
            # instance.save()

            messages.success(request, "Password Changed Successfully")
            if request.user.is_superuser:
                return redirect(reverse('superuser_home'))

            if request.user.is_seller:
                return redirect(reverse('seller'))    
    return render(request, 'authenticate/password_change.html', )

@login_required()
def update_whatsapp(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        user, new = WhatsappNumber.objects.get_or_create(id=1)
        user.number=request.POST.get("number", None)
        user.link = request.POST.get("link", None)
        user.save()
    return redirect(reverse('settings'))



from referrals.models import ReferralRelationship



def referral_signup(request, token):
    referral = get_object_or_404(ReferralRelationship, refer_token=token)
    if request.user.is_authenticated:
        return redirect('/')

    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            password = request.POST.get("password1")
            user.set_password(password)
            user.inviter = referral.inviter
            user.save()
            
            referral.invited = user
            referral.save()
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
    context = {'form': form, 'token': token}
    return render(request, 'authenticate/signup.html', context)


# from allauth.account.views import 