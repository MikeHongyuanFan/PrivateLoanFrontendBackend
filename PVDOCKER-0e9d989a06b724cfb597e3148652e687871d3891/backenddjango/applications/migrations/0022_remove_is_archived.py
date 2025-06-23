from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0021_alter_application_quantity_surveyor_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE applications_application DROP COLUMN is_archived;",
            reverse_sql="ALTER TABLE applications_application ADD COLUMN is_archived boolean DEFAULT FALSE NOT NULL;"
        ),
    ] 