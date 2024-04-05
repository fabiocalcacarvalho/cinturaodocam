# Generated by Django 4.2.7 on 2024-04-04 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_partida_vencedor_alter_partida_desafiante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='vencedor',
        ),
        migrations.AlterField(
            model_name='partida',
            name='desafiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidas_desafiante', to='principal.jogador'),
        ),
        migrations.AlterField(
            model_name='partida',
            name='detentor_atual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidas_detentor', to='principal.jogador'),
        ),
    ]
