from mobio.libs.olap import SingletonArgs
from sqlalchemy import create_engine
from threading import Thread
from time import sleep
from sqlalchemy import text
from sqlalchemy.dialects import registry
import re

registry.register("mobio", "mobio.libs.olap.mining_warehouse.dialect", "MobioDialect")


class EngineRole:
    LEADER = "LEADER"
    FOLLOWER = "FOLLOWER"


class Engines(metaclass=SingletonArgs):
    # ENGINE config
    ENGINE_ECHO: bool = False
    ENGINE_FUTURE: bool = True

    # ENGINE parameters
    ROLE = "role"
    ENGINE = "engine"
    ALIVE = "alive"

    # FUNCTION parameters
    POOL_NAME = None
    USER_NAME = None
    PASS_WORD = None
    DATABASE = None
    QUERY = None

    dict_shards = {}

    def __init_shard__(self, role, alive, host: str, port: str):
        return {
            self.ROLE: role,
            self.ALIVE: alive,
            self.ENGINE: create_engine(
                self.build_query(host=host, port=int(port)),
                echo=self.ENGINE_ECHO,
                # future=self.ENGINE_FUTURE,
            ),
        }

    def build_query(self, host: str, port: int):
        return f"{self.POOL_NAME}://{self.USER_NAME}:{self.PASS_WORD}@{host}:{port}/{self.DATABASE}?{self.QUERY if self.QUERY else ''}"

    def __init__(self, uri):
        pattern = re.compile(
            r"""(?P<name>[\w\+]+)://
                        (?:
                            (?P<username>[^:/]*)
                            (?::(?P<password>[^@]*))?
                        @)?
                        (?P<host_port>[^/]*)?
                        (?:/(?P<database>[^\?]*))?
                        (?:\?(?P<query>.*))?""",
            re.X,
        )

        m = pattern.match(uri)
        if m is not None:
            components = m.groupdict()
            self.POOL_NAME = components.get("name")
            self.USER_NAME = components.get("username")
            self.PASS_WORD = components.get("password")
            self.DATABASE = components.get("database")
            self.QUERY = components.get("query")
            for host in components["host_port"].split(","):
                host, port = host.split(":")
                self.dict_shards[host] = self.__init_shard__(
                    role=None, alive=None, host=host, port=port
                )
                t = Thread(target=self.__health_check__)
                t.daemon = True
                t.start()
        else:
            raise Exception("Could not parse URL from string '%s'" % uri)

    def __health_check__(self):
        while True:
            lst_host = []
            for key in list(self.dict_shards):
                value = self.dict_shards.get(key)
                if value:
                    engine = value.get(self.ENGINE)
                    alive = value.get(self.ALIVE)
                    if alive is True or alive is None:
                        try:
                            with engine.connect() as connection:
                                results = connection.execute(text("show frontends"))
                                for result in results:
                                    result_host = result[1]
                                    lst_host.append(result_host)
                                    result_query_port = result[4]
                                    result_role = result[6]
                                    result_alive = result[9]
                                    if result_host not in self.dict_shards:
                                        self.dict_shards[
                                            result_host
                                        ] = self.__init_shard__(
                                            role=result_role,
                                            alive=result_alive,
                                            host=result_host,
                                            port=result_query_port,
                                        )
                                    else:
                                        self.dict_shards[result_host][
                                            self.ROLE
                                        ] = result_role
                                        self.dict_shards[result_host][self.ALIVE] = (
                                            True if result_alive == "true" else False
                                        )
                            break
                        except Exception as ex:
                            print("exec on host: {} ERROR:  {}".format(key, ex))
                else:
                    print("engine value is null")
            for i in list(self.dict_shards):
                if i not in lst_host:
                    self.dict_shards.pop(i)
                    print("host: {} not exists in database".format(i))
            sleep(5)
