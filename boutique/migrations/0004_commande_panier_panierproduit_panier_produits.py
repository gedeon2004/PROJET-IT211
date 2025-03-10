# Generated by Django 5.1.3 on 2025-02-15 07:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0003_produit_image_produit_vendeur_alter_produit_prix_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50, unique=True)),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PanierProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('panier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boutique.panier')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boutique.produit')),
            ],
        ),
        migrations.AddField(
            model_name='panier',
            name='produits',
            field=models.ManyToManyField(through='boutique.PanierProduit', to='boutique.produit'),
        ),
    ]
