from ldstat import app
from ldstat.database import db_session
from flask import render_template, request
from models import Batch, County, ProfessionalArea, ProfessionalGroup, Post
from flask import redirect, url_for
import simplejson as json
from config import APP_STATIC
from os import path
import datetime


# @app.route("/profession_per_municipality_weekly")
# def profession_per_municipality_weekly():
#     file_path = path.join(APP_STATIC, 'json', 'profession_per_municipality_weekly.json')
#     if path.isfile(file_path) and stat(file_path).st_mtime > time.time() - 7 * 24 * 60 * 60:
#         pass
#     else:
#         result = db_session.execute('select * from profession_per_municipality_weekly')
#         with open(file_path, 'w+') as fo:
#             fo.write(json.dumps([dict(row) for row in result], indent=4))
#     return render_template('profession_per_municipality_weekly.html')
#
@app.route("/batch_info")
def batch_info():
    result = db_session.execute("select * from batch_info order by start_time;")
    return render_template('batch_info.html', result=result)


#
# @app.route("/professional_area_per_county")
# def professional_area_per_county():
#     batch = Batch.query.order_by(Batch.id.desc()).first()
#     result = db_session.execute("select * from professional_area_per_county where batch_id = %s;" % batch.id)
#     return render_template('professional_area_per_county.html', result=result, batch=batch)
#
# @app.route("/professional_area_per_county_weekly")
# def professional_area_per_county_last_week():
#     batches = Batch.query.order_by(Batch.id.desc()).limit(2)
#     result = db_session.execute('select * from professional_area_per_county_last_week')
#     return render_template('professional_area_per_county_last_week.html', result=result, batches=batches)
#
# @app.route("/professional_area_weekly")
# def professional_area_weekly():
#     batches = Batch.query.order_by(Batch.id.desc()).limit(2)
#     result = db_session.execute('select * from professional_area_weekly')
#     return render_template('professional_area_weekly.html', result=result, batches=batches)
#
# @app.route("/county_weekly")
# def county_weekly():
#     batches = Batch.query.order_by(Batch.id.desc()).limit(2)
#     result = db_session.execute('select * from county_weekly')
#     return render_template('county_weekly.html', result=result, batches=batches)
#
# @app.route("/professional_group_per_municipality/<county_id>/<professional_area_id>")
# def professional_group_per_municipality(county_id, professional_area_id):
#     batch = Batch.query.order_by(Batch.id.desc()).first()
#     county = County.query.filter_by(id=county_id).one()
#     professional_area = ProfessionalArea.query.filter_by(id=professional_area_id).one()
#     result = db_session.execute('select * from professional_group_per_municipality where county_id = %s and professional_area_id = %s and batch_id = %s;' % (county_id, professional_area_id, batch.id))
#     return render_template('professional_group_per_municipality.html', result=result, batch=batch, county=county, professional_area=professional_area)
#
# @app.route("/profession_per_municipality/<municipality_id>/<professional_group_id>")
# def profession_per_municipality(municipality_id, professional_group_id):
#     batch = Batch.query.order_by(Batch.id.desc()).first()
#     municipality = Municipality.query.filter_by(id=municipality_id).one()
#     professional_group = ProfessionalGroup.query.filter_by(id=professional_group_id).one()
#     result = db_session.execute('select * from profession_per_municipality where municipality_id = %s and professional_group_id = %s and batch_id = %s;' % (municipality_id, professional_group_id, batch.id))
#     return render_template('profession_per_municipality.html', result=result, batch=batch, municipality=municipality, professional_group=professional_group)

# @app.route("/posts/<municipality_id>/<profession_id>")
# def posts(municipality_id, profession_id):
#     municipality = Municipality.query.filter_by(id=municipality_id).one()
#     county = municipality.county
#     profession = Profession.query.filter_by(id=profession_id).one()
#     professional_group = profession.professional_group
#     professional_area = professional_group.professional_area
#     batch = Batch.query.order_by(Batch.id.desc()).first()
#     posts = Post.query.filter(Post.batches.any(id=batch.id), Post.municipality_id == municipality.id,
#                               Post.profession_id == profession.id)
#     return render_template('posts.html', posts=posts, batch=batch, municipality=municipality, profession=profession,
#                            county=county, professional_group=professional_group, professional_area=professional_area)

