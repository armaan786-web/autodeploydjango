# Generated by Django 4.2.5 on 2023-12-21 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_remove_package_visa_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisaSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate_amt', models.FloatField()),
                ('cgst', models.FloatField()),
                ('sgst', models.FloatField()),
                ('totalAmount', models.FloatField()),
                ('lastupdated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated_on', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_category', to='crm_app.visacategory')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.visacountry')),
                ('subcategory_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_subcategory', to='crm_app.visacategory')),
            ],
            options={
                'db_table': 'Pricing',
            },
        ),
    ]
