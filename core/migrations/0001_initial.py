# Generated by Django 5.2 on 2025-05-05 17:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Giới thiệu bản thân')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Ngày sinh')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')], max_length=1, verbose_name='Giới tính')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Địa điểm')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Ảnh đại diện')),
                ('preferred_gender', models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')], max_length=1, verbose_name='Giới tính mong muốn')),
                ('min_age', models.IntegerField(blank=True, null=True, verbose_name='Độ tuổi tối thiểu')),
                ('max_age', models.IntegerField(blank=True, null=True, verbose_name='Độ tuổi tối đa')),
                ('preferred_location', models.CharField(blank=True, max_length=100, verbose_name='Địa điểm mong muốn')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
