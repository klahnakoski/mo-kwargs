from mo_kwargs import override


@override(kwargs="config")
def test_function(config=None):
    config.config = None
    print(config)


if __name__ == "__main__":
    test_function(a=1, b=2, c=3)
