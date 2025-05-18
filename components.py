import sqlite3


class DataBaseDebugging:
    def __init__(self, database_file_name="DB_users.sqlite"):
        self.Database_file_name = database_file_name
        self.con = sqlite3.connect(self.Database_file_name, check_same_thread=False)
        self.cur = self.con.cursor()

    def create_circle(self, circle_name_: str, err=False):
        sql_req = f"""
            CREATE TABLE {circle_name_} (
            id REFERENCES Users (id) 
            );
            """
        try:
            self.cur.execute(sql_req)
            self.con.commit()
            return True
        except Exception as e:
            if err:
                return e
            return False

    def delete_circle(self, circle_name_: str, err=False):
        sql_req = f"""
            DROP TABLE {circle_name_}
            """
        try:
            self.cur.execute(sql_req)
            self.con.commit()
            return True
        except Exception as e:
            if err:
                return e
            return False

    def get_circles(self):
        sql_req = """
            SELECT name FROM sqlite_master WHERE type = 'table'
            """
        res = []
        for i_ in self.cur.execute(sql_req).fetchall():
            i = i_[0]
            if i in ("Users", "Admins"):
                res.append(i)
        return res

    def get_users(self):
        sql_req = """
            SELECT * FROM Users
            """
        return self.cur.execute(sql_req).fetchall()

    def get_admins(self):
        sql_req = """
            SELECT * FROM Admins
            """
        return self.cur.execute(sql_req).fetchall()

    def get_users_in_circle(self, circle_name_: str, err=False):
        sql_req = f"""
            SELECT * FROM Users u
            WHERE u.id IN (
                SELECT id FROM SHIT
            )
            """
        try:
            res = self.cur.execute(sql_req)
            return res
        except Exception as e:
            if err:
                return e
            return None

    def new_user(self, name_: str, login_:str, password_: str, class_: int, letter_: str):
        val1 = ""
        val2 = ""

        sql_req = f"""INSERT INTO Users (
            name, login, password, class, letter
        ) VALUES (
            '{name_}', '{login_}', '{password_}', {class_}, '{letter_}'
        )"""

        self.cur.execute(sql_req)
        self.con.commit()

    def new_admin(self, name_: str, login_:str, password_: str):
        sql_req = f"""INSERT INTO Users (
            name, login, password
        ) VALUES (
            '{name_}', '{login_}', '{password_}'
        )"""

        self.cur.execute(sql_req)
        self.con.commit()

    def check_user(self, login_: str, password_: str):
        sql_req = f"""SELECT * FROM Users
        WHERE login == '{login_}' and password == '{password_}'
        """
        res = self.cur.execute(sql_req).fetchall()
        if res:
            return True
        else:
            return False

    def check_admin(self, login_: str, password_: str):
        sql_req = f"""SELECT * FROM Admins
        WHERE login == '{login_}' and password == '{password_}'
        """
        res = self.cur.execute(sql_req).fetchall()
        if res:
            return True
        else:
            return False

    def update_user(self, data, err=False):
        val1 = ""
        val2 = ""

        for column in ["name", "login", "password", "letter"]:
            if "tg_id" in data:
                old, new = data["tg_id"]
                if old:
                    val1 += f"tg_id='{old}',"
                if new:
                    val2 += f"tg_id='{new}',"
        for column in ["tg_id", "class"]:
            if "tg_id" in data:
                old, new = data["tg_id"]
                if old:
                    val1 += f"tg_id={old},"
                if new:
                    val2 += f"tg_id={new},"

        if not val1 or not val2:
            return False

        sql_req = f""""
        UPDATE Users
        SET {val2}
        WHERE {val1}
        """

        try:
            self.cur.execute(sql_req)
            self.con.commit()
            return True
        except Exception as e:
            if err:
                return e
            return False

    def update_admins(self, data, err=False):
        val1 = ""
        val2 = ""

        for column in ["name", "password", "letter"]:
            if column in data:
                old, new = data[column]
                if old:
                    val1 += f"{column}='{old}',"
                if new:
                    val2 += f"{column}='{new}',"
        for column in ["class"]:
            if column in data:
                old, new = data[column]
                if old:
                    val1 += f"{column}={old},"
                if new:
                    val2 += f"{column}={new},"

        if not val1 or not val2:
            return False

        sql_req = f""""
        UPDATE Users
        SET {val2}
        WHERE {val1}
        """

        try:
            self.cur.execute(sql_req)
            self.con.commit()
            return True
        except Exception as e:
            if err:
                return e
            return False


class User:
    def __init__(self):
        self.Logged = False
        self.Log_Btn = False
        self.Reg_Btn = False
        self.Name = None
        self.Login = None
        self.Password = None
        self.Status = None
        self.StartMessageId = ""




Message_Help = (

)

Message_Command_User = (
    f"Вот ваши доступные команды\n"
    "Записаться на кружок\n"
    "Где состою\n"
    "Уйти с кружка\n"
)


if __name__ == "__,ain__":
    db_debugger = DataBaseDebugging()
    print(db_debugger.get_users())