@app.route("/most_common")
def most_common():
    result = db_session.execute('select * from most_common_profession')
    return render_template('most_common.html', result=result)


@app.route("/posts/<professional_group_id>/<county_id>")
def posts(professional_group_id, county_id):
    county = County.query.filter_by(id=county_id).one()
    professional_group = ProfessionalGroup.query.filter_by(id=professional_group_id).one()
    batch = Batch.query.order_by(Batch.id.desc()).first()

    posts = Post.query.filter(Post.batches.any(id=batch.id), Post.county_id == county.id,
                              Post.professional_group_id == professional_group.id).order_by(Post.num_jobs.desc()).limit(100)
    return render_template('posts.html', posts=posts, batch=batch,
                           county=county, professional_group=professional_group)


# def generate_county_json():
#     result = db_session.execute("select * from distinct_num_posts_per_week_and_county;")
#     result_list = {}
#     date_handler = lambda obj: (
#         obj.isoformat()
#         if isinstance(obj, datetime.datetime)
#            or isinstance(obj, datetime.date)
#         else None)
#     x_labels = []
#     for row in result:
#         if row['county_name'] not in result_list:
#             result_list[row['county_name']] = []
#         result_list[row['county_name']].append(row['distinct_num_posts'])
#         if row['start_time'] not in x_labels:
#             x_labels.append(row['start_time'])
#     result_flattend = [{'name': k, 'data': v} for k, v in result_list.items()]
#     output = {'result': result_flattend, 'x_labels': x_labels}
#     with open(path.join(APP_STATIC, 'json', 'county_time_series.json'), 'w+') as fo:
#         fo.write(json.dumps(output, indent=4, default=date_handler))
#
#
# def generate_professional_area_json():
#     result = db_session.execute("select * from distinct_num_posts_per_week_and_professional_area;")
#     result_list = {}
#     date_handler = lambda obj: (
#         obj.isoformat()
#         if isinstance(obj, datetime.datetime)
#            or isinstance(obj, datetime.date)
#         else None)
#     x_labels = []
#     for row in result:
#         if row['professional_area_name'] not in result_list:
#             result_list[row['professional_area_name']] = []
#         result_list[row['professional_area_name']].append(row['distinct_num_posts'])
#         if row['start_time'] not in x_labels:
#             x_labels.append(row['start_time'])
#     result_flattend = [{'name': k, 'data': v} for k, v in result_list.items()]
#     output = {'result': result_flattend, 'x_labels': x_labels}
#     with open(path.join(APP_STATIC, 'json', 'professional_area_time_series.json'), 'w+') as fo:
#         fo.write(json.dumps(output, indent=4, default=date_handler))


def generate_employer_summary_json():
    result = db_session.execute("select * from employer_summary limit 100;")
    result_list = []
    for row in result:
        result_list.append({
            'x': row['num_professional_areas'],
            'y': row['num_counties'],
            'z': row['num_posts'],
            'employer_name': row['employer_name']
        })
        # result_list.append({key:value for (key,value) in row.items()})
    with open(path.join(APP_STATIC, 'json', 'employer_summary.json'), 'w+') as fo:
        fo.write(json.dumps(result_list, indent=4))


