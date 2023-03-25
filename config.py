from urllib.parse import urlparse

ENV = "prod"

if ENV == 'dev':
    DATABASE_CONFIG = {
        'host': "localhost",
        'database': "babyfoot",
        'user': "postgres",
        'password': "519173"
    }
else: 

    uri = "postgres://mzallduhesqqds:f18bf72dfd0e2415db010290b8192be8c92e4e1d257205808e9dedead1d0c091@ec2-44-214-132-149.compute-1.amazonaws.com:5432/dd2oto7f7bkek8"
    parsed_uri = urlparse(uri)

    DATABASE_CONFIG = {
        'host': "ec2-44-214-132-149.compute-1.amazonaws.com",
        'database': "dd2oto7f7bkek8",
        'user': "mzallduhesqqds",
        'password': "f18bf72dfd0e2415db010290b8192be8c92e4e1d257205808e9dedead1d0c091",
        'port': "5432"
    }