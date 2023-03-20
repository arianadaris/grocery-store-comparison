from __main__ import db

# Products Model
class products(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    keyword = db.Column(db.String(100))
    detail = db.Column(db.String(100))
    target_tcin = db.Column(db.String(100))
    traderjoes_sku = db.Column(db.String(100))

    def __init__(self, name, image, keyword, detail):
        self.name = name
        self.image = image
        self.keyword = keyword
        self.detail = detail
        self.target_tcin = 0
        self.traderjoes_sku = 0

    def __repr__(self):
        return f'{self.name} ({self.keyword}, {self.detail}): {self.target_tcin}, {self.traderjoes_sku}'
    
    def as_dict(self):
        return {
            'id': self._id,
            'name': self.name,
            'image': self.image,
            'keyword': self.keyword,
            'detail': self.detail,
            'target_tcin': self.target_tcin,
            'traderjoes_sku': self.traderjoes_sku,
        }
    
    def set_target_tcin(self, tcin):
        self.target_tcin = tcin

    def set_traderjoes_sku(self, sku):
        self.traderjoes_sku = sku