# @app.route("/time_series")
# def time_series():
#     file_path = path.join(APP_STATIC, 'json', 'employer_summary.json')
#     if path.isfile(file_path) and stat(file_path).st_mtime > time.time() - 7 * 24 * 60 * 60:
#         pass
#     else:
#         generate_employer_summary_json()
#     file_path = path.join(APP_STATIC, 'json', 'county_time_series.json')
#     if path.isfile(file_path) and stat(file_path).st_mtime > time.time() - 7 * 24 * 60 * 60:
#         pass
#     else:
#         generate_county_json()
#     file_path = path.join(APP_STATIC, 'json', 'professional_area_time_series.json')
#     if path.isfile(file_path) and stat(file_path).st_mtime > time.time() - 7 * 24 * 60 * 60:
#         pass
#     else:
#         generate_professional_area_json()
#     return render_template('time_series.html')
#
#
# def generate_professional_area_weekly_json():
#     query = """
#     select
#         professional_area_id,
#         professional_area_name,
#         start_time,
#         sum(distinct_num_posts) as distinct_num_posts
#     from
#         distinct_posts_per_county_professional_area_week
#     group by
#         professional_area_name,
#         professional_area_id,
#         start_time
#     order by
#         professional_area_id,
#         start_time;
#     """
#     result = db_session.execute(query)
#     result_list = {}
#     date_handler = lambda obj: (
#         obj.isoformat()
#         if isinstance(obj, datetime.datetime)
#            or isinstance(obj, datetime.date)
#         else None)
#     x_labels = []
#     for row in result:
#         if row['professional_area_id'] not in result_list:
#             result_list[row['professional_area_id']] = []
#         result_list[row['professional_area_name']].append(row['distinct_num_posts'])
#         if row['start_time'] not in x_labels:
#             x_labels.append(row['start_time'])
#     result_flattend = [{'name': k, 'data': v} for k, v in result_list.items()]
#     output = {'result': result_flattend, 'x_labels': x_labels}
#     with open(path.join(APP_STATIC, 'json', 'professional_area_weekly.json'), 'w+') as fo:
#         fo.write(json.dumps(output, indent=4, default=date_handler))


@app.route("/professional_group_weekly", methods=["GET"])
def professional_group_weekly():
    county_id = request.args.get('county_id')
    county = County.query.filter_by(id=county_id).one()
    professional_area_id = request.args.get('professional_area_id')
    professional_area = ProfessionalArea.query.filter_by(id=professional_area_id).one()
    date_handler = lambda data_obj: (
        data_obj.isoformat()
        if isinstance(data_obj, datetime.datetime)
           or isinstance(data_obj, datetime.date)
        else None)
    query = """
        select
            *
        from
            distinct_num_posts_per_county_professional_group_week
        where
            county_id = %s and
            professional_area_id = %s;
        """
    result = db_session.execute(query % (county_id, professional_area_id))
    obj = {}
    for row in result:
        series_id = row['professional_group_id']
        if series_id not in obj:
            obj[series_id] = {'id': series_id, 'name': row['professional_group_name'], 'data': []}
        obj[series_id]['data'].append([row['start_time'], row['distinct_num_posts']])
    return json.dumps(obj, indent=4, default=date_handler)


@app.route("/professional_area_weekly", methods=['GET'])
def professional_area_weekly():
    professional_area_id = request.args.get('professional_area_id', None)

    date_handler = lambda data_obj: (
        data_obj.isoformat()
        if isinstance(data_obj, datetime.datetime)
           or isinstance(data_obj, datetime.date)
        else None)
    if not professional_area_id:
        query = """
        select
            professional_area_id,
            professional_area_name,
            start_time,
            sum(distinct_num_posts) as distinct_num_posts
        from
            distinct_num_posts_per_county_professional_area_week
        group by
            professional_area_id,
            professional_area_name,
            start_time
        order by
            professional_area_id,
            start_time;
        """
        result = db_session.execute(query)
        obj = {}
        for row in result:
            series_id = row['professional_area_id']
            if series_id not in obj:
                obj[series_id] = {'id': series_id, 'name': row['professional_area_name'], 'data': []}
            obj[series_id]['data'].append([row['start_time'], row['distinct_num_posts']])
    else:
        professional_area = ProfessionalArea.query.filter_by(id=professional_area_id).one()
        query = """
        select
            county_id,
            county_name,
            start_time,
            sum(distinct_num_posts) as distinct_num_posts
        from
            distinct_num_posts_per_county_professional_area_week
        where
            professional_area_id = %s
        group by
            county_id,
            county_name,
            start_time
        order by
            county_id,
            start_time;
        """
        result = db_session.execute(query % professional_area_id)
        obj = {}
        for row in result:
            series_id = row['county_id']
            if series_id not in obj:
                obj[series_id] = {'id': series_id, 'name': row['county_name'], 'data': []}
            obj[series_id]['data'].append([row['start_time'], row['distinct_num_posts']])
    return json.dumps(obj, indent=4, default=date_handler)


@app.route("/all_professional_areas_weekly")
def all_professional_areas_weekly():
    return render_template('all_professional_areas_weekly.html')


@app.route("/")
def index():
    return redirect(url_for('most_common'))
