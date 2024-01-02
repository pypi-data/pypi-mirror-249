
import os
class Bruce_generate:
    def __init__(self,BASE_DIR:str):
        #self.FILE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.FILE_PATH = str(BASE_DIR)
    def make_one(self):
        """
        一键生成
        """
        self.make_run_sh()
        self.make_run_bat()
        self.make_migrate_bat()
        self.make_migrate_sh()

    def make_migrate_bat(self)->bool:
        """
        生成django项目windows的迁移文件
        """
        try:
            data="python manage.py makemigrations  && python manage.py migrate"
            file_name="migrate.bat"
            # 返回脚本绝对路径
            #path=os.path.abspath(__file__)
            # 返回脚本上一层目录路径
            #root_path1 = os.path.dirname(os.path.abspath(__file__))
            # 返回脚本上两层目录路径
            #root_path2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(self.FILE_PATH+"\\"+file_name, 'w') as file:
                file.write(data)
            return True
        except Exception as e:
            return False

    def make_migrate_sh(self):
        """
        生成django项目liunx的迁移文件
        """
        try:
            data = "python manage.py makemigrations  && python manage.py migrate"
            file_name = "migrate.sh"
            with open(self.FILE_PATH + "\\" + file_name, 'w') as file:
                file.write(data)
            return True
        except Exception as e:
            return False

    def make_run_bat(self,port=8000):
        """
        生成django项目windows的bat运行文件
        """
        try:
            data = "python manage.py runserver 0.0.0.0:8000"
            file_name = "run.bat"
            with open(self.FILE_PATH + "\\" + file_name, 'w') as file:
                file.write(data)
            return True
        except Exception as e:
            return False
        pass
    def make_run_sh(self,port=8000):
        """
        生成django项目liunx的sh运行文件
        """
        data="python manage.py runserver 0.0.0.0:8000"
        file_name = "run.sh"
        try:
            data = "python manage.py runserver 0.0.0.0:8000"
            file_name = "run.sh"
            with open(self.FILE_PATH + "\\" + file_name, 'w') as file:
                file.write(data)
            return True
        except Exception as e:
            return False


