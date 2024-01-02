

class Bruce_generate:
    def make_migrate_bat(self):
        """
        生成flask项目windows的迁移文件
        """
        data="flask db migrate && flask db upgrade"
        file_name = "migrate_bat"
        pass
    def make_migrate_sh(self):
        """
        生成flask项目liunx的迁移文件
        """
        data="flask db migrate && flask db upgrade"
        file_name = "migrate_sh"
        pass
    def make_run_bat(self,host="",port=8000):
        """
        生成flask项目windows的bat运行文件
        """
        data="flask  --app app.py run -h 0.0.0.0 -p 8000 --debug"
        file_name = "run.bat"
        pass
    def make_run_sh(self,host="",port=8000):
        """
        生成flask项目liunx的sh运行文件
        """
        data="flask  --app app.py run -h 0.0.0.0 -p 8000 --debug"
        file_name="run.sh"
        pass