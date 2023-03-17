from __main__ import db


# Products Model
class products(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    keyword = db.Column(db.String(100))
    detail = db.Column(db.String(100))
    target_tcin = db.Column(db.String(100))
    kroger_id = db.Column(db.String(100))
    walmart_id = db.Column(db.String(100))

    def __init__(self, name, keyword, detail, target_tcin):
        self.name = name
        self.keyword = keyword
        self.detail = detail
        self.target_tcin = target_tcin
        self.kroger_id = 2
        self.walmart_id = 3

    def __str__(self):
        return f'{self.name} ({self.keyword}, {self.detail}): {self.target_tcin}, {self.kroger_id}, {self.walmart_id}'
    
    def as_dict(self):
        return {
            'name': self.name,
            'keyword': self.keyword,
            'detail': self.detail,
            'target_tcin': self.target_tcin,
            'kroger_id': self.kroger_id,
            'walmart_id': self.walmart_id
        }
    