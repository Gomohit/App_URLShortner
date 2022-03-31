from django.shortcuts import render
from django.db import connection
# Create your views here.
def xyz(request):
    return render(request, "index.html")


def signup(request):
    email = request.GET['emailname']
    psw = request.GET['pswname']
    cursor = connection.cursor()
    query = "insert into users (email ,password) values (%s,%s)"
    value = (email, psw)
    cursor.execute(query, value)
    print(cursor.rowcount)

    # query = "Select * from city where name='"+email+"'"
    # cursor.execute(query)
    # row = cursor.fetchone()
    # print(row)
    data = {'email': email, 'password': psw}
    return render(request, "first.html", data)


