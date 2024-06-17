# pages/migrations/0019_auto_20240521_1545.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_auto_20240521_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aadhar',
            name='DOB',
            field=models.DateField(default='2024-01-01'),
        ),
    ]

