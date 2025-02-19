# Generated by Django 5.1.3 on 2025-02-12 18:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0002_auto_20250209_1809'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='image',
            field=models.ImageField(blank=True, default='produits/default.jpg', null=True, upload_to='produits/'),
        ),
        migrations.AddField(
            model_name='produit',
            name='vendeur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='produits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prix',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='quantite_en_stock',
            field=models.IntegerField(default=0),
        ),
    ]
