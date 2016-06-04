# ldstat

deployment
1. import ldstat (this ensures config is loaded)
1. import the db object from models and run db.create_all()
2. populate database with Counties and Professional Areas by importing the classes and running get_objects(cls)
3. continue by populating subgroups by running get_professional_groups, get_municipalities and get_professions from batch
4. populate posts by running get_posts from batch