# Generated by Django 3.2.7 on 2021-09-22 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0005_game_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='engine.game'),
        ),
    ]