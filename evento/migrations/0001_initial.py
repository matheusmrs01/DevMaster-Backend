# Generated by Django 2.2.1 on 2019-05-17 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True)),
                ('url_image', models.TextField(default='https://www.mariowiki.com/images/thumb/a/a6/Super_Mushroom_Artwork_-_Super_Mario_3D_World.png/1200px-Super_Mushroom_Artwork_-_Super_Mario_3D_World.png')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('multiplicador_xp', models.FloatField(blank=True, default=1)),
                ('data_inicio', models.DateTimeField()),
                ('data_final', models.DateTimeField(blank=True)),
                ('primeiro', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item1', to='evento.Item')),
                ('quarto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item4', to='evento.Item')),
                ('quinto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item5', to='evento.Item')),
                ('segundo', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item2', to='evento.Item')),
                ('sexto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item6', to='evento.Item')),
                ('terceiro', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='Item3', to='evento.Item')),
            ],
        ),
    ]
