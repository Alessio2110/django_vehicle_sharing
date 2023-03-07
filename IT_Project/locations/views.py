import sqlite3
from django.contrib import messages
from django.views.generic.edit import CreateView
from .models import Location
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

class LocationView(CreateView):

    model = Location
    fields = ['address']
    template_name = 'locations/home.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['mapbox_access_token'] = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsZWszb2twMzBoa3QzcHBnNnhqbHIwMHUifQ.AW2-2b4IYh4qqPqqzMXy8Q'
        return context



def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname").strip()
        username = request.POST.get("username").strip()
        passwd = request.POST.get("passwd").strip()
        userRole = request.POST.get("userRole").strip()

        with sqlite3.connect("./db.sqlite3") as db:
            cursor = db.cursor()
            cursor.execute(
            """SELECT username
                    From userlist
                    WHERE username= '{}' """.format(username)
        )
        res = cursor.fetchone()
        if res:
            db.close()
            messages.error(request, "Sorry,the username existed.")
            return redirect("/register")
        elif username=='' or passwd=='' or fullname=='':
            db.close()
            messages.error(request, "Sorry,the username or passwd or fullname null.")
            return redirect("/register")
        else:
            cursor.execute(
                """INSERT INTO userlist (fullname, username, passwd, userrole)
                    VALUES ('{}', '{}', '{}', '{}')""".format(fullname,username, passwd, userRole)
            )
            db.commit()
            db.close()
            # return redirect("/login")
            return redirect("/")
    else:
        return render(request, "locations/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        passwd = request.POST.get("passwd").strip()
        userRole = request.POST.get("userRole").strip()

        with sqlite3.connect("./db.sqlite3") as db:
            cursor = db.cursor()
            cursor.execute(
                """SELECT fullname, username, passwd, userrole
                    From userlist
                    WHERE username= '{}' """.format(username)
        )
        res = cursor.fetchone()
        db.close()
        if res:
            if passwd == res[2] and userRole == res[3]:
                request.session["fullname"] = res[0]
                request.session["username"] = res[1]
                request.session["passwd"] = res[2]
                request.session["userrole"] = res[3]
                return redirect("/")
                # return redirect("/customer")

            else:
                 messages.error(request, "The password or userRole is wrong.")
                 # return render(request, "login.html")
                 return redirect("/login")
        else:
            messages.error(request, "The username does not exist.")
            #return render(request, "login.html")
            return redirect("/login")

    # elif request.method == "GET":
    #     return redirect("/register")

    else:
        return render(request, "locations/login.html")

