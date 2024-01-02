# Generated by Django 5.0 on 2023-12-29 01:46

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stela_control', '0024_rename_modules_elements_remove_bookpost_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stela_control.variant'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whishlist', to='stela_control.variant'),
        ),
        migrations.AlterField(
            model_name='variantsimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog', to='stela_control.variant'),
        ),
        migrations.AlterField(
            model_name='itemproducts',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stela_control.variant'),
        ),
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('budget_design', 'Budget Design'), ('budget_development', 'Budget Development'), ('Others', 'Others'), ('Billing receipt', 'Billing receipt'), ('budget_marketing', 'Budget Marketing'), ('Monthly charge', 'Monthly charge')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('Consulting', 'Consulting'), ('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Restaurants and Food Services', 'Restaurants and Food Services'), ('Education and Training', 'Education and Training'), ('Media Creators', 'Media Creators'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services'), ('Health and Wellness', 'Health and Wellness'), ('IT Development Services', 'IT Development Services'), ('E-commerce', 'E-commerce')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-light-danger', 'card-light-danger'), ('card-tale', 'card-tale'), ('card-light-blue', 'card-light-blue'), ('card-dark-blue', 'card-dark-blue')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.CharField(blank=True, choices=[('Events and Conferences', 'Events and Conferences'), ('Tips and Tricks', 'Tips and Tricks'), ('Interviews', 'Interviews'), ('Tutorials', 'Tutorials'), ('Guides and Manuals', 'Guides and Manuals'), ('News', 'News'), ('Inspiration', 'Inspiration')], default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 28, 22, 45, 57, 540739)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Stela Payment Free Suscription', 'Stela Payment Free Suscription'), ('Promotional Discount', 'Promotional Discount'), ('Initial Payment', 'Initial Payment'), ('No Selected', 'No Selected')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send')], max_length=20),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 3', 'Style Template 3'), ('Style Template 4', 'Style Template 4'), ('Style Template 1', 'Style Template 1'), ('Style Template 2', 'Style Template 2')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Stela Marketing', 'Stela Marketing'), ('Stela Design', 'Stela Design'), ('No Selected', 'No Selected'), ('Stela Websites', 'Stela Websites'), ('Cloud Elastic Instance', 'Cloud Elastic Instance'), ('Cloud Domains', 'Cloud Domains'), ('Store', 'Store')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('budget_marketing_terms', 'Budget Marketing Terms'), ('billing_terms', 'Monthly Billing Terms'), ('budget_design_terms', 'Budget Design Terms'), ('Privacy Policy', 'Privacy Policy'), ('Disclaimer', 'Disclaimer'), ('Return Policy', 'Return Policy'), ('Terms and Conditions', 'Terms and Conditions'), ('Cookie Policy', 'Cookie Policy'), ('monthly_terms', 'Billing Terms'), ('budget_development_terms', 'Budget Development Terms')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Github', 'Github'), ('Linkedin', 'Linkedin'), ('Wikipedia', 'Wikipedia'), ('Youtube', 'Youtube'), ('X', 'X'), ('Tiktok', 'Tiktok')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='support',
            name='option',
            field=models.CharField(choices=[('Payments Issue', 'Payments Issue'), ('Others', 'Others'), ('I have a problem with my subscription', 'I have a problem with my subscription'), ('I have a problem with my project', 'I have a problem with my project'), ('My account has an error', 'My account has an error'), ('My delivery has been delayed', 'My delivery has been delayed')], max_length=60, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[('Paypal', 'Paypal'), ('Zelle', 'Zelle'), ('Binance', 'Binance')], max_length=100, verbose_name='Type of Wallet'),
        ),
        migrations.DeleteModel(
            name='Variants',
        ),
    ]
