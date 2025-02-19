from django.db import models
from django.contrib.auth.models import User  # Importation du modèle User
from django.utils import timezone


# Create your models here.

# Modèle pour les catégories de produits
class Categorie(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

# Modèle pour les produits
class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantite_en_stock = models.IntegerField(default=0)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produits")
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="produits", default=1)  
    image = models.ImageField(upload_to="produits/", blank=True, null=True, default='produits/default.jpg')

    def __str__(self):
        return self.nom
    
# Modèle pour les ventes
class Vente(models.Model):
    date = models.DateTimeField(auto_now_add=True)  # ou simplement models.DateTimeField() si modifiable
    total = models.DecimalField(max_digits=10, decimal_places=2)

# Modèle pour les articles vendus dans une vente
class ArticleVendu(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="articles")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField()
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} (Vente {self.vente.id})"
    


class Commande(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Commande {self.reference}"
    

class Panier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relier un panier à un utilisateur
    produits = models.ManyToManyField(Produit, through='PanierProduit')  # Relier plusieurs produits au panier

    def __str__(self):
        return f"Panier de {self.user.username}"

class PanierProduit(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)  # Quantité de chaque produit dans le panier

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom} dans le panier de {self.panier.user.username}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    
    
class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name