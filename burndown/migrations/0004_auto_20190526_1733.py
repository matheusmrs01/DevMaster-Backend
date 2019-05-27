# Generated by Django 2.2.1 on 2019-05-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burndown', '0003_auto_20190526_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='burndown',
            name='quantidade_queimada_dia0',
        ),
        migrations.AddField(
            model_name='burndown',
            name='quantidade_missao_falta',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Quantidade de missões da semana passada, não queimadas'),
        ),
        migrations.AlterField(
            model_name='burndown',
            name='quantidade_missao',
            field=models.IntegerField(blank=True, default=0, verbose_name='Quantidade de missões da semana'),
        ),
    ]