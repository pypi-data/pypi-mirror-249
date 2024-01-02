# Generated by Django 5.0 on 2023-12-27 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stela_control', '0020_biography_alter_billingrecipt_option_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biography',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='biography',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='biography',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='biography',
            name='place_of_birth',
        ),
        migrations.RemoveField(
            model_name='biography',
            name='profession',
        ),
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('Monthly charge', 'Monthly charge'), ('budget_design', 'Budget Design'), ('Billing receipt', 'Billing receipt'), ('budget_marketing', 'Budget Marketing'), ('budget_development', 'Budget Development'), ('Others', 'Others')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('E-commerce', 'E-commerce'), ('Education and Training', 'Education and Training'), ('IT Development Services', 'IT Development Services'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services'), ('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('Media Creators', 'Media Creators'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('Consulting', 'Consulting'), ('Restaurants and Food Services', 'Restaurants and Food Services'), ('Health and Wellness', 'Health and Wellness')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-light-blue', 'card-light-blue'), ('card-light-danger', 'card-light-danger'), ('card-tale', 'card-tale'), ('card-dark-blue', 'card-dark-blue')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.CharField(blank=True, choices=[('News', 'News'), ('Inspiration', 'Inspiration'), ('Tutorials', 'Tutorials'), ('Guides and Manuals', 'Guides and Manuals'), ('Events and Conferences', 'Events and Conferences'), ('Interviews', 'Interviews'), ('Tips and Tricks', 'Tips and Tricks')], default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 27, 12, 39, 44, 635908)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Stela Payment Free Suscription', 'Stela Payment Free Suscription'), ('No Selected', 'No Selected'), ('Initial Payment', 'Initial Payment'), ('Promotional Discount', 'Promotional Discount')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send')], max_length=20),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 3', 'Style Template 3'), ('Style Template 1', 'Style Template 1'), ('Style Template 2', 'Style Template 2'), ('Style Template 4', 'Style Template 4')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Cloud Elastic Instance', 'Cloud Elastic Instance'), ('Stela Marketing', 'Stela Marketing'), ('Store', 'Store'), ('Cloud Domains', 'Cloud Domains'), ('No Selected', 'No Selected'), ('Stela Design', 'Stela Design'), ('Stela Websites', 'Stela Websites')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='pathcontrol',
            name='step',
            field=models.CharField(choices=[('Step 4', 'Step 4'), ('Step 3', 'Step 3'), ('Step 2', 'Step 2')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sendmoney',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('budget_design_terms', 'Budget Design Terms'), ('billing_terms', 'Monthly Billing Terms'), ('monthly_terms', 'Billing Terms'), ('Return Policy', 'Return Policy'), ('budget_development_terms', 'Budget Development Terms'), ('Terms and Conditions', 'Terms and Conditions'), ('budget_marketing_terms', 'Budget Marketing Terms'), ('Cookie Policy', 'Cookie Policy'), ('Privacy Policy', 'Privacy Policy'), ('Disclaimer', 'Disclaimer')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('Github', 'Github'), ('Linkedin', 'Linkedin'), ('Tiktok', 'Tiktok'), ('Facebook', 'Facebook'), ('X', 'X'), ('Youtube', 'Youtube'), ('Wikipedia', 'Wikipedia'), ('Instagram', 'Instagram')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='support',
            name='option',
            field=models.CharField(choices=[('My delivery has been delayed', 'My delivery has been delayed'), ('My account has an error', 'My account has an error'), ('Payments Issue', 'Payments Issue'), ('I have a problem with my project', 'I have a problem with my project'), ('I have a problem with my subscription', 'I have a problem with my subscription'), ('Others', 'Others')], max_length=60, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='support',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50, null=True),
        ),
    ]
