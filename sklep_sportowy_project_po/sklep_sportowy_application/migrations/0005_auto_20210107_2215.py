# Generated by Django 3.1.5 on 2021-01-07 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklep_sportowy_application', '0004_auto_20210107_2212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zamowieniaprodukty',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='zamowieniaprodukty',
            unique_together=set(),
        ),
    ]
