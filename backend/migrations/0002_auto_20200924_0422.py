# Generated by Django 2.2 on 2020-09-24 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comboproduct',
            name='branch',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.DO_NOTHING, to='backend.Branch'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='pricing',
            unique_together={('product', 'branch', 'unit', 'version')},
        ),
    ]
