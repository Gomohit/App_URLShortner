import string

from django.shortcuts import render, redirect
from django.db import connection
from django.core.mail import send_mail
import random



# Create your views here.
def xyz(request):
    return render(request, "home1.html")


def signup(request):
    email = request.POST['emailname']
    psw = request.POST['pswname']
    cno = request.POST['contactno']
    fname = request.POST['firstname']
    lname = request.POST['lastname']

    cursor = connection.cursor()
    query1 = "select * from users where email=%s"
    value1 = email
    cursor .execute(query1, value1)
    data = cursor.fetchall()

    if len(data) > 0:
        data = {"email": "already signed up", "password": "", "contact": "", "firstname": "", "lastname": ""}
        return render(request, "first.html", data)
    else:
        otp = random.randint(100000, 999999)
        strotp = str(otp)
        print(strotp)
        query2 = "insert into users (email ,password,contact, firstname,lastname,otp) values (%s,%s,%s,%s,%s,%s)"
        value2 = (email, psw, cno, fname, lname, strotp)
        cursor.execute(query2, value2)
        print(cursor.rowcount)
        body = 'your otp for our portal you signed up with email ' + email + ' is ' + strotp
        send_mail('OTP For Verification', body, 'mgbehror4@gmail.com', [email])
        data = {'email': email, 'password': psw, 'contact': cno, 'firstname': fname, 'lastname': lname}
        return render(request, "signupsuccess.html", data)

    # query = "Select * from city where name='"+email+"'"
    # cursor.execute(query)
    # row = cursor.fetchone()
    # print(row)


def signin(request):
    return render(request, "login.html")




def login(request):
    email = request.POST['emailname']
    psw = request.POST['pswname']
    cno = request.post['contactno']

    cursor = connection.cursor()
    query1 = "select * from users where email=%s"
    value1 = email
    cursor.execute(query1, value1)
    data = cursor.fetchone()
    if data is None:
        data = {"email": "not signed up", "password": ""}
        return render(request, "first.html", data)
    else:
        if data[2] == 0:
            data = {"email": "you are not a verified user", "password": ""}
            return render(request, "first.html", data)
        if data[1] == psw:
            data = {"email": "Login Success", "password": ""}
            return render(request, "first.html", data)

        else:
            data = {"email": "password is not correct", "password": ""}
            return render(request, "first.html", data)

def otpVerification(request):
    email = request.POST['emailname']
    otp = request.POST['otp']
    cursor = connection.cursor()
    query1 = "select * from users where email=%s"
    value1 = email
    cursor.execute(query1, value1)
    data = cursor.fetchone()
    if data is not None:
        if data[6] == otp:
            query2 = "update users set is_verify=1 where email=%s"
            value2 = email
            cursor.execute(query2, value2)
            if cursor.rowcount == 1:
                print("otp verified successfully")
                data = {"email": "OTP VERIFIED Success"}
                return render(request, "first.html", data)
            else:
                data = {"email": "OTP is not correct"}
                return render(request, "first.html", data)

def  generateShortURL():
    letters = string.ascii_letters + string.digits
    shorturl = ''
    for i in range(6):
        shorturl = shorturl + "".join(random.choice(letters))
    return shorturl

def urlshortner(request):
    longlink = request.GET['link']
    customurl = request.GET['customurl']
    shorturl = ''
    if customurl is None or customurl == '':
        shorturl = ''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link=%s"
        value1 = customurl
        cursor.execute(query1, value1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email": "Already custom url exist please try other url"}
            return render(request, "first.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values (%s,%s)"
            value = (longlink, customurl)
            cursor.execute(query2, value)
            data = {"email": "Your url is shorten with classy.co/"+customurl}
            return render(request, "first.html", data)
    if shorturl is not None or shorturl != '':
        while True:
            shorturl = generateShortURL()
            cursor = connection.cursor()
            query1 = "select * from links where short_link=%s"
            value1 = shorturl
            cursor.execute(query1, value1)
            data = cursor.fetchone()
            if data is None:
                break
        query2 = "insert into links(long_link, short_link) values (%s,%s)"
        value = (longlink, shorturl)
        cursor.execute(query2, value)
        data = {"email": "Your url is shorten with classy.co/"+shorturl}
        return render(request, "first.html", data)

def HandlingUrl (request,**kwargs):
    url = kwargs['url']
    cursor = connection.cursor()
    query = "select long_link from links where short_link = %s "
    value = url
    cursor.execute(query, value)
    data = cursor.fetchone()
    if data is None:
        return render(request, "home.html")
    else:
        return redirect(data[0])























