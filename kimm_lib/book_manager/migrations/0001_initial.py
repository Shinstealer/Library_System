# Generated by Django 2.2.1 on 2019-06-20 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=50, null=True)),
                ('publisher', models.CharField(max_length=50, null=True)),
                ('publish_date', models.DateField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book_manager.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_date', models.DateField(null=True)),
                ('disposal_date', models.DateField(null=True)),
                ('remarks', models.CharField(max_length=100)),
                ('bookinfo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book_manager.BookInfo')),
            ],
        ),
    ]
