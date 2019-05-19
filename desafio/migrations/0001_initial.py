# Generated by Django 2.2.1 on 2019-05-18 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('missao', '0001_initial'),
        ('jogador', '0001_initial'),
        ('evento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desafio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome Desafio')),
                ('status', models.CharField(choices=[('P', 'Proposta'), ('A', 'Aposta'), ('C', 'Conslusão')], default='P', max_length=1, verbose_name='Status')),
                ('desafiado', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Desafiado', to='jogador.Jogador')),
                ('desafiante', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Desafiante', to='jogador.Jogador')),
                ('item_desafiado', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemDesafiado', to='evento.Item')),
                ('item_desafiante', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemDesafiante', to='evento.Item')),
            ],
        ),
        migrations.CreateModel(
            name='DesafioMissoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desafio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Desafio', to='desafio.Desafio')),
                ('missao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Missão', to='missao.Missao')),
            ],
        ),
    ]
