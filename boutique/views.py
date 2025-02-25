from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Categorie, Produit, Vente, ArticleVendu
from .forms import ProduitForm, CategorieForm, VenteForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .forms import SignupForm
from .models import Commande
from .models import Panier 
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserProfile 
from .models import Panier, PanierProduit

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            user_profile = request.user.profile  
            user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()
            return JsonResponse({'success': True})
    
    return render(request, 'registration/hisprofile.html')  


# Ajouter un nouveau produit
@login_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        print("Formulaire soumis !")
        if form.is_valid():
            form.save()
            #print("Formulaire validé, produit ajouté !")
            messages.success(request, 'Le produit a été ajouté avec succès.')
            return redirect('gestion_produits')
        
    else:
        form = ProduitForm()
    return render(request, 'boutique/ajouter_produit.html', {'form': form})


def profile(request):
    
    return render(request, 'registration/accueil.html')  # Renvoyer le template de l'accueil

def accueil(request):
    return render(request, 'registration/accueil.html')  # Renvoyer le template de l'accueil

def hisprofile(request):
    return render(request, 'registration/hisprofile.html')  


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Chiffrer le mot de passe
            user.save()
            return redirect('login')  # Rediriger vers la page de connexion
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def check_user_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Vérifier si le mot de passe correspond à l'utilisateur connecté
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            # Si le mot de passe est correct
            return JsonResponse({'status': 'success', 'message': 'Mot de passe correct.'})
        else:
            # Si le mot de passe est incorrect
            return JsonResponse({'status': 'error', 'message': 'Mot de passe incorrect.'})
    
    return render(request, 'check_password.html')


# Liste des produits du vendeur connecté
@login_required
def liste_produits(request):
    produits = Produit.objects.all()  # Récupérer tous les produits
    return render(request, 'store/liste_produits.html', {'produits': produits})
    produits = Produit.objects.filter(vendeur=request.user)  # Filtrer par vendeur
    return render(request, 'store/liste_produits.html', {'produits': produits})




# Modifier un produit existant
@login_required
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect("liste_produits")
    else:
        form = ProduitForm(instance=produit)

    return render(request, "boutique/modifier_produit.html", {"form": form, "produit": produit})


# Supprimer un produit
@login_required
def supprimer_produit(request, id):  
    produit = get_object_or_404(Produit, id=id)
    produit.delete()
    return redirect ('gestion_produits' )  

