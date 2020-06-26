from django.shortcuts import render, redirect

from mailmerge import MailMerge

from datetime import date, datetime
from datetime import timedelta
from .forms import LoginForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, logout, authenticate

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Create your views here.

from django.views.generic import ListView, DetailView

from .models import Zgrada, Stanar, Reklama, Oglasivac, RacunStanara, RacunReklama, RezultatiTreptanja

import face_recognition
import cv2 
import os
from PIL import Image
import time

import numpy as np
import dlib
from math import hypot


def blinkstat(request):
    context = {'lista': RezultatiTreptanja.objects.order_by('-number_of_blinks')}
    return render(request, 'blog/blinkstatistic.html', context)


def blinkanalysis(request):
    import subprocess
    context = {'lista': RezultatiTreptanja.objects.order_by('-number_of_blinks')}
    print(RezultatiTreptanja.objects.order_by('-number_of_blinks'))
    messages.info(request, "Kada pročitate ceo tekst, pritisnite ESC taster na tastaturi!")
    try:
        print("pozivam blink funkciju!!!")
        subprocess.Popen(["python","skriptablink.py", str(request.user)])
        raise SystemExit()
        
    except KeyboardInterrupt:
        print ("Quit...")
        
    finally:
        return render(request, 'blog/blinkanalysis.html', context)


def facedect(user, loc):
        cam = cv2.VideoCapture(0)

        cam.set(3, 1280)
        cam.set(4, 720)

        for i in range(15):
            a, temp = cam.read()

        #time.sleep(2)

        s, img = cam.read()
        if s:   
                
                #slika iz galerije, obrada:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                print('basedir:', BASE_DIR)
                MEDIA_ROOT =os.path.join(BASE_DIR, loc)

                loc=str(MEDIA_ROOT)
                print(loc)

                #IZ GALERIJE POZNATIH SLIKA, ODNOSNO ONA SLIKA USER-a KONKRETNOG, IZ MEMORIJE
                image_from_galery = face_recognition.load_image_file(loc)
                face_locations_from_galery = face_recognition.face_locations(image_from_galery)
                print(face_locations_from_galery)
                print(f'There are {len(face_locations_from_galery)} people in image from galery')
                face_galery_encoding = face_recognition.face_encodings(image_from_galery)[0]
                print(face_galery_encoding)

                #SA KAMERE
                image_from_camera = img


                face_locations_from_camera = face_recognition.face_locations(image_from_camera)
                print(face_locations_from_camera)
                if len(face_locations_from_camera) != 1:
                    pil_image = Image.fromarray(image_from_camera)
                    pil_image.save(f'{BASE_DIR}\\upravnik\\LOGINs\\FAIL\\{user}{str(date.today())}2.jpg')
                    return False
                print(f'There are {len(face_locations_from_camera)} people in image from camera')
                face_camera_encoding = face_recognition.face_encodings(image_from_camera)[0]
                print(face_camera_encoding)

                check=face_recognition.compare_faces([face_galery_encoding], face_camera_encoding)
                

                print(check)
                if check[0]:
                    pil_image = Image.fromarray(image_from_camera)
                    pil_image.save(f'{BASE_DIR}\\upravnik\\LOGINs\\SUCCESS\\{user}{str(date.today())}2.jpg')
                    return True
                    #{user}-{str(datetime.today())}.jpg

                else :
                    pil_image = Image.fromarray(image_from_camera)
                    pil_image.save(f'{BASE_DIR}\\upravnik\\LOGINs\\FAIL\\{user}{str(date.today())}2.jpg')
                    return False    


