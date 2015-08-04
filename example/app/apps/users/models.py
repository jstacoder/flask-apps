from ...base import BaseModel,sa
           
class User(BaseModel):
    name = sa.Column(sa.String(255))
    comments = sa.orm.relation('Comment',lazy='dynamic')
        
