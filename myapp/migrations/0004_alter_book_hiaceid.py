# Generated by Django 4.1.5 on 2023-01-24 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_book_hiaceid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='hiaceid',
            field=models.DecimalField(decimal_places=0, max_digits=2),
        ),
    ]
