from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('total_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Total Contributions')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Party',
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(db_index=True, max_length=200)),
                ('zip_code', models.CharField(db_index=True, max_length=10)),
                ('total_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Total Contributions')),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.employer')),
            ],
            options={
                'unique_together': {('full_name', 'zip_code')},
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('CAND_ID', models.CharField(max_length=9, primary_key=True, serialize=False, verbose_name='Candidate ID')),
                ('CAND_NAME', models.CharField(db_index=True, max_length=200, verbose_name='Candidate Name')),
                ('CAND_ELECTION_YR', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Election Year')),
                ('CAND_OFFICE_ST', models.CharField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('CAND_OFFICE', models.CharField(choices=[('H', 'House'), ('S', 'Senate'), ('P', 'President')], max_length=1, verbose_name='Office')),
                ('CAND_OFFICE_DISTRICT', models.CharField(blank=True, max_length=2, null=True, verbose_name='District')),
                ('total_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Total Contributions')),
                ('CAND_PTY_AFFILIATION', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.party')),
            ],
            options={
                'db_table': 'api_candidate',
            },
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('CMTE_ID', models.CharField(max_length=9, primary_key=True, serialize=False, verbose_name='Committee ID')),
                ('CMTE_NM', models.CharField(db_index=True, max_length=200, verbose_name='Committee Name')),
                ('TRES_NM', models.CharField(blank=True, max_length=90, null=True, verbose_name='Treasurer Name')),
                ('CMTE_ST', models.CharField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('CMTE_TP', models.CharField(blank=True, max_length=1, null=True, verbose_name='Committee Type')),
                ('CMTE_DSGN', models.CharField(blank=True, max_length=1, null=True, verbose_name='Designation')),
                ('total_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='Total Contributions')),
                ('CAND_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='committees', to='api.candidate')),
            ],
            options={
                'db_table': 'api_committee',
            },
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(db_index=True, decimal_places=2, max_digits=14)),
                ('receipt_date', models.DateField(db_index=True)),
                ('fec_sub_id', models.BigIntegerField(help_text='Original FEC SUB_ID', null=True, unique=True)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='api.committee')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='api.contributor')),
            ],
            options={
                'ordering': ['-receipt_date'],
            },
        ),
        migrations.CreateModel(
            name='FECContribution',
            fields=[
                ('CMTE_ID', models.CharField(max_length=9, verbose_name='Filer identification number')),
                ('AMNDT_IND', models.CharField(blank=True, max_length=1, null=True, verbose_name='Amendment indicator')),
                ('RPT_TP', models.CharField(blank=True, max_length=3, null=True, verbose_name='Report type')),
                ('TRANSACTION_PGI', models.CharField(blank=True, max_length=5, null=True, verbose_name='Primary-general indicator')),
                ('IMAGE_NUM', models.CharField(blank=True, max_length=18, null=True, verbose_name='Image number')),
                ('TRANSACTION_TP', models.CharField(blank=True, max_length=4, null=True, verbose_name='Transaction type')),
                ('ENTITY_TP', models.CharField(blank=True, max_length=3, null=True, verbose_name='Entity type')),
                ('NAME', models.CharField(blank=True, max_length=200, null=True, verbose_name='Contributor name')),
                ('CITY', models.CharField(blank=True, max_length=30, null=True, verbose_name='City')),
                ('STATE', models.CharField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('ZIP_CODE', models.CharField(blank=True, max_length=9, null=True, verbose_name='ZIP code')),
                ('EMPLOYER', models.CharField(blank=True, max_length=38, null=True, verbose_name='Employer')),
                ('OCCUPATION', models.CharField(blank=True, max_length=38, null=True, verbose_name='Occupation')),
                ('TRANSACTION_DT', models.DateField(blank=True, null=True, verbose_name='Transaction date')),
                ('TRANSACTION_AMT', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True, verbose_name='Transaction amount')),
                ('OTHER_ID', models.CharField(blank=True, max_length=9, null=True, verbose_name='Other ID')),
                ('TRAN_ID', models.CharField(blank=True, max_length=32, null=True, verbose_name='Transaction ID')),
                ('FILE_NUM', models.BigIntegerField(blank=True, null=True, verbose_name='File number / Report ID')),
                ('MEMO_CD', models.CharField(blank=True, max_length=1, null=True, verbose_name='Memo code')),
                ('MEMO_TEXT', models.CharField(blank=True, max_length=100, null=True, verbose_name='Memo text')),
                ('SUB_ID', models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='FEC record number')),
            ],
            options={
                'verbose_name': 'FEC Contribution',
                'verbose_name_plural': 'FEC Contributions',
                'ordering': ['-TRANSACTION_DT'],
            },
        ),
    ]
