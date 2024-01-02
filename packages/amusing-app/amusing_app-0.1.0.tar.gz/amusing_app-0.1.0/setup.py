# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amusing', 'amusing.core', 'amusing.db', 'amusing.scripts', 'amusing.utils']

package_data = \
{'': ['*']}

install_requires = \
['brotli==1.1.0',
 'certifi==2023.11.17',
 'charset-normalizer==3.3.2',
 'click==8.1.7',
 'greenlet==3.0.3',
 'idna==3.6',
 'markdown-it-py==3.0.0',
 'mdurl==0.1.2',
 'mutagen==1.47.0',
 'numpy==1.26.2',
 'pandas==2.1.4',
 'pycryptodomex==3.19.1',
 'pygments==2.17.2',
 'python-dateutil==2.8.2',
 'pytz==2023.3.post1',
 'pyyaml==6.0.1',
 'requests==2.31.0',
 'rich==13.7.0',
 'six==1.16.0',
 'sqlalchemy==2.0.24',
 'typer==0.9.0',
 'typing-extensions==4.9.0',
 'tzdata==2023.3',
 'urllib3==2.1.0',
 'websockets==12.0',
 'yt-dlp==2023.11.16',
 'ytmusicapi==1.3.2']

entry_points = \
{'console_scripts': ['amusing = amusing.cli:app']}

setup_kwargs = {
    'name': 'amusing-app',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1> 🎧 Amusing 🎸 </h1>\n\nA CLI to help download music independently or from your exported apple music library.\n\n## Why should you use <strong>Amusing</strong>?\n\n- To download your entire Apple Music Library and store it locally in one go\n- To search and download individual songs from YouTube\n- To keep track of your ever growing music collection\n\n## 🛠️ Install it!\n\n```console\n$ pip install amusing\n```\n\n## ✨ Getting set up\n\nThere are three things to know before moving on to the next section:\n\n- The CLI takes in a `appconfig.yaml` file similar to what\'s indicated in `appconfig.example.yaml`. You can simply rename it.\n  The file looks like this:\n\n  ```yaml\n  root_download_path: "..."\n  db_name: "..."\n  ```\n\n- A dedicated sqlite database called `db_name` will be created in `root_download_path/db_name.db` to store two tables `Song` and `Album` as defined in `amusing/db/models.py`. All songs downloaded locally will be getting a row in the `Song` table and a row for their corresponding album in the `Album` table.\n- The songs are downloaded in `root_download_path/songs` directory.\n- That\'s it. You\'re done. Let\'s look at the commands available next.\n\n## 💬 Available commands\n\nThere are currently 6 commands available, excluding the `amusing --version`.\n\nThe first time you run a command (eg. --help), an `Amusing` directory will be created in your `pathlib.Path.home()/Downloads` folder. For eg., on MacOS, it\'s in `/Users/Username/Downloads`.\n\n```console\n$ amusing --help\n\n Created a new config file: /Users/username/Downloads/Amusing/appconfig.yaml\n\n Usage: amusing [OPTIONS] COMMAND [ARGS]...\n\n Amusing CLI to help download music independently or from your exported apple music library.\n\n╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --version  -v                                                                                                                                  │\n│ --help               Show this message and exit.                                                                                               │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ download           Parse the entire AM library and download songs and make/update the db as needed.                                            │\n│ showsimilar        Look up the db and show if similar/exact song(s) are found.                                                                 │\n│ showsimilaralbum   Look up the db and show albums similar to the album searched.                                                               │\n│ showsimilarartist  Look up the db and show songs for similar/exact artist searched.                                                            │\n│ song               Search and download the song and add it to the db. Use --force to overwrite the existing song in the db. Creates a new      │\n│                    album if not already present.                                                                                               │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n\n```\n\n### To parse an exported `Library.xml` file from your Apple Music account, use:\n\n```console\n$ amusing download --help\n\n Usage: amusing download [OPTIONS] [PATH]\n\n Parse the entire AM library and download songs and make/update the db as needed.\n\n╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│   path      [PATH]  The path to the Library.xml exported from Apple Music. [default: ./Library.xml]                                            │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --help          Show this message and exit.                                                                                                    │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n# Example\n$ amusing download "your/path/to/Library.xml"\n\n```\n\n### To download a song individually, use:\n\n```console\n$ amusing song --help\n\n Usage: amusing song [OPTIONS] NAME ARTIST ALBUM\n\n Search and download the song and add it to the db. Use --force to overwrite the existing song in the db. Creates a new album if not already\n present.\n\n╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ *    name        TEXT  Name of the song. [default: None] [required]                                                                            │\n│ *    artist      TEXT  Aritst of the song. [default: None] [required]                                                                          │\n│ *    album       TEXT  Album the song belongs to. [default: None] [required]                                                                   │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --force    --no-force      Overwrite the song if present. [default: no-force]                                                                  │\n│ --help                     Show this message and exit.                                                                                         │\n╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n\n# Example, the search keywords need not be exact of course:\n$ amusing song "Run" "One Republic" "Human"\n\n```\n\n### Search for a similar song, album or artist in your db/downloads:\n\n```console\n$ amusing showsimilar "Someday"\n\nSong to look up:  someday\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Song                 ┃ Artist        ┃ Album                                ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ Someday              │ OneRepublic   │ Human (Deluxe)                       │\n│ Someday At Christmas │ Justin Bieber │ Under the Mistletoe (Deluxe Edition) │\n└──────────────────────┴───────────────┴──────────────────────────────────────┘\n\n\n$ amusing showsimilarartist "OneRepublic"\n\nArtist to look up:  OneRepublic\n┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Song            ┃ Artist      ┃ Album                                             ┃\n┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ Run             │ OneRepublic │ Human (Deluxe)                                    │\n│ Someday         │ OneRepublic │ Human (Deluxe)                                    │\n│ No Vacancy      │ OneRepublic │ No Vacancy - Single                               │\n│ RUNAWAY         │ OneRepublic │ RUNAWAY - Single                                  │\n│ Sunshine        │ OneRepublic │ Sunshine - Single                                 │\n│ I Ain\'t Worried │ OneRepublic │ Top Gun: Maverick (Music from the Motion Picture) │\n│ West Coast      │ OneRepublic │ West Coast - Single                               │\n└─────────────────┴─────────────┴───────────────────────────────────────────────────┘\n\n$ amusing showsimilaralbum "Human"\n\nAlbum to look up:  Human\n┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓\n┃ Album          ┃ Number of songs ┃\n┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩\n│ Human (Deluxe) │ 2               │\n└────────────────┴─────────────────┘\n\n```\n\n## TODO 📝\n\n1. Provide an option to choose which searched result is downloaded.\n2. Provide a command to show all songs in an album\n',
    'author': 'Yash Prakash',
    'author_email': 'yashprakash13@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
