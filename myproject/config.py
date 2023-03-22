from urllib.parse import urlparse

ENV = "PROD"

if ENV == 'dev':
    DATABASE_CONFIG = {
        'host': "localhost",
        'database': "babyfoot",
        'user': "postgres",
        'password': "519173"
    }
else: 

    uri = "postgres://sbizzhblpgkxep:1d908f276d27a024a11e115e880bde5221483445737911f2cb1e3d927b35d400@ec2-3-234-204-26.compute-1.amazonaws.com:5432/df3id0m5ik8i37"
    parsed_uri = urlparse(uri)

    DATABASE_CONFIG = {
        'host': "ec2-3-234-204-26.compute-1.amazonaws.com",
        'database': "df3id0m5ik8i37",
        'user': "sbizzhblpgkxep",
        'password': "1d908f276d27a024a11e115e880bde5221483445737911f2cb1e3d927b35d400",
        'port': "5432"
    }

