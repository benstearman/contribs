from django.db import migrations, models
import django.contrib.postgres.indexes
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_add_indices'),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name='candidate',
            index=django.contrib.postgres.indexes.GinIndex(fields=['CAND_NAME'], name='candidate_name_trgm_idx', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='committee',
            index=django.contrib.postgres.indexes.GinIndex(fields=['CMTE_NM'], name='committee_name_trgm_idx', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='contributor',
            index=django.contrib.postgres.indexes.GinIndex(fields=['full_name'], name='contributor_name_trgm_idx', opclasses=['gin_trgm_ops']),
        ),
    ]
