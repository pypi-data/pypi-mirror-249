"""

\t\t\t\t  
بسم الله الرحمن الرحيم
=
\t\n
Pamylka python package\n
Created by Ahmed Elbehairy
Created at 13/3/1445 Higri


"""
__creator__ = "Ahmed Elbehairy"
__copyrights__ = "All copyrights reserved at pamylka.com"
__version__ = "00.04.13"

from re import compile
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from pyodbc import Connection, connect
from arabic_reshaper import reshape
from os import path, listdir, system
from datetime import datetime
from traceback import print_exc
from time import sleep
from pygame import mixer, time
from platform import node
from getpass import getuser


DOMAIN = "pamylka.com/"
H = "https://"
SUBDOMAINS = ["shop."]
SHOPURL = H + SUBDOMAINS[0] + DOMAIN


class InApp:
    ...


class App:
    """The official applications class for any project Assigned to Pamylka\n
    Set by: Ahmed Elbehairy"""

    def __init__(
        self,
        name: str,
        version: str,
        type: str,
        date: str,
        creator: str = __creator__,
        app: str = "app",
        extension: str = "py",
        execute: bool = True,
        root: str = "../",
    ):
        """
        Parameters
        -
        :param str name: The name of the program or application you want to initialize
        :param str version: The version of the application at the moment which have to be edited manually
        :param str type: the type of the application, it usually means what this application do or what type of program is it is, is it a web scraper or a desktop application
        :param str date: The date when the program created
        :param str creator: The creator of the application
        :param str app: the app class of what you are

        Return
        -
        :return: an Application object
        :rtype: App
        """
        self.name = name
        self.version = version
        self.creator = creator
        self.type = type
        self.date = date
        self.app = app

        try:
            file_path = find(f"{self.name}.{extension}", root)

            if not file_path:
                return

            with open(file_path, "r", encoding="utf-8") as file:
                pattern = compile("[_ ]{0,2}?version[_ ]{0,2}?")
                file_lines = file.readlines()

                for i in range(len(file_lines)):
                    if pattern.search(file_lines[i]):
                        file_lines[i] = f'__version__ = "{self.version}"\n'

                        with open(file_path, "w", encoding="utf-8") as file:
                            file.writelines(file_lines)

                        break

                if not execute:
                    return
                with open(f"{file_path}pam", "w", encoding="utf-8") as executable:
                    executable.writelines(file_lines)
        except FileNotFoundError:
            return

    def __str__(self) -> str:
        """
        Prety printing the app
        """
        return f"\n\n{self.name} - version: {self.version} - Get from: {SHOPURL}{self.name.lower()}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class AlphaApp(App):
    def __init__(
        self,
        name: str,
        version: str,
        type: str,
        date: str,
        creator: str = __creator__,
        app: str = "app",
        extension: str = "py",
        execute: bool = True,
        root: str = "../",
    ):
        super().__init__(
            name, version, type, date, creator, app, extension, execute, root
        )
        self.Application = {
            "The Alpha app": {"Name": name, "Apptype": app, "App": self}
        }
        self.count = 1

    def include(self, app: InApp):
        self.Application[len(self.Application)] = {
            "Name": app.name,
            "Apptype": app.app,
            "App": app,
        }

    def printApplication(self) -> dict:
        """Prints the apps included in the application"""

        print("\n\nApplication includes:\n")
        for index in self.Application:
            print(
                f"::: {index} ::: ",
                f"Name: {self.Application[index]['Name']}",
                f"App: {self.Application[index]['Apptype']}\n",
                sep="\n",
            )

        return self.Application

    def printApps(self) -> None:
        """Prints the apps of the application but with the __str__ format"""

        for index in self.Application:
            input(f"Next >>>> {index}")
            print(self.Application[index]["App"])

    def __len__(self) -> int:
        return len(self.Application)


