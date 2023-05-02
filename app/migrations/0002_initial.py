# Generated by Django 4.2 on 2023-04-23 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.currency'),
        ),
        migrations.AddField(
            model_name='poll',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='balance',
            name='currency_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.currency'),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='balance', to=settings.AUTH_USER_MODEL),
        ),
    ]