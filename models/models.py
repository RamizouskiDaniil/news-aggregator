class Article:
    def __init__(self,id, title, description, link, pubDate, source):
        self.id = id
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate
        self.source = source

class Favorite:
    def __init__(self, id, title, description, link, pubDate, created, source):
        self.id = id
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate
        self.created = created
        self.source = source


