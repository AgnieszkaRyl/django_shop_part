# Generated by Django 3.1.5 on 2021-01-07 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sklep_sportowy_application', '0002_auto_20210107_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adresy',
            options={},
        ),
        migrations.AlterModelOptions(
            name='kartyklienta',
            options={},
        ),
        migrations.AlterModelOptions(
            name='konta',
            options={},
        ),
        migrations.AlterModelOptions(
            name='kontapracownicze',
            options={},
        ),
        migrations.AlterModelOptions(
            name='produkty',
            options={},
        ),
        migrations.AlterModelOptions(
            name='zamowienia',
            options={},
        ),
        migrations.AlterModelOptions(
            name='znizki',
            options={},
        ),
        migrations.RemoveField(
            model_name='produkty',
            name='img_path',
        ),
        migrations.AddField(
            model_name='produkty',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
