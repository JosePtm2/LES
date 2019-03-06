from django.db import models

# Create your models here.


class Tags(models.Model):
    name = models.IntegerField(db_column='Name',
                               blank=True,
                               null=True)
    id = models.AutoField(db_column='ID',
                          primary_key=True)

    class Meta:
        managed = True
        db_table = 'Tags'


class Pattern(models.Model):
    id = models.AutoField(db_column='ID',
                          primary_key=True)
    userid = models.ForeignKey('Users.User',
                               models.DO_NOTHING,
                               db_column='UserID')
    patternname = models.CharField(db_column='PatternName',
                                   max_length=255)
    image = models.TextField(db_column='Image',
                             blank=True,
                             null=True)
    description = models.CharField(db_column='Description',
                                   max_length=255)
    data_creation = models.DateField(db_column='Data Creation')

    class Meta:
        managed = True
        db_table = 'Pattern'


class Group(models.Model):
    id = models.AutoField(db_column='ID',
                          primary_key=True)
    userid = models.ForeignKey('Users.User',
                               models.DO_NOTHING,
                               db_column='UserID')
    groupname = models.CharField(db_column='GroupName',
                                 unique=True,
                                 max_length=255,
                                 blank=True,
                                 null=True)
    creationdate = models.DateField(db_column='CreationDate',
                                    blank=True,
                                    null=True)
    name = models.CharField(db_column='Name',
                            max_length=255)
    description = models.CharField(db_column='Description',
                                   max_length=255)

    pattern = models.ManyToManyField('Pattern')
    tags = models.ManyToManyField('Tags')

    class Meta:
        managed = True
        db_table = 'Group'


class Sentence(models.Model):
    id = models.AutoField(db_column='ID',
                          primary_key=True)
    userid = models.ForeignKey('Users.User',
                               models.DO_NOTHING,
                               db_column='UserID')
    sentencename = models.CharField(db_column='SentenceName',
                                    max_length=255)
    datecreated = models.DateField(db_column='DateCreated')
    subject = models.CharField(db_column='Subject',
                               max_length=255)
    receiver = models.CharField(db_column='Receiver',
                                max_length=255,
                                blank=True,
                                null=True)
    datarealizado = models.DateField(db_column='DataRealizado')
    artefacto = models.CharField(db_column='Artefacto',
                                 max_length=255)
    verbid = models.ForeignKey('Verb',
                               models.DO_NOTHING,
                               db_column='VerbID')

    group = models.ManyToManyField('Group')

    class Meta:
        managed = True
        db_table = 'Sentence'


class Verb(models.Model):
    id = models.AutoField(db_column='ID',
                          primary_key=True)
    verbname = models.CharField(db_column='VerbName',
                                unique=True,
                                max_length=255)
    verbtype = models.CharField(db_column='VerbType',
                                max_length=255)

    class Meta:
        managed = True
        db_table = 'Verb'
