# Generated by Django 4.2.4 on 2023-09-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0007_habit_demo_user_can_interact_alter_demouser_is_demo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]