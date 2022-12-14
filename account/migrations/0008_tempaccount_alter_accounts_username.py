# Generated by Django 4.1.1 on 2022-11-23 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='tempAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('phone_number', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='accounts',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]
