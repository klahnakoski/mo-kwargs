from mo_logs import logger

from mo_kwargs import override


@override(kwargs="config")
def test_function(config=None):
    config.config = None
    logger.note("values {{config}}", config=config)


if __name__ == "__main__":
    test_function(a=1, b=2, c=3)
