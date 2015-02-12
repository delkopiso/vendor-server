from django.db import models

# Create your models here.

class Article(object):
    def __init__(self, _id, title, text, source, coverPic, section, logo, index):
        self.id = _id
        self.title = title
        self.text = text
        self.source = source
        self.coverPic = coverPic
        self.section = section
        self.logo = logo
        self.index = index


