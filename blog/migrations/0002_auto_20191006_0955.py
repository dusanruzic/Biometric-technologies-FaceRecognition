# Generated by Django 2.2.1 on 2019-10-06 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='danKraj',
        ),
        migrations.RemoveField(
            model_name='period',
            name='danPocetak',
        ),
        migrations.RemoveField(
            model_name='period',
            name='godinaKraj',
        ),
        migrations.RemoveField(
            model_name='period',
            name='godinaPocetak',
        ),
        migrations.RemoveField(
            model_name='period',
            name='mesecKraj',
        ),
        migrations.RemoveField(
            model_name='period',
            name='mesecPocetak',
        ),
        migrations.AddField(
            model_name='period',
            name='kraj',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='period',
            name='pocetak',
            field=models.DateField(auto_now=True),
        ),
    ]