class BaseApp(AlphaApp):
    """The class for the big base application of the project"""

    def __init__(
        self,
        name: str,
        version: str,
        category: str,
        type: str,
        date: str,
        creator: str = __creator__,
        application_nu: int = 1,
        extension: str = "py",
        execute: bool = True,
        root: str = "../",
    ):
        super().__init__(
            name,
            version,
            type,
            date,
            creator,
            extension=extension,
            app="Base App",
            execute=execute,
            root=root,
        )
        """
        Parameters
        -
        :param int application_nu: Just to tell the class how many apps or files are in the project
        :param str category: Mostly indicates the field where the application is used
        
        Return
        -
        :return: The BaseApp object
        :rtype: BaseApp
        """
        self.count = application_nu
        self.category = category

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Get from: {SHOPURL}{self.name.lower()}\nCategory: {self.category}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class HeroApp(AlphaApp):
    """The class for the biggest Pamylka apps"""

    def __init__(
        self,
        name: str,
        version: str,
        category: str,
        type: str,
        date: str,
        creator: str = __creator__,
        application_nu: int = 1,
        extension: str = "py",
        execute: bool = True,
        root: str = "../",
    ):
        super().__init__(
            name,
            version,
            type,
            date,
            creator,
            extension=extension,
            app="Hero App",
            execute=execute,
            root=root,
        )
        """
        Parameters
        -
        :param int application_nu: Just to tell the class how many apps or files are in the project
        :param str category: Mostly indicates the field where the application is used
        
        Return
        -
        :return: The HeroApp object
        :rtype: BaseApp
        """
        self.count = application_nu
        self.category = category

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Get from: {H}{self.name.lower()}.{DOMAIN}\nCategory: {self.category}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class InApp(App):
    """The class for the apps included in the application"""

    def __init__(
        self,
        name: str,
        ver: str,
        date: str,
        use: str,
        base: BaseApp | HeroApp,
        creator: str = __creator__,
        extension: str = "py",
        execute: bool = True,
        root: str = "../",
    ):
        super().__init__(
            name,
            ver,
            type,
            date,
            creator,
            extension=extension,
            app="Inside App",
            execute=execute,
            root=root,
        )
        """
        Parameters
        -
        :param str use: The use of the mini application or file
        :param int num: What's the index of the application order
        :param str base: What's the parent of this application
        
        Return
        -
        :return: The InApp object
        :rtype: BaseApp
        """
        self.appUse = use
        self.base = base
        base.include(self)
        base.count += 1
        self.appnum = base.count

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Base app: {self.base.name}\nUsage: {self.appUse}\n\nCreated by: {self.creator} at {self.date}\n"


def db_connect(
    database: str,
    driver: str = "ODBC Driver 17 for SQL Server",
    server: str = node().upper(),
    trstconn: str = "yes",
) -> Connection:
    """
    Connect to database
    =
    """
    conn = connect(
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        f"Trusted_Connection={trstconn};"
    )

    crsr = conn.cursor()

    return conn, crsr


def crsrexec(prompt: str, crsr: Connection.cursor) -> None:
    """Execute the querty and commit it right after"""
    crsr.execute(prompt)
    crsr.commit()


def find(name: str, file_path: str = "../") -> str:
    """
    Find the file if it doesn't exist in the first directory
    """

    if path.exists(name):
        return name

    if path.exists(path.join(file_path, name)):
        return path.join(file_path, name)

    for file_ in listdir(file_path):
        file__ = path.join(file_path, file_)
        if path.isdir(file__):
            value = find(name, file__)
            if value:
                return value

        if file__.endswith(name):
            return file__

    return


def get_key(di: dict, val):
    for key, value in di.items():
        if val == value:
            return key


def aprint(string: str):
    for line in string.splitlines():
        for word in line.split()[::-1]:
            if word.isascii():
                print(word)
                continue
            print(reshape(word), end=" ")
        print()


def driver_setup(
    profile_dir: str = "Default",
    executable_path: str = "C:\Selenium\chromedriver-win64\chromedriver.exe",
    detach: bool = True,
    user_data_dir: str = r"C:\Users"
    + f"\{getuser()}"
    + r"\AppData\Local\Google\Chrome Dev\User Data",
    useragent: str = UserAgent().random,
):
    # OPTIONS SETUP
    options = Options()  # Defining options for the driver
    options.add_experimental_option(
        "detach", detach
    )  # Force the browser to stay open even after fininshing
    options.add_argument(
        f"--user-data-dir={user_data_dir}"
    )  # Inputing the user data path for the driver
    options.add_argument(
        f"--profile-directory={profile_dir}"
    )  # Specifing the profile directory
    options.add_argument(f"--user-agent={useragent}")

    # DRIVER SETUP
    driver = Chrome(
        service=Service(executable_path=executable_path), options=options
    )  # Specifing the driver with the chromedriver path
    driver.implicitly_wait(30)

    return driver


