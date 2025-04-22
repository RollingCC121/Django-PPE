from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.utils.html import escape


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    bandas_pop = [
        "ABBA", "Adele", "Ariana Grande", "Backstreet Boys", "Bananarama",
        "Beyoncé", "Billie Eilish", "Blackpink", "Britney Spears", "Bruno Mars",
        "Camila Cabello", "Carly Rae Jepsen", "Coldplay", "Dua Lipa", "Ed Sheeran",
        "Ellie Goulding", "Enrique Iglesias", "Fifth Harmony", "Florence + The Machine", "George Michael",
        "Gwen Stefani", "Harry Styles", "Halsey", "Imagine Dragons", "INXS",
        "James Blunt", "Janet Jackson", "Jason Mraz", "Jennifer Lopez", "Jessie J",
        "Jonas Brothers", "Justin Bieber", "Katy Perry", "Kelly Clarkson", "Kylie Minogue",
        "Lady Gaga", "Lana Del Rey", "Little Mix", "Lorde", "Luis Fonsi",
        "Madonna", "Mariah Carey", "Maroon 5", "Miley Cyrus", "Niall Horan",
        "NSYNC", "Olivia Rodrigo", "One Direction", "OneRepublic", "P!nk",
        "Paramore", "Pharrell Williams", "Post Malone", "Rihanna", "Robbie Williams",
        "Rosalía", "Sabrina Carpenter", "Sam Smith", "Selena Gomez", "Shakira",
        "Shawn Mendes", "Sia", "Spice Girls", "Sugababes", "Take That",
        "Taylor Swift", "The Chainsmokers", "The Weeknd", "Tove Lo", "Troye Sivan",
        "Twice", "U2", "Usher", "Vance Joy", "Vanessa Carlton",
        "Walk The Moon", "Whitney Houston", "Zara Larsson", "Zayn Malik", "BTS",
        "EXO", "Red Velvet", "TXT", "Super Junior", "Monsta X",
        "CNCO", "Morat", "Reik", "Ha*Ash", "Jesse & Joy",
        "Axel", "Lali", "Tini", "Karol G", "RBD",
        "Camilo", "Danny Ocean", "Sebastián Yatra", "Danna Paola", "Aitana"
    ]

    query = request.GET.get('q', '')
    bandas_filtradas = bandas_pop

    if query:
        try:
            regex = re.compile(query, re.IGNORECASE)
            bandas_filtradas = [banda for banda in bandas_pop if regex.search(banda)]
        except re.error:
            messages.error(request, f'Expresión regular inválida: "{escape(query)}"')

    return render(request, 'home.html', {
        'bandas_pop': bandas_filtradas,
        'query': query
    })
    
    return render(request, 'home.html', {'bandas_pop': bandas_pop})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuario creado exitosamente. Inicia sesión.')
            return redirect('login')

    return render(request, 'register.html')
