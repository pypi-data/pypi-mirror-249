# Development

## Installing symbols

Use the following command to install symbols for `PyGObject`:

```bash
python3 -m pip install pygobject-stubs --upgrade --force-reinstall --no-cache-dir --config-settings=config=Gtk3,Gdk3,Soup2
```

## VSCode autocompletion

You need to select the venv where you installed the `pygobject-stubs`.

1. Press `F1`
2. Select `Python: Select interpreter`
3. Browse to your venv `bin` folder and select the `python` binary