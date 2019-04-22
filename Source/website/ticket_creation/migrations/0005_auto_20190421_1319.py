# Generated by Django 2.1.7 on 2019-04-21 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_creation', '0004_auto_20190420_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('creater', models.CharField(max_length=256)),
                ('creater_role', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='all_tickets',
            name='read_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]