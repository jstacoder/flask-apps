from sqlalchemy.ext.declarative import declared_attr,declarative_base
from inflection import pluralize, underscore
import sqlalchemy as sa
import os
import datetime
import decimal
import json
import sys
        
class classproperty(object):
    def __init__(self,getter):
        self.getter = getter
    
    def __get__(self,instance,owner):
        return self.getter(owner)
                
class BaseModel(declarative_base()):
    _session = None
    _engine = None
    _query = None

    __abstract__ = True
    
    def save(self):
        self.session.add(self)
        self.session.commit()
        return self
    
    def delete(self):
        self.session.delete(self)
                    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get(cls,id):
        return cls.query.get(id)
                
    @classproperty
    def query(cls):
        if cls._query is None:
            cls._query = cls.session.query(cls)
        return cls._query
                
    @classproperty
    def session(cls):
        if BaseModel._session is None:
            BaseModel._session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=cls.engine))
        return BaseModel._session

    @classproperty
    def engine(cls):
        if BaseModel._engine is None:
            BaseModel._engine = sa.create_engine(os.environ.get('DATABASE_URI','sqlite:///test.db'))
        return BaseModel._engine
    
    @declared_attr
    def id(self):
        return sa.Column(sa.Integer,primary_key=True)
                
    @declared_attr
    def __tablename__(self):
        return underscore(pluralize(self.__name__))

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            ARGS = ('year', 'month', 'day', 'hour', 'minute',
                    'second', 'microsecond')
            return {'__type__': 'datetime.datetime',
                    'args': [getattr(obj, a) for a in ARGS],
                    'string':str(obj)}
        elif isinstance(obj, datetime.date):
            ARGS = ('year', 'month', 'day')
            return {'__type__': 'datetime.date',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, datetime.time):
            ARGS = ('hour', 'minute', 'second', 'microsecond')
            return {'__type__': 'datetime.time',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, datetime.timedelta):
            ARGS = ('days', 'seconds', 'microseconds')
            return {'__type__': 'datetime.timedelta',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, decimal.Decimal):
            return {'__type__': 'decimal.Decimal',
                    'args': [str(obj),]}
        else:
            return super(EnhancedJSONEncoder,self).default(obj)
        
        
class EnhancedJSONDecoder(json.JSONDecoder):            
    def __init__(self, *args, **kwargs):
        super(EnhancedJSONDecoder,self).__init__(*args, object_hook=self.object_hook,
                **kwargs)
        
    def object_hook(self, d): 
        if '__type__' not in d:
            return d
        o = sys.modules[__name__]
        for e in d['__type__'].split('.'):
            o = getattr(o, e)
        args, kwargs = d.get('args', ()), d.get('kwargs', {})
        return o(*args, **kwargs)


def dumps(*args,**kwargs):
    return json.dumps(cls=EnhancedJSONEncoder,*args,**kwargs)

def loads(*args,**kwargs):
    return json.loads(cls=EnhancedJSONDecoder,*args,**kwargs)
