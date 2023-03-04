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
        cust_name = request.POST.get("cust_name").strip()
        username = request.POST.get("username").strip()
        passwd = request.POST.get("passwd").strip()

        with sqlite3.connect("./db.sqlite3") as db:
            cursor = db.cursor()
        cursor.execute(
        """SELECT cust_username
                From Customer
                WHERE cust_username= '{}' """.format(username)
        )
        res = cursor.fetchone()
        if res:
            db.close()
            messages.error(request, "The username existed. Reenter, please.")
            return redirect("/register")
        else:
            cursor.execute(
                """INSERT INTO customer (cust_username, cust_pw, pwd_salt, cust_name)
                    VALUES ('{}', '{}', '{}', '{}')""".format(username, passwd, salt, cust_name)
            )
            db.commit()
            db.close()
            # return redirect("/login")
            return redirect("/")
    else:
        return render(request, "register.html")
