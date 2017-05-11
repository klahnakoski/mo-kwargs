
More KWARGS!
============

Motivation
----------

Extensive use of dependency injection, plus managing the configuration for each of the components being injected, can result in some spectacularly complex system configuration. One way to reduce the complexity is to use configuration templates that contain useful defaults, and simply overwrite the properties that need to be changed for the new configuration. `@override` has been created to provide this templating system for Python function calls (primarily class constructors).  

`@override` will decorate a function to accept a `kwargs` parameter which is just like `**kwargs`, but the call parameters will override the properties in `kwargs`, rather than raise duplicate key exceptions.

**Example**

We decorate the `login()` function with `@override`. In this case, `username` is a required parameter, and `password` will default to `None`. The kwargs parameter should always default to `None` so that it's not required.

		@override
		def login(username, password=None, kwargs=None):
			pass

Define some `dicts` for use with our `kwargs` parameter:

		creds = {"userame": "ekyle", "password": "password123"}
		alt_creds = {"username": "klahnakoski"}


The simplest case is when we use kwargs with no overrides

		login(kwargs=creds)
		# SAME AS
		login(**creds)
		# SAME AS
		login(username="ekyle", password="password123")

You may override any property in kwargs: In this case it is `password`

		login(password="123", kwargs=creds)
		# SAME AS
		login(username="ekyle", password="123")

There is no problem with overriding everything in `kwargs`:

		login(username="klahnakoski", password="asd213", kwargs=creds)
		# SAME AS
		login(username="klahnakoski", password="asd213")

You may continue to use `**kwargs`; which provides a way to overlay one parameter template (`creds`) with another (`alt_creds`)

		login(kwargs=creds, **alt_creds)
		# SAME AS
		login(username="klahnakoski", password="password123")



