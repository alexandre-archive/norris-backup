# -*- coding: utf-8 -*-

import logging
import os

logger = logging.getLogger(__name__)


class Dump(object):

    def dump_db(self, user, pwd, db, output_file):
        pass

    @classmethod
    def get_dumper(cls, engine):
        if engine in ['mariadb', 'mysql']:
            return MySQLDump()

        logger.info('Dump skypped. No dumper found for: %s' % engine)
        return Dump()


class MySQLDump(Dump):

    def dump_db(self, db, user, pwd, output_file):
        '''
        Dump database (MySQL/MariaDB).
        '''
        logger.info('Dumping DB %s to file %s...' % (db, output_file))
        os.popen('mysqldump -u %s -p%s %s > %s' % (user, pwd, db, output_file))
        logger.info('DB dump done.')
