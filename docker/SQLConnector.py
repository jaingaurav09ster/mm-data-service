from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from docker.Logging import get_output_handler
from docker.config import DATABASE_CONFIG

# Initialise the declarative base to be used elsewhere in the models
Base = declarative_base()


class SQLConnector:
    def __init__(self, echo=False, logger=None, severity=None):
        output_handler = get_output_handler(logger=logger, severity=severity)
        output_handler("Trying to connect to DB.")

        self._create_engine(echo)

        output_handler(" *** DB Engine configured with {}".format(self.engine))
        self.Session = sessionmaker(bind=self.engine)
        output_handler('DB Access Configured (but not yet connected).')

    def _create_engine(self, echo):
        if not eval(DATABASE_CONFIG['USE_KERBEROS']):
            if not eval(DATABASE_CONFIG['USE_DSN']):
                self.engine = create_engine(
                    "{dialect}://{user}:{pwd}@{host}:{port}/{dbname}".format(
                        user=DATABASE_CONFIG["DB_USER"],
                        pwd=DATABASE_CONFIG["DB_PWD"],
                        host=DATABASE_CONFIG["DB_HOST"],
                        port=DATABASE_CONFIG["DB_PORT"],
                        dbname=DATABASE_CONFIG['DB_NAME'],
                        dialect=DATABASE_CONFIG['DIALECT_DRIVER']
                    ), echo=echo)
            else:
                dsn_name = DATABASE_CONFIG['DSN_NAME']
                self.engine = create_engine(
                    "{dialect}://{user}:{pwd}@{dsn_name}".format(
                        user=DATABASE_CONFIG["DB_USER"],
                        pwd=DATABASE_CONFIG["DB_PWD"],
                        dsn_name=dsn_name,
                        dialect=DATABASE_CONFIG['DIALECT_DRIVER'],
                    ), connect_args={
                        'Database': DATABASE_CONFIG['DB_NAME']
                    },
                    echo=echo)
        else:
            # We use Kerberos
            if not eval(DATABASE_CONFIG['USE_DSN']):
                self.engine = create_engine(
                    "{dialect}://{host}:{port}/{dbname}".format(
                        host=DATABASE_CONFIG["DB_HOST"],
                        port=DATABASE_CONFIG["DB_PORT"],
                        dbname=DATABASE_CONFIG['DB_NAME'],
                        dialect=DATABASE_CONFIG['DIALECT_DRIVER']
                    ),
                    connect_args={'auth': 'KERBEROS',
                                  'Trusted_Connection': 'YES',
                                  'encrypt': 'yes',
                                  'trustServerCertificate': 'yes',
                                  'loginTimeout': 200,
                                  'TrustedCerts': DATABASE_CONFIG['KERBEROS_CERT_PATH'],
                                  'multiSubnetFailover': 'yes'})
            else:
                # We use Kerberos and DSN
                dsn_name = DATABASE_CONFIG['DSN_NAME']
                self.engine = create_engine(
                    "{dialect}://{dsn_name}".format(
                        dsn_name=dsn_name,
                        dialect=DATABASE_CONFIG['DIALECT_DRIVER']
                    ),
                    connect_args={'auth': 'KERBEROS',
                                  'Trusted_Connection': 'YES',
                                  'encrypt': 'yes',
                                  'trustServerCertificate': 'yes',
                                  'loginTimeout': 200,
                                  'TrustedCerts': DATABASE_CONFIG['KERBEROS_CERT_PATH'],
                                  'multiSubnetFailover': 'yes'})
