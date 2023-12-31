# Generated by Django 4.2.6 on 2023-10-19 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('estate', 'Real Estate'), ('pro', 'Trading Pro')], max_length=12, null=True)),
                ('type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'withdraw')], default='deposit', max_length=9)),
                ('amount', models.IntegerField()),
                ('address', models.CharField(max_length=150, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('status', models.IntegerField(max_length=1)),
                ('progress', models.CharField(choices=[('pending', 'pending'), ('active', 'active'), ('completed', 'completed')], default='pending', max_length=12)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile')),
            ],
        ),
    ]
