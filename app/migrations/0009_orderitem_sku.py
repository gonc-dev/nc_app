# Generated by Django 2.2 on 2020-06-27 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200620_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='sku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.SKU'),
        ),
    ]
