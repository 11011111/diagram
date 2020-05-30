from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class Main(View):
    def get(request):
        return render(request, 'pages/main.html', locals())


class Profile(View):
    def get(self, request):
        return render(request, 'path/template.html', locals())

    def post(self, request):
        return render(request, 'path/template.html', locals())


class Calculator(View):
    def get(self, request):
        return render(request, 'path/template.html', locals())

    def post(self, request):
        return render(request, 'path/template.html', locals())


class Search(View):
    def get(self, request):
        return render(request, 'path/template.html', locals())
