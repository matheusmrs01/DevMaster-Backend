# Generated by Django 2.2.1 on 2019-05-19 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafio', '0004_auto_20190518_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desafio',
            name='status',
            field=models.CharField(choices=[('P', 'Proposta'), ('A', 'Aposta'), ('E', 'Em Andamento'), ('C', 'Concluído')], default='P', max_length=1, verbose_name='Status'),
        ),
    ]
