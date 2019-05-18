# Generated by Django 2.2.1 on 2019-05-18 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('desafio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desafio',
            name='item_desafiado',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemDesafiado', to='jogador.JogadorItem'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='item_desafiante',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemDesafiante', to='jogador.JogadorItem'),
        ),
    ]