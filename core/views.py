from django.http import HttpResponse

def home(request):
    return HttpResponse("✅ Hello from Dockerized Django 🚀 CI/CD Pipeline working!")
