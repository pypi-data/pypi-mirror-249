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
from stela_control.models import (
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
from stela_control.forms import (
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

def requestAPI(request): 
    action = request.POST.get('action')
    form_id = request.POST.get('form-id')
    obj = request.POST.get('queryid')
    print(action, form_id)
    if not obj:
        obj = 0

    stelaquery=ProStelaData.objects.filter(pk=obj)
        
    if action == 'callProStelaCustom':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="custom",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                  
    if action == 'callProStelaContent':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en redacción de contenido'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en redacción de contenido'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="Content Chats",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    print(e)
                    return JsonResponse({
                        'alert2': 'event'
                        })

    if action == 'callProStelaMarketing':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="Marketing Chats",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                                 
    if action == 'callStelaSight':
        url = []
        prompt = str(request.POST.get('prompt'))
        qty = int(request.POST.get('qty'))
        openai.api_key = settings.API_KEY
        response = openai.Image.create(
            prompt=prompt,
            n=qty,
            size="512x512"
            )
        for obj in response['data']:
            url.append(obj['url'])
        
        images_html = render_to_string('stela_control/load-data/meta/stela-sight/data.html', {
                        'url': url,
                        })
        return JsonResponse({'success': images_html})
    
    if action == "smartHashtag":
        hashdata = []
        userdata = []
        placesdata = []
        keyword = str(request.POST.get('qs'))
        keyword_findall = ''.join(re.findall(r'\w+', keyword))
        clean_keyword = keyword_findall.lower()
        url = "https://instagram-data12.p.rapidapi.com/search/"

        querystring = {
            "query":clean_keyword
            }

        headers = {
            "X-RapidAPI-Key": settings.KEYHUB,
            "X-RapidAPI-Host": settings.HUBHOST
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        print(data)
        hashtags = data['hashtags'][:5]
        users = data['users'][:5]
       
        for list in hashtags:
            hashdata.append(list['hashtag'])

        for list in users:
            userdata.append(list['user'])

        boost_html = render_to_string('stela_control/load-data/meta/smart-boost/index.html', {
                        'hashtags': hashdata,
                        'users': userdata,
                        })
        return JsonResponse({'success': boost_html})
    
    if action == "callStelaChat":
        start_time = time.time()
        obj = request.POST.get('queryid')
        text=ProStelaData.objects.get(id=obj)
        messages=ast.literal_eval(text.storage_data)
        chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                'messages': messages,
                'user': request.user,
                })

        return JsonResponse({'response': chat_html, 'qs':text.pk})
    
    if action == "deleteQuery":
        obj = request.POST.get('queryid')
        query=ProStelaData.objects.get(id=obj)
        query.delete()
        
        return JsonResponse({'success': 'response'})
    
    if action == "cityCheck":
        country_id = request.POST.get('country_id')
        cities = City.objects.filter(country_id=country_id)
    
        return render(request, 'render/city_data.html', {'cities': cities})

    if action == "checkUserTokenForm":
        form=RegistrationForm()
        obj_data = render_to_string('stela_control/load-data/single-form.html', {
            'form': form,    
        })    
        return JsonResponse({'content': obj_data})
        
    if form_id == "newUserToken":
        form=RegistrationForm(request.POST, request.FILES)  
        if form.is_valid():
            usertoken=form.save(commit=False)
            payload = {
                'user_id': usertoken.pk,
                'exp': datetime.datetime.utcnow() + timedelta(days=60), 
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            usertoken.api_token = token
            usertoken.is_active = True
            usertoken.set_password(form.cleaned_data['password1'])
            usertoken.save()
            return JsonResponse({'success':_('API Client was created successfully')})
        else:
            print(form.errors)
            obj_data = render_to_string('stela_control/load-data/registration/forms/register-form.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

def billingData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        formset_kwargs = {'form_kwargs': {'request': request}}
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "loadPreview":
            recipt_pk=request.POST.get('reciptID')
            print(recipt_pk)
            recipt=BillingRecipt.objects.get(pk=recipt_pk)
            obj_data = render_to_string(f'stela_control/load-data/billing/recipt-data.html', { 
                    'recipt': recipt
                }) 
            return JsonResponse({'data': obj_data})
        
        if action == "editRecipt":
            recipt_pk=request.POST.get('reciptID')
            recipt=BillingRecipt.objects.get(pk=recipt_pk)
            customer=Customer.objects.get(pk=recipt.customer.pk)
            customer_form = CustomerForm(instance=customer)
            form=BillingForm(instance=recipt)
            get_formset = inlineformset_factory(
                BillingRecipt, ItemServices, 
                form=BillingChargeFormDynamic, 
                extra=0, 
                can_delete=True,
            )
            get_formset2 = inlineformset_factory(
                BillingRecipt, ItemDiscount, 
                form=BillingDiscountForm, 
                extra=0, 
                can_delete=True,
            )
            obj_data = render_to_string(f'stela_control/load-data/billing/form-billing.html', { 
                    'form': form,
                    'customer_form': customer_form,
                    'formset':get_formset(**formset_kwargs, prefix='charge', instance=recipt),
                    'formset2': get_formset2(instance=recipt),
                    'pk': recipt.pk,
                }) 
            return JsonResponse({'data': obj_data})

        if action == 'generateRecipt':
            id=request.POST.get('pk')
            recipt=BillingRecipt.objects.filter(pk=id)
            controlbudget=BillingRecipt.objects.filter(is_budget=True, is_generated=True, payment_option="USD").count() + 1
            controlbilling=BillingRecipt.objects.filter(is_generated=True, payment_option="USD").exclude(is_budget=True).count() + 1
            
            if recipt[0].option == 'budget':
                control_id='BU-'+ str(controlbudget)            
                control_bu=InvoiceControl.objects.filter(control_id=control_id)
                if control_bu.exists():
                    obj_data = render_to_string('stela_control/load-data/alerts/budget-alert.html', {
                            
                    })
                    response = JsonResponse({'budget': _('This budget is registered'), 'html': obj_data})
                    return response
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt[0],
                        control_id=control_id,                  
                        )
                    recipt.update(
                        status="Dynamic Billing",
                        is_generated=True,
                        is_budget=True
                    )
                    obj_data = render_to_string('stela_control/load-data/alerts/budget-success.html', {
                            
                    })
                    response = JsonResponse({'success': _('Budget Generated Successfully'), 'html': obj_data})
                    return response

            else: 
                control_id='DB-'+ str(controlbilling)            
                control_in=InvoiceControl.objects.filter(control_id=control_id)
                if control_in.exists():
                    obj_data = render_to_string('stela_control/load-data/alerts/invoice-alert.html', {
                            
                    })
                    response = JsonResponse({'invoice': _('This invoice is registered'), 'html': obj_data})
                    return response
                
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt[0],
                        control_id=control_id,
                    )
                    recipt.update(
                        status="Dynamic Billing",
                        is_generated=True
                        
                    )
                    obj_data = render_to_string('stela_control/load-data/alerts/invoice-success.html', {
                            
                    })
                    response = JsonResponse({'success': _('Invoice Generated Successfully'), 'html': obj_data})
                    return response

        if action == 'cancelRecipt':
            try:
                reciptid=request.POST.get('pk')
                recipt=BillingRecipt.objects.filter(pk=reciptid).update(status='Cancelled')
                obj_data = render_to_string('stela_control/load-data/alerts/cancel-recipt.html', {
                            
                    })    
                response = JsonResponse({'success': _('Cancellation request successful'), 'html': obj_data})
                return response
            except Exception as e:
                response = JsonResponse({'alert': e})
                return response
        
        if action == 'Payeed':
            try:
                reciptid=request.POST.get('pk')
                recipt=BillingRecipt.objects.filter(pk=reciptid).update(status='Payeed')
                getRecipt=BillingRecipt.objects.get(id=reciptid)
                get_code=str('DP')+get_random_string(8).upper()
                validator=get_random_string(20).lower()
                subtotal=getRecipt.amount 
                taxes=subtotal * Decimal(0.1)
                total=subtotal+taxes
                username=request.user.username
                user=UserBase.objects.get(username=username)
                fetch=StelaPayments(
                    user=user,
                    key_validator=validator,
                    transaction_id=get_code,
                    payment_option='Direct Pay',
                    subtotal=subtotal,
                    taxes=taxes,
                    total_paid=total,
                    profit=subtotal * Decimal(0.30),
                    host="Emmerut"
                )
                fetch.save()
                obj_data = render_to_string('stela_control/load-data/alerts/payeed-recipt.html', {
                            
                    }) 
                response = JsonResponse({'success': _('Recipt status update successful'), 'html': obj_data})
                return response
            except Exception as e:
                response = JsonResponse({'failed': e})
                return response

        if action == 'billCust':
            userid=request.POST.get('userid')
            try:
                customer = Customer.objects.get(userid=userid)
                customer_form = CustomerForm(instance=customer)
                customer_data = render_to_string('stela_control/billing/sections/bill-data-customer.html', {
                            'customer_form': customer_form      
                })
                response = JsonResponse({'costumer': customer_data})
                return response
            except:
                response = JsonResponse({'notfound': _('The client is not in your records.')})
                return response

        if action == 'emailSend':
            pass

        if action == 'delete':
            objects_ids = request.POST.getlist('id[]')
            for id in objects_ids:
                object=BillingRecipt.objects.get(id=id)
                object.delete()
                try:
                    order=Order.objects.get(billing=id)
                    order.delete()
                except:
                    pass
                try:
                    payment=StelaPayments.objects.get(billing=id)
                    payment.delete(using="master")
                except:
                    pass
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "submit-billing":
            form = BillingForm(request.POST)
            customer_form = CustomerForm(request.POST)
            get_formset = inlineformset_factory(
                BillingRecipt, ItemServices, 
                form=BillingChargeFormDynamic, 
                extra=1, 
                can_delete=False,
            )
            get_formset2 = inlineformset_factory(
                BillingRecipt, ItemDiscount, 
                form=BillingDiscountForm, 
                extra=0, 
                can_delete=False,
            )
            formset = get_formset(request.POST, **formset_kwargs, prefix='charge')
            formset2 = get_formset2(request.POST)
            
            if all([form.is_valid(),
                    customer_form.is_valid(),
                    formset.is_valid(),
                    formset2.is_valid()
                ]):
                
                customer_data = customer_form.save(commit=False)
                costumer = Customer.objects.filter(userid=customer_data.userid)
                
                if costumer.exists():
                    costumer.update(
                        owner=request.user,
                        full_name=customer_data.full_name,
                        userid=customer_data.userid,
                        address=customer_data.address,
                        phone=customer_data.phone,
                        email=customer_data.email,
                        country_profile=customer_data.country_profile,
                    )
                else:
                    customer_data.owner = request.user
                    customer_data.save()
                customer_instance = Customer.objects.get(userid=customer_data.userid)
                parent = form.save(commit=False)
                parent.owner = request.user
                parent.customer = customer_instance
                parent.payment_option = "USD"
                parent.save()
        
                for form in formset:
                    get_service = str(form.cleaned_data['field'])
                    text_splitted = get_service.split(' - ')
                    get_qty = form.cleaned_data['qty']
                    service = Elements.objects.filter(title=text_splitted[0], parent__yearly=False, parent__type="Service", parent__lang=lang).exclude(price=0).first()
                    amount = service.price * get_qty
                    child = form.save(commit=False)
                    child.recipt_id = parent.id
                    child.field_id = service.pk
                    child.amount = amount
                    child.save()
                
                for form in formset2:
                    child = form.save(commit=False)
                    child.recipt_id = parent.id
                    child.save()
                

                get_amount = ItemServices.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                get_discounts = ItemDiscount.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                
                amount = get_amount['total']
                taxes = amount * Decimal(0.10)

                if get_discounts['total']:
                    discount = get_discounts['total']
                    BillingRecipt.objects.filter(id=parent.id).update(amount=amount, discount=discount)
                    recipt = BillingRecipt.objects.get(id=parent.id)
                    
                else:
                    discount = ''

                if parent.option == "Budget":
                    pass
                else:
                    BillingRecipt.objects.filter(id=parent.id).update(tax=taxes)

                BillingRecipt.objects.filter(id=parent.id).update(amount=amount)

                recipt = BillingRecipt.objects.get(id=parent.id)

                return JsonResponse({
                    'success':_('Your content was upload successfully'),
                    'reciptPk': recipt.pk
                    })
            else:
                print(form.errors)
                print(formset.errors)
                print(formset2.errors)
                obj_data = render_to_string(f'stela_control/load-data/biling/form-billing.html', { 
                    'form': form,
                    'customer_form': customer_form,
                    'formset':formset,
                    'formset2': formset2
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})    
            
        if form_id == "update-billing":
            billing_pk=request.POST.get('pk')
            billing_data=BillingRecipt.objects.get(pk=billing_pk)
            customer_data=Customer.objects.get(pk=billing_data.customer.pk)
            form = BillingForm(request.POST, instance=billing_data)
            customer_form = CustomerForm(request.POST, instance=customer_data)
            get_formset = inlineformset_factory(
                BillingRecipt, ItemServices, 
                form=BillingChargeFormDynamic, 
                extra=0, 
                can_delete=True,
            )
            get_formset2 = inlineformset_factory(
                BillingRecipt, ItemDiscount, 
                form=BillingDiscountForm, 
                extra=0, 
                can_delete=True,
            )
            formset = get_formset(request.POST, **formset_kwargs, prefix='charge', instance=billing_data)
            formset2 = get_formset2(request.POST, instance=billing_data)
            
            if all([form.is_valid(),
                    customer_form.is_valid(),
                    formset.is_valid(),
                    formset2.is_valid()
                ]):
                customer_data = customer_form.save(commit=False)
                costumer = Customer.objects.filter(userid=customer_data.userid)
                
                if costumer.exists():
                    costumer.update(
                        owner=request.user,
                        full_name=customer_data.full_name,
                        userid=customer_data.userid,
                        address=customer_data.address,
                        phone=customer_data.phone,
                        email=customer_data.email,
                        country_profile=customer_data.country_profile,
                    )
                else:
                    customer_data.owner = request.user
                    customer_data.save()
                customer_instance = Customer.objects.get(userid=customer_data.userid)
                parent = form.save(commit=False)
                parent.owner = request.user
                parent.customer_id = customer_instance.pk
                parent.payment_option = "USD"
                parent.save()

                instances = formset.save(commit=False)
                            
                for obj in formset.deleted_objects:
                            obj.delete()
                            
                for instance in instances:
                    get_service = str(instance.field)
                    text_splitted = get_service.split(' - ')
                    service = Elements.objects.get(title=text_splitted[0]) 
                    get_qty = instance.qty
                    amount = service.price * get_qty
                    instance.amount = amount
                    instance.save()

                instances2 = formset2.save(commit=False)

                for obj in formset2.deleted_objects:
                    obj.delete()

                for instance in instances2:
                    instance.save()
                
                get_amount = ItemServices.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                get_discounts = ItemDiscount.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                
                amount = get_amount['total']
                taxes = amount * Decimal(0.10)

                if get_discounts['total']:
                    discount = get_discounts['total']
                    BillingRecipt.objects.filter(id=parent.id).update(amount=amount, discount=discount)
                    recipt = BillingRecipt.objects.get(id=parent.id)
                    
                else:
                    discount = ''

                if parent.option == "Budget":
                    pass
                else:
                    BillingRecipt.objects.filter(id=parent.id).update(tax=taxes)

                BillingRecipt.objects.filter(id=parent.id).update(amount=amount)

                recipt = BillingRecipt.objects.get(id=parent.id)

                return JsonResponse({
                    'success':_('Your content was upload successfully'),
                    'reciptPk': recipt.pk
                    })
            else:
                print(form.errors, 'form')
                print(formset.errors, 'formset')
                print(formset2.errors, 'formset2')
                obj_data = render_to_string(f'stela_control/load-data/biling/form-billing.html', { 
                    'form': form,
                    'customer_form': customer_form,
                    'formset':formset,
                    'formset2': formset2
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            
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

def contentData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        section = request.POST.get('section')
        ckeditor = request.POST.get('ckeditor')
        form_name = request.POST.get('check')
        remove = request.POST.get('remove')
        is_cke = request.POST.get('is_cke')
        action = request.POST.get('action')
        print(form_id, form_name, is_cke, action, section, ckeditor, remove)      
        
        if form_name:
            form_class = get_form_class_by_name(form_name)
            content=Content.objects.filter(author=author, section=action, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=form_class,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section=action))
                obj_data = render_to_string(f'stela_control/load-data/maincontent/update_forms/{form_name}.html', { 
                    'formset': formset,
                    'form_name': form_name,
                    'section': action   
                })
                if ckeditor:
                    response = JsonResponse({'content': obj_data, 'cke': ckeditor})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string(f'stela_control/load-data/maincontent/forms/{form_name}.html', { 
                    'formset': get_formset(prefix='formset'),
                    'form_name': form_name,
                    'section': action
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response

        if form_id:
            form_name = form_id
            form_class = get_form_class_by_name(form_name)
            content=Content.objects.filter(author=author, section=section, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=form_class,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = section
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    print(form_name)
                    obj_data = render_to_string(f'stela_control/load-data/maincontent/error_forms/{form_name}.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                        'form_name': form_name,
                        'section': section
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _(f'Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = section
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string(f'stela_control/load-data/maincontent/error_forms/{form_name}.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                        'form_name': form_name,
                        'section': section
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if remove:
            pk=request.POST.get('id')
            content=Content.objects.get(pk=pk)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
           
def docsData(request): 
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        is_cke = request.POST.get('is_cke')
        ckeditor = request.POST.get('ckeditor')
        print(form_id, action, is_cke, ckeditor)
        
        if action == "checkDocs":
            pk=request.POST.get('pk')
            if pk:
                obj=SitePolicy.objects.get(pk=pk)
                form=PolicyForm(instance=obj)
                get_formset = inlineformset_factory(
                SitePolicy, LegalProvision, 
                form=LegalProvitionForm,
                extra=0, can_delete=True,
                )
                formset=get_formset(instance=obj, prefix='terms')

                obj_data = render_to_string('stela_control/load-data/site_docs/update_forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                                'pk': pk  
                    })

                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                form=PolicyForm()
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(prefix='terms')

                obj_data = render_to_string('stela_control/load-data/site_docs/forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                    })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response

        if action == "checkFAQ": 
            pk=request.POST.get('pk')
            if pk:   
                print(pk)
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(instance=content, prefix='formset')
                obj_data = render_to_string('stela_control/load-data/site_docs/update_forms/faq_form.html', { 
                    'form': form,
                    'formset':formset,   
                    'pk': pk
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                form=FAQForm()
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/site_docs/forms/faq_form.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response
        
        if action == "removeDoc":
            doc_id=request.POST.get('id')
            doc=SitePolicy.objects.get(pk=doc_id)
            doc.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeFAQ":
            content_id=request.POST.get('id')
            content=FAQ.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if form_id == "doc-form":
            update_form = request.POST.get('form-update')
            if update_form:
                form=PolicyForm(request.POST, instance=update_form)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='terms', instance=update_form)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=PolicyForm(request.POST)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='terms')
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "faq-form":
            pk = request.POST.get('form-update')
            if pk:
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(request.POST, instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()
                
                    instances = formset.save(commit=False)
                                
                    for obj in formset.deleted_objects:
                            obj.delete()
                                
                    for instance in instances:
                        instance.faq = parent
                        instance.save()
                        
                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=FAQForm(request.POST)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_empty_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
 
def stelaStoryData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "checkBlog":       
            form = BlogForm()
            obj_data = render_to_string('stela_control/load-data/maincontent/forms/blog_form.html', { 
                    'form': form
                })
            return JsonResponse({'empty': obj_data})
        
        if action == "postData":   
            postpk=request.POST.get('obj')    
            post = Content.objects.get(pk=postpk)
            obj_data = render_to_string('stela_control/load-data/stela_story/feed-item.html', { 
                    'post': post,
                    'usertz': get_timezone,
                })
            return JsonResponse({'content': obj_data})
        
        if action == "filter":   
            filter=request.POST.get('get_value')   
            feed=Content.objects.filter(author=author, lang=lang).order_by('-id')
            if filter in [_('News'), _('Tutorials'), _('Tips and Tricks'), _('Guides and Manuals'), _('Inspiration'), _('Events and Conferences'), _('Interviews')]:   
                filter_feed=feed.filter(category=filter)
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter in ['today', '15', '29']:
                if filter == 'today':
                    start_date = datetime.datetime.now().date()
                    end_date = start_date
                elif filter == '15':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=15)
                elif filter == '29':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=29)

                filter_feed=feed.filter(created__range=[start_date, end_date])
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter == '':
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})
            return response
        
        if action == "updateFeed":   
            pk = request.POST.get('feed_id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(instance=post)
            if post.is_schedule:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({
                        'content': obj_data,
                        'getDate': post.schedule
                    })
            else:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({'content': obj_data})
                
            return response
        
        if action == "removeObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Content.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if action == "loadPages":
            lang=request.LANGUAGE_CODE
            country_id = str(lang).split('-')
            get_timezone = country_timezones(country_id[1])[0] 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            print(starts)
            print(ends)
            new_posts = Content.objects.filter(author=author, lang=lang).order_by('-id')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/blog-feed.html', {
                    'feed': new_posts,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
        
        if form_id == "blog-form":
            form = BlogForm(request.POST, request.FILES)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if form_id == "blog-update":
            pk = request.POST.get('obj-id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(request.POST, request.FILES, instance=post)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
 
def staffData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        form_name = request.POST.get('form_name')
        pk = request.POST.get('pk')
        print(form_id, action, pk, form_name)

        if action == "checkStaff":   
            if pk:
                staff = Team.objects.get(pk=pk)    
                form = StaffForm(instance=staff)
                get_formset = inlineformset_factory(
                        Team, SocialLinks, 
                        form=SocialMediaForm,
                        extra=0, 
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset', instance=staff),
                        'pk': pk
                    })
                return JsonResponse({'content': obj_data})
            else:
                form = StaffForm()
                get_formset = inlineformset_factory(
                        Team, SocialLinks, 
                        form=SocialMediaForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'),
                        'pk': pk
                    })
                return JsonResponse({'empty': obj_data})
        
        if action == "removeStaff":
            pk=request.POST.get('id')
            staff=Team.objects.get(pk=pk)
            staff.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "staff-form":
            if pk:
                staff = Team.objects.get(pk=pk)
                form = StaffForm(request.POST, request.FILES, instance=staff)
                set_formset = inlineformset_factory(
                    Team, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset', instance=staff)
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.lang = lang
                    parent.save()

                    instances = formset.save(commit=False)
                                
                    for obj in formset.deleted_objects:
                            obj.delete()
                                
                    for instance in instances:
                        instance.parent_staff = parent
                        instance.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': formset,
                        'pk': pk,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form = StaffForm(request.POST, request.FILES)
                set_formset = inlineformset_factory(
                    Team, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent_staff = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': formset,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
                 
def inventoryData(request):
    if request.method == 'POST':
        data=request.POST.get('pk')
        lang=request.LANGUAGE_CODE
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        form_name = request.POST.get('form_name')
        formset_name = request.POST.get('formset_name')
        model_parent = request.POST.get('model_parent')
        model_child = request.POST.get('model_child')
        type = request.POST.get('type')
        cke = request.POST.get('is_cke')
        cke_formset = request.POST.get('is_cke_formset')
        ckeditor = request.POST.get('ckeditor')
        schedule = request.POST.get('schedule')
        formset_ckeditor = request.POST.get('formset_ckeditor')
        print(form_id, type, form_name, formset_name, action, model_parent, model_child, cke, ckeditor, cke_formset, formset_ckeditor)
    
        if form_name:
            form_class = get_form_class_by_name(form_name)
            formset_class = get_form_class_by_name(formset_name)
            class_parent = get_form_class_by_name(model_parent)
            class_child = get_form_class_by_name(model_child)
            if data:
                obj=Inventory.objects.get(pk=data)
                form=form_class(instance=obj)
                get_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=1 
                )
                if schedule and cke and cke_formset:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule
                    })
               
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'schedule': schedule,
                        'cke_formset': cke_formset,
                        })
                if schedule and cke:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'cke': cke,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule
                    })
               
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'schedule': schedule
                        })
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'cke': cke,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        })
                else:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        })
            else:
                form=form_class()
                get_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                if schedule and cke:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule
                    })
               
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'schedule': schedule
                        })
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        })
                    
                elif cke and cke_formset:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'cke_formset': cke_formset
                        })
                    
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        })
                else:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        })
            return response

        if form_id:
            products=Variant.objects.all()
            sku_count=products.count() + 1 
            form_class = get_form_class_by_name(form_id)
            formset_class = get_form_class_by_name(formset_name)
            class_parent = get_form_class_by_name(model_parent)
            class_child = get_form_class_by_name(model_child)
            if data:
                service=Inventory.objects.get(pk=data)
                set_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=True,
                    )
                form = form_class(request.POST, request.FILES, instance=service)  
                formset = set_formset(request.POST, request.FILES, instance=service, prefix='formset')  
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                        parent = form.save(commit=False)
                        if type == "Product":
                            cat_id = form.cleaned_data['category']
                            category=Category.objects.get(pk=cat_id.pk)
                            get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                            parent = form.save(commit=False)
                            parent.category = category
                            parent.sku = get_code
                        parent.owner = request.user
                        parent.type = type
                        parent.lang = lang
                        parent.save()
                            
                        instances = formset.save(commit=False)
                                
                        for obj in formset.deleted_objects:
                                obj.delete()
                                
                        for instance in instances:
                            instance.parent = parent
                            instance.save()

                        return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    if schedule and ckeditor:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'schedule':schedule})
                    elif schedule:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'schedule':schedule})
                    
                    elif ckeditor and formset_ckeditor:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'cke': ckeditor,
                        'cke_formset': cke_formset,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'cke_formset': cke_formset})

                    elif ckeditor:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'cke': ckeditor,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form = form_class(request.POST, request.FILES)
                set_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    if type == "Product":
                        cat_id = form.cleaned_data['category']
                        category=Category.objects.get(pk=cat_id.pk)
                        get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                        parent = form.save(commit=False)
                        parent.category = category
                        parent.sku = get_code
                    parent.owner = request.user
                    parent.type = type
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    if schedule and ckeditor:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'schedule':schedule})
                    elif schedule:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'schedule':schedule})
                    elif ckeditor:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'cke': ckeditor,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_class,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Inventory.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
               
def sendgridData(request, id, ig):
    ig_account=InstagramAccount.objects.get(asset_id=ig)
    if request.method == 'POST':
        action = request.POST.get('form-id')
        lang=request.LANGUAGE_CODE
        call = request.POST.get('action')
        print(action)
        print(call)

        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'date': timezone.now(),
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if action == "sendmetric-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your IG Analyzer was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if call == "loadPages":
            get_timezone = request.POST.get('zone') 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = IGPost.objects.filter(parent=ig_account).order_by('-schedule')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/meta/ig-new-pages.html', {
                    'newposts': new_posts,
                    'instagram': ig_account,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
