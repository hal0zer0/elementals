# Generated by Django 3.1.1 on 2020-09-21 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Battery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BatteryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('cost', models.ManyToManyField(to='elemcore.Battery')),
            ],
        ),
        migrations.AddField(
            model_name='battery',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elemcore.batterytype'),
        ),
        migrations.CreateModel(
            name='Construct',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elemcore.card')),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
                ('traits', models.ManyToManyField(to='elemcore.Trait')),
            ],
            bases=('elemcore.card',),
        ),
    ]
