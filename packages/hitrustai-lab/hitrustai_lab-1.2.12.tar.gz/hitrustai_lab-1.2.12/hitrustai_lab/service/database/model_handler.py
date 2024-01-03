

class ModelHandler:
    def __init__(self, db_settings: dict, logger):
        self.db = db_settings.get('db')
        self.info = db_settings.get('table_info')
        self.result = db_settings.get('table_result')
        self.table = db_settings.get('table')
        self.logger = logger

    def save_data(self, data_type, **input_data):
        try:
            if data_type == 'info':
                input_model = self.info(**input_data)
            elif data_type == 'result':
                input_model = self.result(**input_data)
            else:
                input_model = self.table(**input_data)

            self.db.session.add(input_model)
            self.db.session.commit()
            return input_model

        except:
            self.db.session.rollback()
            self.logger.exception(
                f"[{input_model.serial_number}]Save data into {input_model.__tablename__} failed")
