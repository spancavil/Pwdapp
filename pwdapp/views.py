import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from httplib2 import Response
from pwdapp.models import Users, Password
from django.contrib.auth.hashers import *
import jwt, datetime


def Inicio(request):
    token = request.COOKIES.get('accessToken')
    if not token:
        return render(request, 'pwdapp/login.html')
    try:
        payload = jwt.decode(token, 'ultraspannosecret', algorithms=['HS256'])
        print(payload)
        return redirect('/dashboard/')
    except Exception as e:
        print("Except on Inicio" + str(e))
        return render(request, 'pwdapp/login.html')


def register(request):
    if (request.method == 'GET'):
        return render(request, 'pwdapp/register.html')
    if (request.method == "POST"):
        # json.loads es el equivalente de JSON.parse
        data = json.loads(request.body)
        
        if (data['password'] and data['confirm'] and data['username']):
            if (data['password'] == data['confirm']):
                # json.dumps es el equivalente de JSON.stringify
                try: 
                    pwdHashed = make_password(data['password'])
                    print(pwdHashed)
                    user = Users(user=data['username'], login_password=pwdHashed)
                    user.save()
                    return HttpResponse(json.dumps({"msg": "User saved. You can login"}))
                except Exception as e:
                    print('Exception raised on register:' + str(e))
                    return HttpResponse(json.dumps({"error": "Database error"}))

            else:
                return HttpResponse(json.dumps({"error": "Passwords must match"}))
        else:
            return HttpResponse(json.dumps({"error": "Enter valid data"}))
    else:
        return HttpResponse(json.dumps({"error": "Request not handled"}))

def login(request):
    if (request.method == "POST"):
        # json.loads es el equivalente de JSON.parse
        data = json.loads(request.body)
        if (data['password'] and data['username']):
            # json.dumps es el equivalente de JSON.stringify
            try:
                username = Users.objects.filter(user=data['username']).first()
                if not username:
                    return HttpResponse(json.dumps({"error": "Not valid username/password"}))
                else:
                    hashed = username.login_password
                    checked = check_password(data['password'], hashed)
                    print(checked)
                    if checked:

                        payload = {
                            'id': username.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #Definimos un token que durará 60m,
                            'iat': datetime.datetime.utcnow(),
                            'username': username.user
                        }

                        token = jwt.encode(payload, "ultraspannosecret", algorithm="HS256")

                        # response = HttpResponse(json.dumps({'message': "Login successfully"}))
                        # response.set_cookie('accessToken', token, httponly=True)

                        response2 = redirect('/dashboard/')
                        response2.set_cookie('accessToken', token, httponly=True)
                        print(response2)
                        return response2
                        
            except Exception as e:
                print("Exception in login:" + str(e))
                return HttpResponse(json.dumps({"error": "Not valid username/password"}))
        else:
            return HttpResponse(json.dumps({"error": "Enter valid data"}))
    else:
        return render(request, 'pwdapp/login.html')

def protected_view(request):
    token = request.COOKIES.get('accessToken')
    print(token)
    if not token:
        print("No token")
        return render(request, 'pwdapp/not-login.html')
    try:
        payload = jwt.decode(token, 'ultraspannosecret', algorithms=['HS256'])
        print("El payload:")
        print(payload)
        username = payload["username"]
        print(f"Username: {username}")
        return render(request, 'pwdapp/dashboard.html', {"username": username})
    except Exception as e:
        print("Error at protected_view:" + str(e))
        return render(request, 'pwdapp/not-login.html')

def logout(request):
    print("Access logout")
    response = redirect('/login/')
    response.delete_cookie('accessToken')
    return response
        
