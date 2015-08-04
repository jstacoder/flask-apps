from ...base import BaseModel,sa,dumps
            
class Comment(BaseModel):
    text = sa.Column(sa.Text)
    date_added = sa.Column(sa.DateTime,default=sa.func.now())
    user_id = sa.Column(sa.Integer,sa.ForeignKey('users.id'))
    user = sa.orm.relation('User',uselist=False)

    def _to_json(self):
        return dict(
            text=self.text,
            date=self.date_added,
            user=self.user.name
        )

