# Generated by Django 2.2.1 on 2019-05-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafio', '0007_desafiomissoes_xp_ganha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desafio',
            name='vencedor',
            field=models.CharField(blank=True, choices=[('DE', 'Desafiante'), ('DO', 'Desafiado')], max_length=2, null=True, verbose_name='Status'),
        ),
    ]