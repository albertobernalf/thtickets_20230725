# Generated by Django 3.2 on 2023-03-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0023_remove_tickets_sede'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='desdeFinal',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='hastaFinal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
