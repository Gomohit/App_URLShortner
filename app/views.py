from django.shortcuts import render


# Create your views here.
def xyz(request):
    return render(request, "index.html")


def signup(request):
    email = request.GET['emailname']
    psw = request.GET['pswname']
    data = {'email': email, 'password': psw}
    return render(request, "first.html", data)


