# Generated by Django 2.1.8 on 2019-04-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_creation', '0005_auto_20190421_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='creater_role',
        ),
        migrations.AddField(
            model_name='notification',
            name='creater_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='ticket_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='creater',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
