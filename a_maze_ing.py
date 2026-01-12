from srcs.config.parser import ConfigParser

if (__name__ == "__main__"):
    try:
        parser = ConfigParser("config.txt")
    except Exception as e:
        print(e)
    config = parser.extract()
    print(config)
