# Generated by Django 3.2.2 on 2021-05-12 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BasketsApp', '0003_alter_basket_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='products',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasketsApp.product'),
        ),
    ]