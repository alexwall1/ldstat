from sqlalchemy import Table, Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import json


def encode_results(results):
    array = []
    for obj in results:
        fields = {}
        for field in obj.keys():
            data = obj.__getattribute__(field)
            try:
                if isinstance(data, datetime):
                    fields[field] = data.isoformat()
                else:
                    json.dumps(data)
                    fields[field] = data
            except TypeError:
                fields[field] = None
        array.append(fields)
    return array


batch_post_table = Table('batch_post', Base.metadata,
                         Column('batch_id', Integer, ForeignKey('batch.id')),
                         Column('post_id', Integer, ForeignKey('post.id'))
                         )


class Batch(Base):
    __tablename__ = 'batch'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    last_in = Column(String)
    complete = Column(Boolean)
    posts = relationship("Post", secondary=batch_post_table, back_populates="batches")

    def __init__(self):
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        self.complete = False

    def __repr__(self):
        return '<Batch %r (id=%r)>' % (self.start_time, self.id)


class County(Base):
    __tablename__ = 'county'
    url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/soklista/lan'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<County %r (id=%r)>' % (self.name, self.id)


class ProfessionalArea(Base):
    __tablename__ = 'professional_area'
    url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/soklista/yrkesomraden'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<ProfessionalArea %r (id=%r)>' % (self.name, self.id)


class ProfessionalGroup(Base):
    __tablename__ = 'professional_group'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    professional_area_id = Column(Integer, ForeignKey('professional_area.id'))
    professional_area = relationship('ProfessionalArea', backref=backref('professional_groups', lazy='dynamic'))

    def __init__(self, id, name, professional_area):
        self.id = id
        self.name = name
        self.professional_area = professional_area

    def __repr__(self):
        return '<ProfessionalGroup %r (id=%r)>' % (self.name, self.id)


class Profession(Base):
    __tablename__ = 'profession'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False, index=True)
    professional_group_id = Column(Integer, ForeignKey('professional_group.id'))
    professional_group = relationship('ProfessionalGroup', backref=backref('professions', lazy='dynamic'))

    def __init__(self, id, name, professional_group):
        self.id = id
        self.name = name
        self.professional_group = professional_group

    def __repr__(self):
        return '<Profession %r (id=%r)>' % (self.name, self.id)


class Post(Base):
    __tablename__ = 'post'
    url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/%s'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    external_id = Column(String(100), unique=True, nullable=False, index=True)

    batches = relationship("Batch", secondary=batch_post_table, back_populates="posts")

    municipality_id = Column(Integer, ForeignKey('municipality.id'))
    municipality = relationship('Municipality', backref=backref('posts', lazy='dynamic'))
    county_id = Column(Integer, ForeignKey('county.id'))
    county = relationship('County', backref=backref('posts', lazy='dynamic'))
    profession_id = Column(Integer, ForeignKey('profession.id'))
    profession = relationship('Profession', backref=backref('posts', lazy='dynamic'))
    professional_group_id = Column(Integer, ForeignKey('professional_group.id'))
    professional_group = relationship('ProfessionalGroup', backref=backref('posts', lazy='dynamic'))
    # professional_area_id = Column(Integer, ForeignKey('professional_area.id'))
    # professional_area = relationship('ProfessionalArea', backref=backref('posts', lazy='dynamic'))

    # meta data
    is_active = Column(Boolean, default=True)
    is_complete = Column(Boolean, default=False)

    # easily accessed data
    published = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    num_jobs = Column(Integer, nullable=True)

    # raw data
    match_data = Column(JSON)  # "matchningdata"
    ad_data = Column(JSON)  # "annons"
    application_data = Column(JSON)  # "ansokan"
    employer_data = Column(JSON)  # "arbetsplats"
    condition_data = Column(JSON)  # "villkor"

    def __repr__(self):
        return '<Post %s>' % self.external_id

    def get_url(self):
        return Post.url % self.external_id


class Municipality(Base):
    __tablename__ = 'municipality'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    county_id = Column(Integer, ForeignKey('county.id'))
    county = relationship('County', backref=backref('municipalities', lazy='dynamic'))

    def __init__(self, id, name, county):
        self.id = id
        self.name = name
        self.county = county

    def __repr__(self):
        return '<Municipality %r (id=%r)>' % (self.name, self.id)
