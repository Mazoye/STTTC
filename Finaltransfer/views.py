from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from PIL import Image
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import cv2
import os
from django.conf import settings
import random
from django.core.mail import send_mail


def handelLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("send_file")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("index")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('index')

    else:
        return HttpResponse("404 - Not found")

def forgot_password(request):
    username = str(request.POST.get('name'))
    u = User.objects.get(username=username);

    s="12345678"
    '''
    for i in range(8):
        s += a[r.randint(0, 75)]
    '''
    u.set_password(s);
    u.save()

    user = authenticate(username=username, password=s)
    login(request, user)
    email=request.user.email
    logout(request)
    subject = "Login Credentials of STTTC"
    body = f"""Hello {username},
Your Newly Genarated Password is {s} you can change it any time."""

    send_mail(
        subject,
        body,
        'sssgjc123@gmail.com',
        [email],
        fail_silently=False,
    )
    return HttpResponse("done")

def home(request):
        return(render(request,'home.html'))

def index(request):
     return (render(request, 'index.html'))
def send_file(request):
    if (str(request.user) != "AnonymousUser"):
        return(render(request,'send_file.html'))
    else:
        return (render(request, 'index.html'))


def encryption(text,d,a):
    if a==1:
        t=list(text[::-1])
        for i in range(len(t)):
            t[i]=chr(ord(t[i])+i)

    elif a==2:
        t=list(text[::-1])
        for i in range(len(t)):
            if(i%2==0):
                t[i]=chr(ord(t[i])+len(t))
            else:
                t[i] = chr(ord(t[i])-len(t))

    elif a==3:
        t=list(text)
        for i in range(len(t)):
            if(i%2==0):
                t[i]=chr(ord(t[i])+ord(chr(i*10).upper()))
            else:

                t[i]=chr(ord(t[i])+len(t)+ord(chr(i*10).upper()))

    elif a==4:
        t=list(text)
        n=len(t)-1
        for i in range(len(t)):
            t[i]=chr(ord(t[i])+n)
            n-=1

    elif a==5:
        t=list(text[::-1])
        for i in range(len(t)):
            f=(ord(chr(i))+len(t))//10
            t[i] = chr(ord(t[i])+f)
    t.insert(d, str(chr(a*10)))
    new_text = "".join(t)
    return(new_text)

def encrypt_data(request):
    text=str(request.POST.get("tid"))

    d=len(text)//10
    a= random.randint(1,5)
    z= encryption(text,d,a)


    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=1)
    qr.add_data(z)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white').convert('RGB')



    # To add image in center
    logo_display = Image.open("static//STTTC.png")
    logo_display.thumbnail((65,65))
    logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
    img.paste(logo_display, logo_pos)


    # save the Qrcode
    img.save('static/qrcode.png')

    return HttpResponse(z)


def uploadqr(request):
    file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'qrdecrypt.png')
    if os.path.exists(file_upload_dir):
        os.remove(file_upload_dir)

    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save("qrdecrypt.png", upload)
        return render(request, 'send_file.html')
    return render(request, 'send_file.html')

def decryption(decodedText):
    v=len(decodedText)-1
    d=v//10
    li=list(decodedText)
    a=ord(li[d])//10
    c=""
    s1=decodedText[:d]
    s2=decodedText[(d + 1):]
    s3=s1+s2
    if a==1:
        for i in reversed(range(v)):
            c+=chr(ord(s3[i])-i)
    elif a==2:
        for i in reversed(range(v)):
            if (i % 2 == 0):
                c+= chr(ord(s3[i])-v)
            else:
                c+= chr(ord(s3[i])+v)
    elif a==3:
        for i in range(v):
            if(i%2==0):
                c+=chr(ord(s3[i])-ord(chr(i*10).upper()))
            else:
                c+=chr(ord(s3[i])-v-ord(chr(i*10).upper()))
    elif a==4:
        g=v-1
        for i in range(v):
            c+=chr(ord(s3[i])-g)
            g-=1
    elif a==5:
        for i in reversed(range(v)):
            f=(ord(chr(i))+v)//10
            c+=chr(ord(s3[i])-f)
    return c

def decrypt(request):
    file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'qrdecrypt.png')

    image = cv2.imread(file_upload_dir)
    qrCodeDetector = cv2.QRCodeDetector()

    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    if points is not None:
        pass
    else:
        decodedText="Error Occurred"

    if(decodedText!="Error Occurred"):
        z=decryption(decodedText)
        return HttpResponse(z)
    return HttpResponse(decodedText)


