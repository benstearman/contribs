from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='candidate',
            index=models.Index(fields=['CAND_NAME', 'CAND_ELECTION_YR'], name='api_candida_CAND_NA_f2bdfb_idx'),
        ),
        migrations.AddIndex(
            model_name='contribution',
            index=models.Index(fields=['contributor', 'committee'], name='api_contrib_contrib_4206e7_idx'),
        ),
        migrations.AddIndex(
            model_name='contribution',
            index=models.Index(fields=['receipt_date', 'amount'], name='api_contrib_receipt_c1c4f5_idx'),
        ),
        migrations.AddIndex(
            model_name='feccontribution',
            index=models.Index(fields=['CMTE_ID'], name='api_feccont_CMTE_ID_aa1cda_idx'),
        ),
        migrations.AddIndex(
            model_name='feccontribution',
            index=models.Index(fields=['NAME'], name='api_feccont_NAME_99113d_idx'),
        ),
        migrations.AddIndex(
            model_name='feccontribution',
            index=models.Index(fields=['TRANSACTION_DT'], name='api_feccont_TRANSAC_5edcbe_idx'),
        ),
        migrations.AddIndex(
            model_name='feccontribution',
            index=models.Index(fields=['TRANSACTION_AMT'], name='api_feccont_TRANSAC_c702e2_idx'),
        ),
    ]
