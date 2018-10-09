# Generated by Django 2.1 on 2018-09-23 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180922_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='commands',
            field=models.ManyToManyField(related_name='commands_list', to='app.Commands'),
        ),
        migrations.AlterField(
            model_name='commands',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_id', to='app.Issue'),
        ),
    ]
