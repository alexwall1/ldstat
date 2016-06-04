import simplejson as json
from datetime import datetime
from sys import getsizeof
import logging

import requests
from database import db_session
from models import County, Municipality, ProfessionalArea, ProfessionalGroup, Profession, Post, Batch
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from dateutil.parser import parse
from sqlalchemy import and_
from ldstat import app

logger = logging.getLogger(__name__)


def get_objects(cls):
    headers = {'Accept-Language': 'sv', 'Accept': 'application/json'}
    response = requests.get(url=cls.url, headers=headers)
    obj = json.loads(response.text)
    arr = obj["soklista"]["sokdata"]
    for item in arr:
        try:
            instance = cls.query.filter_by(id=item["id"]).one()
            app.logger.warn('%s already exists' % instance)
        except NoResultFound:
            instance = cls(item["id"], item["namn"])
            db_session.add(instance)
            db_session.commit()
            app.logger.info('Adding %s' % instance)


def update_posts(batch_id):
    try:
        headers = {'Accept-Language': 'sv', 'Accept': 'application/json'}
        Batch.query.filter_by(id=batch_id).one()
        posts = Post.query.filter()
        posts = Post.query.filter(and_(Post.batch_id == batch_id, Post.is_active == True, Post.deadline == None))
        app.logger.debug('Attempting to update %s posts' % len(posts.all()))
        for post in posts:
            try:
                response = requests.get(url=(post.url % post.external_id), headers=headers)
                app.logger.debug('Received %s byte response for %s' % (getsizeof(response), post.external_id))
                obj = json.loads(response.text)
                body = obj["platsannons"]
                if "ansokan" in body:
                    post.application_data = body.get("ansokan")
                    deadline = parse(post.application_data["sista_ansokningsdag"]).replace(tzinfo=None)
                    if deadline < datetime.now():
                        post.is_active = False
                    post.deadline = deadline
                    app.logger.debug('Updated %s with deadline %s' % (post.external_id, post.deadline))
                if "villkor" in body:
                    post.condition_data = body.get("villkor")
                if "arbetsplats" in body:
                    post.employer_data = body.get("arbetsplats")
                db_session.commit()
            except KeyError as e:
                app.logger.error('Could not parse attribute "%s" for %s. Aborting.' % (e, post.external_id))
            except ValueError as e:
                app.logger.error('Could not parse API response as JSON. Aborting.')
                app.logger.debug(e)
    except NoResultFound:
        app.logger.error('No batch with id %s' % batch_id)


def get_posts():
    batch = Batch()
    db_session.add(batch)
    db_session.commit()

    s = requests.Session()
    s.headers.update({'Accept-Language': 'sv', 'Accept': 'application/json'})

    for county in County.query.all():
        app.logger.info('Getting posts for %s' % county)
        _get_posts(s, batch, county.id, 10000, 1)
    batch.end_time = datetime.now()
    batch.complete = True
    batch.last_in = db_session.query(func.max(Post.external_id)).scalar()
    db_session.add(batch)
    db_session.commit()


