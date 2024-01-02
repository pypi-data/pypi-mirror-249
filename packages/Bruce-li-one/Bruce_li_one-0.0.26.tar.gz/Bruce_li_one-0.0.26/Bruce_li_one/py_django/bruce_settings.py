
class Bruce_sql():
    def __init__(self,database_name:str,host:str="127.0.0.1",user:str="root",password="123456"):
        self.HOST=host
        self.USER=user
        self.PASSWORD=password
        self.DATABASE_NAME=database_name

    def dj_mysql(self,port:str="3306"):
        data_dict={
            'ENGINE': 'django.db.backends.mysql',
            "HOST": self.HOST,
            "NAME": self.DATABASE_NAME,
            "USER": self.USER,
            "PASSWORD": self.PASSWORD,
            "PORT": port
        }
        return data_dict
    def dj_oracle(self,port:str="1521"):
        data_dict = {
            'ENGINE': 'django.db.backends.oracle',
            "HOST": self.HOST,
            "NAME": self.DATABASE_NAME,
            "USER": self.USER,
            "PASSWORD": self.PASSWORD,
            "PORT": port
        }
        return data_dict

    def dj_postgresql(self):
        data_dict={
            "ENGINE": "django.db.backends.postgresql",
            "NAME": self.DATABASE_NAME,
            "USER": self.USER,
            "PASSWORD":  self.PASSWORD,
            "HOST": self.HOST,
            "PORT": "5432",
        }
        return data_dict

    def dj_sqlite3(self,databse_path:str):
        data_dict = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": databse_path
        }
        return data_dict


class Bruce_settings():
    def local(self):
        pass
    def dev(self):
        pass
    def prod(self):
        pass