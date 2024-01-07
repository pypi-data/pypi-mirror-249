import re, datetime, ast, time, openai, requests, jwt, phonenumbers
from googleapiclient.discovery import build
from decimal import Decimal
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum
from cryptography.fernet import Fernet
from googleapiclient.errors import HttpError
from django.contrib.auth import login, logout, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes, force_str
from accounts.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from stela_control.context_processors import SiteData
from django.conf import settings
from pytz import country_timezones
from django.forms import formset_factory, inlineformset_factory
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from accounts.models import UserBase
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import (
    Content, Wallet, DataEmail, 
    DynamicBullets, Newsletter, SendMoney, BillingRecipt,
    ItemProducts, ItemServices, ItemDiscount,  
    InvoiceControl, BudgetControl, StelaSelection, 
    StelaItems, Templates, Order, StelaPayments, PathControl, 
    ControlFacturacion, FacturaItems, TemplateSections, StelaColors,
    ModuleItems, ProStelaData, OrderItems, Inventory, Elements, 
    Variant, Sizes, Gallery, Bulletpoints, Sizes, VariantsImage, Customer, 
    Budget, Category, SitePolicy, LegalProvision, SupportResponse, 
    Support, ChatSupport, SiteControl, ItemCloud, FacebookPage, InstagramAccount, FacebookPostPage, FacebookPageComments, FacebookPageCommentsReply, FacebookPageConversations,
    FacebookPageEvent,  FacebookPageLikes, FacebookPageMessages, FacebookPageShares, FacebookPostMedia, IGMediaContent, FacebookPageImpressions,
    IGPost, IGUserTag, FAQ, SetFaq, Contact,Comments, PaypalClient, Notifications,
    IGPostMetric, IGCarouselMetric, IGReelMetric, IGStoriesMetric, Company, SocialLinks, ProStelaExpert, ProStelaUsage, Reviews,
    Booking, BookingServices, City, Team, JobApplication
    
)
from .forms import (
    FAQForm, NewsletterForm, PolicyForm, BillingForm, BillingDiscountForm, 
    ServicesForm,TemplateForm, ProductForm, StylesForm, 
    TempSecForm, ColorsForm, VariantForm, SizeForm, GalleryForm, BulletForm, 
    WorksForm, VariantImageForm, BillingChargeFormDynamic, BillingChargeFormPOS, 
    BillingFormSuscription, AppstelaForm, LegalProvitionForm, StelaAboutForm, 
    PathForm, MediaForm, FooterContentForm, categForm, StaffForm, BaseInventoryForm,
    BulletSimpleForm, CommentsFormBlog, ReadOnlySupportForm, WalletForm,
    FbPostForm, FacebookEventsForm, IGPostForm, IGMediaForm, RequiredFormSet, CompanyForm, SocialMediaForm,
    SendGridForm,BlogForm, ContentForm, RedirectContentForm, StickerContentForm, ContentDynamicForm,
    SimpleContentForm, SetFaqForm, ImageContentForm, TitleContentForm, AboutContentForm, ReviewsForm,
    ConsultingForm, BookingConsultingForm, RegistrationForm, UserEditForm, UserPortalForm, UserLoginForm, PwdResetForm, 
    PwdResetConfirmForm, ValuesForm, LoginForm, JobApplicationForm, CatalogForm, ContactForm,
    CustomerForm
)

form_mapping = {
    #Content
    'TitleContentForm': TitleContentForm,
    'SimpleContentForm': SimpleContentForm,
    'ContentForm': ContentForm,
    'ContentDynamicForm': ContentDynamicForm,
    'RedirectContentForm': RedirectContentForm,
    'StickerContentForm': StickerContentForm,
    'GalleryForm': GalleryForm,
    'BulletSimpleForm': BulletSimpleForm,
    'ImageContentForm': ImageContentForm,
    'LegalProvitionForm': LegalProvitionForm,
    'FAQForm': FAQForm,
    'SetFaqForm': SetFaqForm,
    'BlogForm': BlogForm,
    'ValuesForm': ValuesForm,
    #Inventory
    'Inventory': Inventory,
    'Elements': Elements,
    'Variant': Variant,
    'ProductForm': ProductForm,
    'WorksForm': WorksForm,
    'VariantForm': VariantForm,
    'ServicesForm': ServicesForm,
    'BaseInventoryForm': BaseInventoryForm,
    'CatalogForm': CatalogForm,

}

