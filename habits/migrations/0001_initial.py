# Generated by Django 4.2.4 on 2023-08-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.TimeField(auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('category', models.CharField(max_length=150)),
                ('units', models.CharField(choices=[('time', 'Time (minutes)'), ('repetition', 'Repetition'), ('distance', 'Distance (km)'), ('check', 'Check')], max_length=50)),
                ('goal', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HabitEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('quantity', models.PositiveIntegerField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
        migrations.AddField(
            model_name='habit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.user'),
        ),
    ]
