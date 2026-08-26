from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_blogpost_alter_donation_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='two_week_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='program',
            name='four_week_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='program',
            name='eight_week_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='program',
            name='extra_week_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