SECRET_KEY = settings.STELA_SECRET

def get_form_class_by_name(form_name):
    return form_mapping[form_name]

def accountsData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        userpk = request.POST.get('userid')
        form_name = request.POST.get('form_name')
        form_id = request.POST.get('form-id')
        pk = request.POST.get('pk')
        domain = request.POST.get('domain')
        print(action, userpk, form_name, form_id, pk, domain)
        
        if action == 'cityCheck':
            country_id = request.POST.get('country_id')
            cities = City.objects.filter(country_id=country_id)
        
            return render(request, 'stela_control/load-data/city_data.html', {'cities': cities})

        if action == "checkEmail":
            pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            email = request.POST.get("user_input")
            if UserBase.objects.filter(email=email).exists():
                response = JsonResponse({'error': _('email not available')})
            elif not pattern.match(email):
                response = JsonResponse({'error': _('Invalid email')})
            else:
                response = JsonResponse({'success': _('email available')})
            return response

        if action == "checkUsername":
            username = request.POST.get("user_input")
            if UserBase.objects.filter(username=username).exists():
                response = JsonResponse({'error': _('username not available')})
                
            elif not re.match(r'^[a-z0-9_]+$', username):
                response = JsonResponse({'error': _('invalid username only lower case, numbers and (_) accepted')})
            
            else:
                response = JsonResponse({'success': _('username available')})
            
            return response
            
        if action == "checkPassword":
            password = request.POST.get("password")
            
            if len(password) < 8:
                response = JsonResponse({'error': _('Password must be at least 8 characters long')})
            
            elif not re.match(r'^[a-zA-Z0-9*.$_]+$', password):
                response = JsonResponse({'error': _('Password must contain only alphanumeric and special characters (a-zA-Z0-9*$_.)')})
            
            elif password.isalpha():
                response = JsonResponse({'error': _('Password must contain at least one number')})
                
            else:
                response = JsonResponse({'success': _('Password is valid')})

            return response

        if action == "matchPassword":
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                response = JsonResponse({'error': _('Password dismatch.')})
            else:
                response = JsonResponse({'success': _('Password match')})
            return response

        if action == "checkEditUser":
            obj=UserBase.objects.get(pk=userpk)
            form=UserEditForm(instance=obj)
            get_formset = inlineformset_factory(
                UserBase, SocialLinks, 
                form=SocialMediaForm,
                extra=0, can_delete=True,
                )
            formset=get_formset(instance=obj, prefix='formset')
            obj_data = render_to_string('stela_control/load-data/profile/dynamic-form.html', {
                            'form': form,  
                            'formset': formset,
                            'form_name': form_name,
                            'pk': userpk
                })
            
            response = JsonResponse({'content': obj_data})
            return response

        if action == "checkPortalUser":
            obj=UserBase.objects.get(pk=userpk)
            form=UserPortalForm(instance=obj)
            obj_data = render_to_string('stela_control/load-data/profile/single-form.html', {
                            'form': form,  
                            'form_name': form_name,
                            'pk': userpk
                })
            
            response = JsonResponse({'content': obj_data})
            return response
        
        if action == "password_reset":
            form=PwdResetForm() 
            obj_data = render_to_string('stela_control/load-data/auth/pw_reset/password_reset_form.html', {
                    'form': form, 
                })
            
            response = JsonResponse({'content': obj_data})
            return response
        
        if form_id == "editUserForm":
            obj=UserBase.objects.get(pk=pk)
            form=UserEditForm(request.POST, request.FILES, instance=obj) 
            get_formset = inlineformset_factory(
                    UserBase, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=0
                )
            formset=get_formset(request.POST, prefix='formset', instance=obj)
            if all([form.is_valid(), 
                    formset.is_valid(),
                    ]):
                parent_user = form.save(commit=False)
                parent_user.save()
                
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                                
                for form in instances:
                    form.parent_user = parent_user
                    form.save()

                return JsonResponse({'success':_('Your profile has been updated')})
            else:
                print(form.errors)
                print(formset.errors)
                obj_data = render_to_string('stela_control/load-data/profile/dynamic-form.html', { 
                    'form': form,
                    'formset': formset,
                    'form_name': form_id,
                    'pk': pk
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "PortalUserForm":
            obj=UserBase.objects.get(pk=pk)
            form=UserPortalForm(request.POST, request.FILES, instance=obj) 
            if form.is_valid():
                form.save()                   
                return JsonResponse({'success':_('Portal User has been updated')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/profile/single-form.html', { 
                    'form': form,
                    'form_name': form_id,
                    'pk': pk
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "login":
            form = LoginForm(request.POST or None)
            redirectUrl = f'http://portal.localhost:8000/console'
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user) 
                    return JsonResponse({
                        'success': redirectUrl
                    })
                else:
                    return JsonResponse({'alert': _('The data entered is not in our records')})
            else: 
                print(form.errors)
                return JsonResponse({'failed': _('Incorrect username or password')})
            
        if form_id == "sign-up":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password1'])
                user.is_active = False
                user.save()
                if UserBase.objects.filter(newsletter=True):
                    data = DataEmail.objects.filter(email=user.email)
                    if data.exists():
                        pass
                    else:
                        DataEmail.objects.create(
                            email = user.email,
                            date = timezone.now()
                    ) 
                current_site = get_current_site(request)
                subject = _('Activate your account')
                html_content = render_to_string('email_template/registration/registration_confirm.html', {
                            'user': user,           
                            'domain': 'stela.localhost:8000',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_EMAIL,
                    [user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                subject = _('New User On Your Site')
                html_content = render_to_string('email_template/registration/alert.html', {
                            'user': user,           
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.STELA_EMAIL,
                    [settings.DEFAULT_EMAIL]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                html_success = render_to_string('stela_control/load-data/auth/signup/success_register.html', { 
                    'email': user.email,
                })
                return JsonResponse({'success': _('Ok'), 'formset_html': html_success})
            else:
                html_alert = render_to_string('stela_control/load-data/auth/signup/register_errors_v1.html', { 
                    'form': form
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': html_alert})

        if form_id == "send_reset":
            form = PwdResetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['email']
                user_email = UserBase.objects.filter(email=data)
                if user_email.exists():
                    for user in user_email:
                        current_site = get_current_site(request)
                        subject = _('Password Reset')
                        html_content = render_to_string('email_template/password_reset/password_reset.html', {
                            'user': user,       
                            'email': user.email,    
                            'domain': 'stela.localhost:8000',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        text_content = strip_tags(html_content)

                        email = EmailMultiAlternatives(
                            subject,
                            text_content,
                            settings.DEFAULT_EMAIL,
                            [user.email]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                        return JsonResponse({'granted': _('The password reset link has been sent to your email')})
                else:
                    return JsonResponse({'alert_pw': _('The email entered is not registered')})
            else:
                return JsonResponse({'alert_pw': _('Enter a valid email address.')})

        if form_id == "reset_password":
            uid = request.POST.get('id')
            user = UserBase.objects.get(pk=uid)
            form = PwdResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'granted': _('The password has been saved successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/auth/pw_reset/form_errors.html', { 
                    'form': form
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            
def new_password_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except Exception as e:
        user = None
        print(e)

    if user is not None and account_activation_token.check_token(user, token):
        print('validated')
        form = PwdResetConfirmForm(user)
        return render(request, 'home/auth/password_reset/index.html', {
            'form': form,
            'uid': uid
            })
    else:
        print('expired')
        return render(request, 'home/auth/password_reset/index.html', {
            'expired': 'ok',
            })

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        external_url = 'http://portal.localhost:8000/console'
        return HttpResponseRedirect(external_url)
    else:
        return render(request, 'home/auth/registration/activation_invalid.html') 
            
def bookingData(request):
    if request.method == 'POST':
        owner=UserBase.objects.get(is_superuser=True)
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "consulting_appointment":
            form=BookingConsultingForm(request.POST)
            if form.is_valid():
                booking_list = Booking.objects.filter(owner=owner, date=form.cleaned_data['schedule'])
                if booking_list.count() > 10:
                    return JsonResponse({'alert':_('There is no availability for the selected day, please choose another.')})  
                else:
                    data = Booking()
                    data.owner = owner
                    data.name = form.cleaned_data['name']
                    data.address = form.cleaned_data['address']
                    data.phone = form.cleaned_data['phone']
                    data.email = form.cleaned_data['email']
                    data.type = form.cleaned_data['type']
                    data.date = form.cleaned_data['schedule']
                    data.dateConfirm = True
                    data.save()
                    services = request.POST.getlist('services[]')
                    for service in services:
                        BookingServices.objects.create(
                            parent=data,
                            service=service
                        )
                    return JsonResponse({'success':_('Your appointment has been successfully scheduled.')})  
              
def inputsData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        field_value = request.POST.get('field_value')
        field_name = request.POST.get('field_name')
        regex_patterns = {
            'name': r'^[a-zA-Z\s]+$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'address': r'.+', 
        }

        if action == "validateBillingData":
            
            if field_name == "phone":
                try:
                    phone_number = phonenumbers.parse(field_name)
                    if not phonenumbers.is_valid_number(phone_number):
                        response = JsonResponse ({
                        'status': 'error',
                        'field': field_name,
                        'message':_(f'{field_name} is not a valid number')
                    })
                    response = JsonResponse ({'status': 'success'})
                    
                except:
                    response = JsonResponse ({
                        'status': 'error',
                        'field': field_name,
                        'message':_(f'{field_name} is not a valid number')
                    })
            else:
                pattern = regex_patterns.get(field_name)

                if pattern and re.fullmatch(pattern, field_value):

                    response = JsonResponse ({'status': 'success'})
                else:
                    response = JsonResponse ({
                        'status': 'error',
                        'field': field_name,
                        'message':_('The value entered in the field is not valid.')
                    })
                return response

def get_youtube_playlist_videos(request):

    if request.method == 'POST':
        action = request.POST.get('action')
        video_id =request.POST.get('videoID')
        print(action)

        if action == "loadPreview":
            obj_data = render_to_string('stela_control/load-data/youtube/video-preview.html', { 
                'video_id': video_id
            })
            return JsonResponse({'html': obj_data})

def jobApplication(request):
    if request.method == 'POST':        
        form_id = request.POST.get('form-id')
        print(form_id)
        
        if form_id == "job-submit":
            form=JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'success':_('Your job application has been send successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/job-application/error-form-v1.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

def coreHandlers(request):
    if request.method == 'POST':        
        action = request.POST.get('action')
        form_id = request.POST.get('form-id')
        print(action, form_id)
        
        if action == "loadPagesBlogV1":
            lang=request.LANGUAGE_CODE
            author = UserBase.objects.get(is_superuser=True)
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            blog_posts = Content.objects.filter(author=author, section="Blog Post", lang=lang)[starts:ends]
            new_pages = render_to_string('stela_control/load-data/handlers/blog/blog-pages-v1.html', {
                    'blog_posts': blog_posts,
                    })
            return JsonResponse({'response': new_pages})

        if form_id == "blog-searchV1":
            q=request.POST.get('search-data')
            blog_posts=Content.objects.filter(title=q)
            if blog_posts:
                new_pages = render_to_string('stela_control/load-data/handlers/blog/blog-pages-v1.html', {
                        'blog_posts': blog_posts
                        })
            else:
                new_pages = render_to_string('stela_control/load-data/handlers/blog/empty-blog.html')
            return JsonResponse({'response': new_pages})
        
        if form_id == "commentForm":
            lang=request.LANGUAGE_CODE
            pk=request.POST.get('pk')
            post=Content.objects.get(pk=pk)
            form=CommentsFormBlog(request.POST)
            if form.is_valid():
                data=form.save(commit=False)
                data.post = post
                data.lang = lang
                data.save()

                return JsonResponse({'success':_('Your comment has been send successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/form.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "contact-submit":
            form=ContactForm(request.POST)
            if form.is_valid():
                form.save()
                
                return JsonResponse({'success':_('Your message has been send successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/contact/form.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

