# pages/migrations/0018_auto_20240521_1537.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20240521_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='aadhar',
            name='Address',
            field=models.TextField(default=''),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aadhar',
            name='DOB',
            field=models.DateField(default='2000-01-01'),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aadhar',
            name='Fathers_Name',
            field=models.CharField(default='', max_length=100),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aadhar',
            name='Mothers_Name',
            field=models.CharField(default='', max_length=100),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aadhar',
            name='Name',
            field=models.CharField(default='', max_length=100),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marksheets',
            name='Board',
            field=models.CharField(default='', max_length=50),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marksheets',
            name='Name',
            field=models.CharField(default='', max_length=100),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marksheets',
            name='School',
            field=models.TextField(default=''),  # Correct default value
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marksheets',
            name='Year',
            field=models.IntegerField(default=2024),  # Correct default value
            preserve_default=False,
        ),
    ]

