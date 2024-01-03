import numpy as np
import pandas as pd
from sqlalchemy import update
from sqlalchemy.pool import QueuePool
from sqlalchemy import asc, desc, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, load_only


def get_orm_profile(host='192.168.10.201', db='acqfd_test', **kwargs):

    profile = {
        'host': host,
        'port': '3306',
        'user': 'acqfd',
        'pwd': 'acqfd16313302',
        'db': db
    }

    if kwargs:
        profile.update(kwargs)

    return profile


class Orm():
    def __init__(
        self,
        profile=get_orm_profile(),
        pool=False,
        pool_size=250,
        max_overflow=0,
        pool_recycle=10,
        pool_timeout=10,
        logger=None
    ):
        self.profile = profile
        self.DB_URL = f"{profile['user']}:{profile['pwd']}@{profile['host']}:{profile['port']}"
        self.sql_connect = f"mysql+pymysql://{self.DB_URL}/{profile['db']}?charset=utf8mb4&binary_prefix=true"
        if pool:
            self.engine = create_engine(
                self.sql_connect,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_recycle=pool_recycle,
                pool_timeout=pool_timeout,
                pool_pre_ping=True,
                poolclass=QueuePool,
                pool_use_lifo=True
            )
        else:
            self.engine = create_engine(self.sql_connect, echo=False)
        self._sessionmaker = sessionmaker(bind=self.engine)
        self.session = scoped_session(self._sessionmaker)
        self.logger = logger

    def create_schema(self):
        schemaName = self.profile['db']
        engine = create_engine(f'mysql+pymysql://{self.DB_URL}')

        conn = engine.connect()
        if schemaName.lower() not in conn.dialect.get_schema_names(conn):
            if self.logger is not None:
                self.logger.warning(
                    f'Schema {schemaName} not exist, create {schemaName}.')
            engine.execute(f"CREATE SCHEMA {schemaName}")
            conn.close()
            if self.logger is not None:
                self.logger.warning(f'Done creating schema {schemaName}')

        # disconnect database
        engine.dispose()

    def get_session(self):
        return scoped_session(self._sessionmaker)

    @staticmethod
    def close_connection(session):
        session.close()

    def create_table(self, base, table):
        '''Create a table in DB'''

        engine = create_engine(self.sql_connect, echo=True)
        table
        base.metadata.create_all(engine)

    def truncate_table(self, table_name: str):
        con = self.engine.connect()
        con.execute(f"TRUNCATE TABLE {table_name};")
        con.close()
        print("TRUNCATE has completed")

    def delete(self, data: pd.DataFrame, tablename):
        '''Delete data in DB'''

        session = self.get_session()
        for i in range(data.shape[0]):
            kwargs = data.iloc[i].to_dict()
            query_data = session.query(tablename).filter_by(**kwargs).all()
            for row in query_data:
                session.delete(row)
                session.commit()
        session.close()

    def get_log_position(self):
        result = pd.read_sql(f"show master status;", self.session.bind)
        position = result['Position'].values[0]
        return position

    def check_sn(self, tablecolumn, sn: str):
        '''Check if a sn is in a table'''

        session = self.get_session()
        try:
            check_sn = session.query(tablecolumn).filter_by(sn=sn).all()
            session.close()

            if len(check_sn) == 0:
                return True
            return False

        except:
            session.rollback()

    def query(self, table, *filterBy, **conditions):
        '''Get data from DB'''

        session = self.get_session()
        query = session.query(table).filter(*filterBy)

        if conditions.get('orderBy'):
            if conditions['orderBy'] == 'asc':
                query = query.order_by(asc(conditions['orderTarget']))
            else:
                query = query.order_by(desc(conditions['orderTarget']))

        if conditions.get('limit'):
            query = query.limit(conditions['limit'])

        if conditions.get('fields'):
            query = query.options(load_only(*conditions['fields']))

        result = pd.read_sql_query(query.statement, session.connection())
        session.close()

        for c in ['pk_id', 'create_time']:
            if c in result.columns:
                result = result.drop(c, axis=1)
        return result

    def query_filter(self, tablename, limit: int = None, order_by: tuple = None, fields: list = None, *args):
        '''Get data from DB'''

        session = self.get_session()
        query = session.query(tablename).filter(*args)

        if order_by:
            if order_by[1] == 'asc':
                query = query.order_by(asc(order_by[0]))
            else:
                query = query.order_by(desc(order_by[0]))

        if limit:
            query = query.limit(limit)

        if fields:
            query = query.options(load_only(*fields))

        result = pd.read_sql(query.statement, session.bind)
        session.close()

        return result

    def elk_query_filter(self, tablename, limit=None, *args):
        query = self.session.query(tablename).filter(*args)
        if limit:
            query = query.limit(limit)
        return pd.read_sql(query.statement, self.session.bind)

    def update(self, table, update_content: dict, *filterBy):
        '''Update data in table'''

        session = self.get_session()
        session.execute(
            update(table).where(*filterBy).values(update_content)
        )
        session.commit()
        session.close()

    def delete(self, table, *args):
        '''Delete data in table'''

        session = self.get_session()
        query_data = session.query(table).filter(*args).all()
        for row in query_data:
            session.delete(row)
            session.commit()
        session.close()

    def check_exist(self, tablename, **kwargs):
        '''用於確認指定資料是否存在'''
        session = self.get_session()
        q = session.query(tablename).filter_by(**kwargs)
        check_result = session.query(q.exists()).scalar()
        session.close()
        return check_result

    def add_data(self, table, **input_data):
        '''Add single data row to table'''

        try:
            session = self.get_session()
            data = table(**input_data)
            session.add(data)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def data_to_DB(self, df: pd.DataFrame, table):
        '''Import dataframe to DB'''

        # 轉換時間格式
        for col in df.columns:
            if df[col].dtype == pd._libs.tslibs.timestamps.Timestamp:
                df[col] = df[col].astype(str).apply(
                    lambda x: None if x == 'NaT' else x)

        # 補空值
        if df.isnull().sum().sum():
            df = df.where(pd.notnull(df), '')

        datarows = np.array(df.to_dict('records'))
        alldata = np.array([table(**row) for row in datarows])

        # upload data
        session = self.get_session()
        session.add_all(alldata)
        session.commit()
        session.close()


def main():
    from sqlalchemy import Column, text, Integer
    from sqlalchemy.dialects.mysql import TIMESTAMP
    from sqlalchemy.ext.declarative import declarative_base

    orm = Orm(
        profile={
            'host': '192.168.10.201',
            'port': '3306',
            'user': 'acqfd',
            'pwd': 'acqfd16313302',
            'db': 'acqfd_test'
        }
    )

    Base = declarative_base()
    metadata = Base.metadata

    class TestTable(Base):
        __tablename__ = 'udid_history'

        pk_id = Column(Integer, primary_key=True,
                       autoincrement=True, unique=True)
        create_time = Column(TIMESTAMP(fsp=6), nullable=False,
                             server_default=text("CURRENT_TIMESTAMP(6)"))

    # 建立資料表
    orm.create_table(Base, TestTable)
    print('Create table done.')


if __name__ == "__main__":
    main()
