# Generated by Django 3.0.7 on 2020-06-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_func', '0008_auto_20200629_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='views',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='grouppost',
            name='views',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