def _get_posts(s, batch, county_id, n, p):
    url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/matchning?lanid=%s&antalrader=%s&sida=%s' % (county_id, n, p)
    response = s.get(url=url)

    try:
        obj = json.loads(response.text)
        for index, item in enumerate(obj["matchningslista"]["matchningdata"]):
            try:
                post = Post.query.filter_by(external_id=str(item["annonsid"])).first()
                if post:
                    app.logger.info('Post %s already exists, adding to new batch.' % post.external_id)
                else:
                    post = Post()
                    post.external_id = str(item["annonsid"])
                    post.published = parse(item["publiceraddatum"])
                    
                    # profession is mandatory
                    post.profession = Profession.query.filter_by(name=item["yrkesbenamning"]).one()

                    if "antalplatser" in item:
                        try:
                            post.num_jobs = int(item["antalplatser"])
                        except ValueError:
                            app.logger.warning('Could not parse number of jobs for %s' % post.external_id)

                    # municipality is optional
                    try:
                        post.municipality = Municipality.query.filter_by(id=int(item["kommunkod"])).one()
                    except (NoResultFound, KeyError):
                        app.logger.warning('No municipality match "%s", post annonsid=%s, saving with unspecified.' % (item["kommunkod"], post.external_id))
                        post.municipality = Municipality.query.filter_by(id="Ospecifierad arbetsort").one()

                    post.match_data = item
                    db_session.add(post)
                post.batches.append(batch)
                db_session.commit()
                db_session.flush()
            except KeyError as e:
                app.logger.error('Attribute "%s" missing from dict. Aborting.' % e)
                app.logger.debug(json.dumps(item, indent=4))
            except IntegrityError:
                app.logger.warning('Post already exists for %s' % item["annonsid"])
                db_session.rollback()
            except ValueError as e:
                app.logger.error(e)
                app.logger.debug(json.dumps(item, indent=4))
            except NoResultFound as e:
                app.logger.error('Could not find match for %s. Aborting.' % item["annonsid"])
                app.logger.debug(e)

        # fixme: this will abort parsing if server runs out of memory
        pages = obj["matchningslista"]["antal_sidor"]
        if p < pages:
            app.logger.debug('Retrieving page %s of %s' % (p + 1, pages))
            _get_posts(s, batch, county_id, n, p + 1)
    except ValueError:
        app.logger.error('Could not parse json response from API. Aborting.')
        app.logger.debug(response.text)


def get_municipalities():
    # try getting all municipalities in one batch
    headers = {'Accept-Language': 'sv', 'Accept': 'application/json'}
    for county in County.query.all():
        url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/soklista/kommuner?lanid=%s' % county.id
        response = requests.get(url=url, headers=headers)
        obj = json.loads(response.text)

        app.logger.info('Getting all municipalities in %s' % county)

        try:
            for item in obj["soklista"]["sokdata"]:
                try:
                    municipality = Municipality.query.filter_by(id=item["id"]).one()
                except NoResultFound:
                    municipality = Municipality(item["id"], item["namn"], county)
                    db_session.add(municipality)
                    db_session.commit()

                    app.logger.info('Adding %s' % municipality)
        except KeyError:
            app.logger.error('Could not read response.\n%s' % response.text)


def get_professional_groups():
    headers = {'Accept-Language': 'sv', 'Accept': 'application/json'}
    for area in ProfessionalArea.query.all():
        url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/soklista/yrkesgrupper?yrkesomradeid=%s' % area.id
        response = requests.get(url=url, headers=headers)
        obj = json.loads(response.text)
        try:
            for item in obj["soklista"]["sokdata"]:
                try:
                    instance = ProfessionalGroup.query.filter_by(id=item["id"]).one()
                    app.logger.warn('%s already exists' % instance)
                except NoResultFound:
                    instance = ProfessionalGroup(item["id"], item["namn"], area)
                    db_session.add(instance)
                    db_session.commit()
                    app.logger.info('Adding %s' % instance)
        except KeyError:
            app.logger.error('Could not read response.\n%s' % response.text)


def get_professions():
    headers = {'Accept-Language': 'sv', 'Accept': 'application/json'}
    for group in ProfessionalGroup.query.all():
        url = 'http://api.arbetsformedlingen.se/af/v0/platsannonser/soklista/yrken?yrkesgruppid=%s' % group.id
        response = requests.get(url=url, headers=headers)
        obj = json.loads(response.text)
        try:
            for item in obj["soklista"]["sokdata"]:
                try:
                    instance = Profession.query.filter_by(id=item["id"]).one()
                    app.logger.warn('%s already exists' % instance)
                except NoResultFound:
                    instance = Profession(item["id"], item["namn"], group)
                    db_session.add(instance)
                    db_session.commit()
                    app.logger.info('Adding %s' % instance)
        except KeyError:
            app.logger.error('Could not read response.\n%s' % response.text)
