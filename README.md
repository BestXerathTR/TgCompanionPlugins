# tg_userbot_plugins

Plugin Repository for [TelegramCompanion](https://github.com/nitanmarcel/TelegramCompanion).

Before making any pull request or creating a plugin on your repo read this carefully.

This is a beta feature so is not fully stable. Also I'm not taking any responsabilites for what plugin you install unless they are installed from this official repository.


All plugins need to be in they own folder with a proper name that doesn't contains any spaces or RTL characters.

Inside the plugin folder there should be two files:

`pluginname.py` - The module that has to be installed in the companion for the new added features to work.

`pluginname.plugin` - The file that contains the module name, author any any required requirements.

To use a new config value in your module you don't have nothing else to do rather than loading them into your script.

```
import os

CONFIG_VALUE = os.environ.get("CONFIG_VALUE", "DEFAULT_VALUE")

```

**Example of pluginname.plugin:**

```

Module = getinstalledplugins
Name = Get Installed Plugins
Description = Use .plugins to  list all the installed plugins or .plugin name to get the info for a specific plugin
Author = Nitan Alexandru Marcel
Version = 1.0
Requirements = telethon
```
