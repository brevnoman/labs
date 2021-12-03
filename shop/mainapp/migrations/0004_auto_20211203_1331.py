# Generated by Django 3.2.9 on 2021-12-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211202_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total Price'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]