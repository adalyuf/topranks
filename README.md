# TopRanks.ai

To get container up and running:

```
git clone https://github.com/adalyuf/topranks.git
```

```
cd topranks
code .
```

Ask the author for the .env file with secrets and add this into the main (topranks) directory.

In VSCode press `F1` and `Rebuild and reopen in container`

The startup.sh script should run and will set up css/js files with npm and install packages with pip.

After this runs, start the server with `python manage.py runserver`
