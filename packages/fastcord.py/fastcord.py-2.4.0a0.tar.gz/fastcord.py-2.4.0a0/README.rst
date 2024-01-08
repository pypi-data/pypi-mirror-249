fastcord.py
==========

.. image:: https://img.shields.io/pypi/v/fastcord.py.svg
   :target: https://pypi.python.org/pypi/fastcord.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/fastcord.py.svg
   :target: https://pypi.python.org/pypi/fastcord.py
   :alt: PyPI supported Python versions

A modern, easy to use, feature-rich, and async ready API wrapper for fastcord written in Python.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U fastcord.py

    # Windows
    py -3 -m pip install -U fastcord.py

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "fastcord.py[voice]"

    # Windows
    py -3 -m pip install -U fastcord.py[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Rappytz/fastcord.py
    $ cd fastcord.py
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that when installing voice support on Linux, you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.8-dev`` for Python 3.8)

Quick Example
--------------

.. code:: py

    import fastcord

    class MyClient(fastcord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    intents = fastcord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run('token')

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import fastcord
    from fastcord.ext import commands

    intents = fastcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='>', intents=intents)

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token')

You can find more examples in the examples directory.

Links
------

- `Documentation <https://fastcordpy.readthedocs.io/en/latest/index.html>`_
- `discord API <https://discord.gg/discord-api>`_
