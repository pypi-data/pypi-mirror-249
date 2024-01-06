import os, yaml, logging


# 读取yaml
def read_yaml(key: str, filename: str):
    """
    读取yaml配置文件
    :param key:     string      要读取的值的名称
    :param filename: string     配置文件的名字
    :return         *           要读取的值
    """
    if not os.path.exists(os.getcwd() + '/config/' + filename + '.yaml'):
        logging.error(f"config目录下没有{filename}.yaml文件，请添加文件！！！")
        raise SystemExit(0)
    try:
        with open(os.getcwd() + '/config/' + filename + '.yaml', encoding="utf-8") as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[key]
    except:
        logging.error(f"{filename}.yaml文件中没有{key}配置，请检查配置文件！！！")
        raise SystemExit(0)


# 追加写入yaml
def write_yaml(data: str, filename: str):
    """
    写入yaml配置
    :param data:        json格式
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="a") as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# 写入yaml
def write_yaml_value(data: str, filename: str):
    """
    写入yaml配置
    :param data:        json格式
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="w") as f:
        yaml.safe_dump(data=data, stream=f, allow_unicode=True)


# 清空yaml
def clear_yaml(filename: str):
    """
    清空yaml
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="w") as f:
        f.truncate()


# 读取全部yaml配置
def read_all_yaml(filename: str):
    """
    读取全部yaml配置
    :param filename:    配置文件的名字
    :return:            全部配置
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8") as f:
        value: object = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value