def loginPage(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pw = request.POST['password']

        user = authenticate(request, username = user, password = pw) # vraca User-a ako se gadjaju username i password, u suprotnom None
        print('user:', user)
        if user is not None:
            print('pre login-a:', request.user)  #AnonymousUser
            print(user.stanar.profile_pic.url)
            if facedect(user, user.stanar.profile_pic.url):
                login(request, user)
                print('USPEO SI, uporedio je lepo slike i prosao si dalje')
            else:
                print('NISI USPEO, nije lepo uporedio slike')
                return redirect('login')
            print('nakon login-a:', request.user)  #duletbg
            messages.success(request, 'Uspešno ste se prijavili na sistem!')
            return redirect('blinkstat')
        else:
            messages.error(request, 'Pogresili ste! Pokusajte ponovo')

        #mojusr = User.objects.get(username='duletbg')


    context = {}
    return render(request, 'blog/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'Odjavili ste se!')
    return render(request, 'blog/logout.html')

#@unauthenticated_user
def register(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    form = MyUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            usr = form.save()

            customer_group = Group.objects.get(name = 'customer')
            usr.groups.add(customer_group)
            Customer.objects.create(user = usr)
            print('forma sacuvana:', usr)
            messages.info(request, 'Cestitamo! Napravili ste account. Molimo da se prijavite')
            return redirect('/login')
    context = {'form': form}
    return render(request, 'blog/register.html', context)

@login_required(login_url='login')
def kreirajracune(request, pk):
    stanari = Zgrada.objects.get(id = pk).stanari.all()
    for stanar in stanari:
        template = "template2.docx"
        document = MailMerge(template)
        print(document.get_merge_fields())
        document.merge(PrezimeIme = stanar.prezime, DanasnjiDatum = str(date.today()), RokPlacanja = str(date.today() + timedelta(days=15)), UgovornaCena = str(stanar.mesecniIznos), Zgrada = stanar.zgrada.ulica + " " + str(stanar.zgrada.broj), BrStana = str(stanar.brojStana), UkupnaCena = str(stanar.mesecniIznos + stanar.dugovanje), Dugovanje = str(stanar.dugovanje))

        document.write('test-'+ str(stanar.prezime) + '.docx')
        print('upisano!!!')


    return render(request, 'blog/kreirajracune.html')

class ZgradaListView(ListView):
    model = Zgrada
    context_object_name = 'zgrade'

    def get_queryset(self):
        queryset = Zgrada.objects.all()
        ulica = self.request.GET.get("ulica")
        if ulica:
            if(ulica != ''):
                queryset = Zgrada.objects.filter(ulica__icontains = ulica)
        
        return queryset

class ZgradaDetailView(DetailView):
    model = Zgrada
    
class StanarListView(ListView):
    model = Stanar
    context_object_name = 'stanari'

    def get_queryset(self):
        queryset = Stanar.objects.all()
        prezime = self.request.GET.get("prezime")
        sort = self.request.GET.get("sort")
        print(sort)

        if prezime:
            if(prezime != ''):
                queryset = Stanar.objects.filter(prezime__icontains = prezime)
        
        if(sort == "iznosDugovanjaOpadajuce"):
            queryset = queryset.order_by('-dugovanje')
        elif(sort == 'iznosDugovanjaRastuce'):
            queryset = queryset.order_by('dugovanje')
        elif(sort == 'mesecniIznosOpadajuce'):
            queryset = queryset.order_by('-mesecniIznos')
        elif(sort == 'mesecniIznosRastuce'):
            queryset = queryset.order_by('mesecniIznos')
        return queryset

class StanarDetailView(DetailView):
    model = Stanar

class ReklamaListView(ListView):
    model = Reklama
    context_object_name = 'reklame'

class ReklamaDetailView(DetailView):
    model = Reklama

class OglasivacListView(ListView):
    model = Oglasivac
    context_object_name = 'oglasivaci'

class OglasivacDetailView(DetailView):
    model = Oglasivac

class RacuniStanariListView(ListView):
    model = RacunStanara
    context_object_name = 'racuni'

class RacuniStanariDetailView(DetailView):
    model = RacunStanara

class RacuniReklamaiListView(ListView):
    model = RacunReklama
    context_object_name = 'racuni'

class RacunireklamaiDetailView(DetailView):
    model = RacunReklama