def check_results(show_func=lambda x: x):
    def above_layer(function):
        def wrapper(*args, **kwargs):
            while True:
                returned = function(*args, **kwargs)
                print(show_func(returned))
                match input("Are you happy with the results? y\\n\n").lower():
                    case "y":
                        return returned
                    case _:
                        continue

        return wrapper

    return above_layer


def err(
    number: int = 10,
    sleeping: int = 5,
    file_name: str = "err.log",
    exception: bool = True,
    scream_enable: bool = True,
    scream_path: str = find("scream.mp3", "../"),
    args_func=lambda x: x,
    kwargs_func=lambda x: x,
):
    def layer(function):
        def wrapper(*args, **kwargs):
            for i in range(number):
                try:
                    return function(*args, **kwargs)
                except SystemExit:
                    raise SystemExit
                except BaseException:
                    print_exc()
                    save_log(
                        f"""An error occured at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:\n\nfunction: {function.__name__}\nargs: {args_func(args)}\nkwargs: {kwargs_func(kwargs)}\n\n""",
                        file_name,
                        exception,
                    )
                    if i < number - 1:
                        print("Taking a break...")
                        sleep(sleeping)
                    continue

            if scream_enable:
                scream(scream_path)

        return wrapper

    return layer


def safe_ex(function):
    if not path.exists(".exit.pypam"):
        with open(".exit.pypam", "w") as file:
            file.write("""with open(".exit", 'w') as file:\n\tfile.write("exit")""")

    def wrapper(*args, **kwargs):
        while True:
            with open(".exit") as file:
                if "exit" in file.read():
                    open(".exit", "w").close()
                    exit()

            function(*args, **kwargs)

    return wrapper


def save_prog(
    file_name: str = "prog.log",
    args_func=lambda x: x,
    kwargs_func=lambda x: x,
    return_func=lambda x: x,
):
    def above_layer(function):
        def wrapper(*args, **kwargs):
            try:
                value = function(*args, **kwargs)
                save_log(
                    f"""At {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:\n\nfunction: {function.__name__}\nargs: {args_func(args)}\nkwargs: {kwargs_func(kwargs)}\n\nReturned value: {return_func(value)}""",
                    file_name,
                    False,
                )
                return value

            except BaseException as e:
                print_exc()
                for log in [file_name, "err.log"]:
                    save_log(
                        f"""An error occured at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:\n\nfunction: {function.__name__}\nargs: {args_func(args)}\nkwargs: {kwargs_func(kwargs)}\n\n""",
                        log,
                        True,
                    )

                raise e

        return wrapper

    return above_layer


def save_log(text: str, file_name: str = f"err.log", exception: bool = True):
    if not path.exists(file_name):
        m = "w"
    else:
        m = "a"

    with open(file_name, m, encoding="utf-8") as file:
        file.write(text)
        if exception:
            print_exc(file=file)
        file.write("\n\n\n")


def scream(scream_path: str = find("scream.mp3", "../"), waiting: int = 2800):
    mixer.init()
    tom_scream = mixer.Sound(scream_path)
    tom_scream.play()

    count = 0
    while mixer.get_busy() and count < waiting:
        time.delay(1)
        count += 1

    return


def get_file(
    file_name: str,
    content_func=lambda x: x.read(),
    encoding: str = "utf-8",
    mode: str = "r",
):
    with open(file_name, mode=mode, encoding=encoding) as file:
        return content_func(file)


def manual_edit(
    write_func=lambda x: x,
    file_name: str = "editable_msg.txt",
    application: str = "notepad.exe",
    encoding: str = "utf-8",
):
    def above_layer(function):
        def wrapper(*args, **kwargs):
            text = function(*args, **kwargs)

            while True:
                match input(
                    "Do you want to edit this or redo function? y\\n\\r\n"
                ).lower():
                    case "y":
                        break
                    case "n":
                        return text
                    case "r":
                        raise wrapper
                    case _:
                        continue

            with open(file_name, "w", encoding=encoding) as file:
                file.write(write_func(text))

            system(f"{application} {file_name}")

            input("Press enter...")

            with open(file_name, encoding=encoding) as file:
                return file.read()

        return wrapper

    return above_layer


def disable(returned_value = None):

    def above_layer(function):
        
        def wrapper(*args, **kwargs):
            return
        
        return wrapper
    

    return returned_value
class Restart(BaseException):
    ...
