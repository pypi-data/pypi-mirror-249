__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"

from collections import UserDict
import os
from decouple import config as dcfg
import json
import redis
import yaml
from clickhouse_connect.driver import Client as CHClient
from urllib.parse import urlparse
import logging
import uuid
import pulsar
from itertools import islice
import oss2
from questdb.ingress import Sender, IngressError, TimestampNanos, TimestampMicros
import pymongo
import clickhouse_connect
from elasticsearch import Elasticsearch
from datetime import datetime
import shutil
import threading
import socket
import platform
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import json
import struct
import traceback
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s')


def get_package_path(cfg: dict, package_id: str):
    plant = cfg['plant']
    module = cfg['module']

    return f"dist/{plant}-{module}-{package_id}.zip"


class JunoConfig(UserDict):
    lock = threading.Lock()
    header = b"jpcfg"

    def __init__(self):
        super(JunoConfig, self).__init__()
        self.data = {}
        self.run_env = "dev"

        if "package_id" not in self.data:
            if os.path.exists('project.yml'):
                with open('project.yml', 'r', encoding='utf-8') as f:
                    self.data.update(yaml.safe_load(f))

        if os.path.exists('project-ext.yml'):
            with open('project-ext.yml', 'r', encoding='utf-8') as f:
                ext = yaml.safe_load(f)
                if ext and len(ext) > 0:
                    self.data.update()

        #
        try:
            jf = Path.home() / ".juno" / "config.yaml"
            if os.path.exists(jf):
                with open(jf, 'r', encoding='utf-8') as f:
                    jc = yaml.safe_load(f)
                    self.data["cloud"] = jc
            else:
                self.data["cloud"] = {
                    "api": "http://192.168.101.157:8823/api"}
        except:
            pass

        if "redis" not in self.data:
            self.data["redis"] = {
                "host": "192.168.101.157",
                "port": 6379,
                "password": "myredis"
            }

        if "pulsar" not in self.data:
            self.data["pulsar"] = {
                "url": "pulsar://192.168.101.157:6650"
            }

        if "router_addr" not in self.data:
            self.data["router_addr"] = "tcp://192.168.101.157:2302"

        try:
            if "instance_id" not in self.data:
                if dcfg("instance_id", ""):
                    self.data["instance_id"] = dcfg("instance_id")
                else:
                    self.data["instance_id"] = self.data['plant'] + \
                        '-' + self.data['module'] + '.' + uuid.uuid4().hex + \
                        '.' + datetime.now().strftime("%Y%m%d%H%M%S") + ".dev"

            # set run_env
            if "run_env" in self.data:
                self.run_env = self.data["run_env"]
            else:
                if self.data["instance_id"].endswith(".dev"):
                    self.data["run_env"] = "dev"
                    self.run_env = "dev"
                elif self.data["instance_id"].endswith(".test"):
                    self.data["run_env"] = "test"
                    self.run_env = "test"
                else:
                    self.data["run_env"] = "prod"
                    self.run_env = "prod"

        except Exception as e:
            logging.debug(
                f"{str(e)}: maybe you are not using junocli under project folder")

        if "input_cfg" not in self.data:
            try:
                content = None
                with JunoConfig.lock:
                    with open('input.json', 'rb') as f:
                        content = f.read()
                self.data["input_cfg"] = json.loads(content)
            except Exception as e:
                pass

        self.data["algo_cfg"] = {}
        try:
            self.data["algo_cfg"] = JunoConfig.read_algo_config()
        except:
            pass

        if dcfg("cloud_api", ""):
            if "cloud" in self.data:
                self.data["cloud"]["api"] = dcfg("cloud_api")
            else:
                self.data["cloud"] = {"api": dcfg("cloud_api")}

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            pass

        raise KeyError(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def save_algo_config(self, config: dict):
        logging.info("save_algo_config")
        if self.run_env == "dev":
            with JunoConfig.lock:
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False)
                    f.flush()
        else:
            JunoConfig._save_algo_config_encrypt(config)

    def save_project_yml(self):
        with JunoConfig.lock:
            with open('project.yml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.data, f)

    @staticmethod
    def read_algo_config():
        content = None
        with JunoConfig.lock:
            with open("config.json", "rb") as f:
                content = f.read()

        lh = len(JunoConfig.header)
        if content[:lh] == JunoConfig.header:
            siz = struct.unpack("H", content[lh: (lh + 2)])[0]
            lh += 2
            key = content[lh: (lh + siz)]
            lh += siz
            siz = struct.unpack("I", content[lh: (lh + 4)])[0]
            lh += 4
            text = content[lh:]
            if len(text) != siz:
                print(f"invalid config len: {len(text)}, {siz}")
            content = JunoConfig.decrypt(text, key)

        return json.loads(content)

    @staticmethod
    def _save_algo_config_encrypt(config: dict):
        key = get_random_bytes(16)  # Generate a random 16-byte (128-bit) key
        print("key: ", key)
        pass_siz = struct.pack("H", 16)
        raw = json.dumps(config, ensure_ascii=False)
        encryed = JunoConfig.encrypt(raw, key)
        text_siz = struct.pack("I", len(encryed))

        with JunoConfig.lock:
            with open("config.json", "wb") as f:
                f.write(JunoConfig.header)
                f.write(pass_siz)
                f.write(key)
                f.write(text_siz)
                f.write(encryed)
                f.flush()

    @staticmethod
    def encrypt(plaintext, key):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")

        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        return cipher.iv + ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        iv = ciphertext[: AES.block_size]
        ciphertext = ciphertext[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext


junoconfig = JunoConfig()


def redis_cli(host: str, port: int, password: str, db: int = 0, socket_timeout=3):
    logging.debug(f"local redis: {host}:{port} {db} {password}")
    opts = None
    if platform.system().lower() == "linux":
        opts = {
            socket.TCP_KEEPIDLE: 120,
            socket.TCP_KEEPINTVL: 30,
            socket.TCP_KEEPCNT: 2
        }
    pool = redis.ConnectionPool(host=host, port=port, db=db,
                                password=password,
                                socket_timeout=11,
                                socket_keepalive=True,
                                retry_on_timeout=True,
                                max_connections=20,
                                socket_keepalive_options=opts)

    return redis.Redis(connection_pool=pool)


def pulsar_cli(url: str, shared: bool = False, ca: str = "certs/ca.cert.pem",
               cert: str = "certs/client.cert.pem", key: str = "certs/client.key-pk8.pem"):
    client: pulsar.Client
    if 'ssl' in url:
        auth = pulsar.AuthenticationTLS(cert, key)
        client = pulsar.Client(url,
                               tls_trust_certs_file_path=ca,
                               tls_allow_insecure_connection=False,
                               authentication=auth)
    else:
        client = pulsar.Client(url)

    return client


def es_cli(url: str, ca: str, user: str, password: str):
    # cfg['elastic']['url'], ca_certs=cfg['elastic']['ca'],
    # basic_auth=(cfg['elastic']['user'], cfg['elastic']['password'])
    return Elasticsearch(url, ca_certs=ca, basic_auth=(user, password))


def clickhouse_cli(url: str):
    p = urlparse(url)
    schema = p.scheme
    if schema != 'ch':
        raise Exception(f'invalid schema in dbs.clickhouse.url: {url}')
    user = p.username
    password = p.password
    host = p.hostname
    port = p.port
    return clickhouse_connect.get_client(host=host, username=user,
                                         password=password, port=port)

# auth = ("pulsar", "KA6oqjb0s5OP49WHfKLabO8ef42ArV_9q9NznHNKUJ8", "_lTCuKKqtRWVDyb9d5545s99VwXVkJjs-HhCtPxPaTQ", "afh08JDKKYUxPYuHCWsytHQ7LgUZ63s-CTvTFaWFVE4")


def qdb_cli(host: str, port: str, auth: str, tls: bool, auto_flush: bool, **kwargs):
    auth_t = tuple(auth.split(' '))
    s = Sender(host, port, auth=auth_t, tls=tls, auto_flush=auto_flush)
    s.connect()
    return s


def mongo_cli(url: str):
    return pymongo.MongoClient(url)


def oss_cli(key: str, sec: str, endpoint: str, bucket: str):
    auth = oss2.Auth(key, sec)
    endpoint = endpoint
    r = oss2.Bucket(auth, endpoint, bucket, connect_timeout=5)
    # for b in islice(oss2.ObjectIterator(r), 10):
    #     print(b.key)
    return r