# Enregistrer une vente
@login_required
def enregistrer_vente(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()
            return redirect('liste_ventes')
    else:
        form = VenteForm()
    return render(request, 'store/enregistrer_vente.html', {'form': form})

# Liste des ventes
@login_required
def liste_ventes(request):
    ventes = Vente.objects.all()  # Liste toutes les ventes
    return render(request, 'store/liste_ventes.html', {'ventes': ventes})

# Tableau de bord du vendeur (produits du vendeur connecté)
@login_required
def dashboard(request):
    produits = Produit.objects.all()  # Récupérer tous les produits
    return render(request, 'boutique/dashboard.html', {'produits': produits})

    commandes = Commande.objects.all()  # Récupère toutes les commandes
    
    
# Pages des clients
@login_required
def client(request):
    produits = Produit.objects.all()  # Récupérer tous les produits
    return render(request, 'boutique/client.html', {'produits': produits})



    # Construire les URLs pour chaque commande
    commandes_with_urls = [
        (commande, reverse('client_order', kwargs={'commande_id': commande.id}))
        for commande in commandes
    ]
    
    # Passer les commandes avec leurs URLs au template
    return render(request, 'boutique/dashboard.html', {'commandes_with_urls': commandes_with_urls})


# Page de gestion des produits du vendeur connecté
@login_required
def gestion_produits(request):
    produits = Produit.objects.all()  # Récupérer tous les produits
    return render(request, 'boutique/gestion_produits.html', {'produits': produits})

# Vérifier le mot de passe d'un utilisateur
def check_user_password(request):
    # Récupérer le nom d'utilisateur et le mot de passe depuis le formulaire
    username = request.POST.get('username')  
    password = request.POST.get('password')

    user = User.objects.filter(username=username).first()
    
    if user:
        # Vérifier si le mot de passe correspond
        if check_password(password, user.password):
            return HttpResponse("Mot de passe correct")
        else:
            return HttpResponse("Mot de passe incorrect")
    else:
        return HttpResponse("Utilisateur non trouvé")
    



def client_order_view(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
   
    return render(request, 'client_order.html', {'commande': commande})

    # Extraire les infos du client depuis la commande
    client_info = {
        'nom': commande.nom_client if hasattr(commande, 'nom_client') else 'Inconnu',
        'email': commande.email_client if hasattr(commande, 'email_client') else 'Non fourni',
        'telephone': commande.telephone_client if hasattr(commande, 'telephone_client') else 'Non fourni'
    }

    return render(request, 'boutique/client_order.html', {'commande': commande, 'client': client_info})

#Voir les détails d'un produit sur le l'interface d'un vendeur
def produit_detail(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)  
    return render(request, 'boutique/produit_detail.html', {'produit': produit})



#Voir les détails d'un produit sur le l'interface d'un client
def produit_detail_clients(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'boutique/voir_detail.html', {'produit': produit})





def ajouter_panier(request, id):
    produit = Produit.objects.get(id=id)
    panier, created = Panier.objects.get_or_create(user=request.user)
    panier.produits.add(produit)  # Assuming the Panier model has a ManyToMany relation with Produit
    return redirect('panier')  # Redirect to the panier page



def client_order_view(request, commande_id):
    # Code pour traiter la commande
    return render(request, 'boutique/client_order.html', {'commande_id': commande_id})

from .models import UserProfile  

@login_required
def profile_view(request):
    user_profile = request.user.profile
    
    if request.method == 'POST':
        # Mettre à jour la photo de profil si fournie
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        # Mettre à jour les autres informations
        user_profile.full_name = request.POST.get('full_name')
        user_profile.phone = request.POST.get('phone')
        user_profile.address = request.POST.get('address')

        # Mettre à jour le mot de passe si fourni
        password = request.POST.get('password')
        if password:
            user_profile.user.set_password(password)

        user_profile.save()
        return JsonResponse({'success': True})

    return render(request, 'hisprofile.html') 



def afficher_panier(request):
    panier, created = Panier.objects.get_or_create(user=request.user)
    items = panier.panierproduit_set.all()  # Récupérer tous les produits dans le panier
    total = sum(item.produit.prix * item.quantite for item in items)  # Calculer le total ici
    return render(request, 'boutique/panier.html', {'panier': panier, 'items': items, 'total': total})

def ajouter_au_panier(request, produit_id):
    """Ajoute un produit au panier."""
    produit = get_object_or_404(Produit, id=produit_id)
    panier, created = Panier.objects.get_or_create(user=request.user)
    
    # Vérifie si le produit est déjà dans le panier
    panier_produit, created = PanierProduit.objects.get_or_create(panier=panier, produit=produit)

    if not created:
        # Si le produit existe déjà, on augmente la quantité
        panier_produit.quantite += 1
    else:
        # Si c'est un nouvel ajout, on définit la quantité à 1
        panier_produit.quantite = 1
    
    panier_produit.save()  # Sauvegarde les modifications
    return redirect('panier')  # Redirige vers la page du panier



def retirer_du_panier(request, produit_id):
    """Retire un produit du panier."""
    panier = get_object_or_404(Panier, user=request.user)
    panier_produit = get_object_or_404(PanierProduit, panier=panier, produit_id=produit_id)
    
    # Supprime le produit du panier
    panier_produit.delete()
    return redirect('panier')  # Redirige vers la page du panier


def recherche_produits(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    
    query = request.GET.get('q')
    category_filter = request.GET.get('categorie')

    if query:
        produits = produits.filter(nom__icontains=query)
    if category_filter:
        produits = produits.filter(categorie__nom=category_filter)

    panier_count = 0
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.get(user=request.user)
            panier_count = panier.panierproduit_set.count()
        except Panier.DoesNotExist:
            panier_count = 0

    return render(request, 'boutique/client.html', {
        'produits': produits,
        'categories': categories,
        'panier_count': panier_count,
    })