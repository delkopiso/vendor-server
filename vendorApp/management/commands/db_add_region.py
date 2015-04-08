#!/usr/bin/env python
import os

from django.core.management.base import BaseCommand, CommandError
from mongoengine import connect
from vendorApp.models import Article

class Command(BaseCommand):
    help = 'Adds the region field to the database model'

    def handle(self, *args, **options):
        # connect to MongoDB
        conn_uri = os.environ.get('MONGOLAB_URI')
        DB_NAME = 'vendor'
        if conn_uri is not None:  # production env
            connect(DB_NAME, host=conn_uri)
        else:  # development env, using localhost
            connect(DB_NAME)

        Article.objects().update(set__region='nigeria')
        self.stdout.write('Successfully updated all records to include the field {"region": "nigeria"}')
