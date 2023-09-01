# Generated by Django 4.2.4 on 2023-08-31 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_remove_habit_user_alter_habit_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='habits.user'),
            preserve_default=False,
        ),
    ]