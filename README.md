# NotThatUselessProjectReport

The idea of this plugin is generate a text file with some info about the current open folder or project. By some info I mean the total of files the folder has, the types of files and how much lines of code each type have. It doesn't read binary files, they are totally ignored by the plugin.

I know it is not the most useful information you can have about your project, but I is something cool to know. At least I think it is cool.

I hope you you find this plugin helpful.

### Installation

You can install via [**Sublime Package Control**](http://wbond.net/sublime_packages/package_control) plugin.
Just open "Package Control: Install Package" in your Command Palette and search for "Not That Useless Project Report".


For **manual installation**, run the following script in the Sublime Text terminal ```(ctrl+`)``` which utilizes ```git clone```.

```python
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/pererinha/NotThatUselessProjectReport', 'NotThatUselessProjectReport'], 'working_dir': path})
```


**It is currently working just for Sublime 3**

### Usage
* On Mac **Command + Shift + U**
* On Windows or Linux **Ctrl + Shift + U**

Or 

**Ctrl + Shift + P** and search for *“Generate a not useless report about your project”*


### Example of a report
This is the report of this project

```
Project report
==============

Summary
-------
|--------------------|--------------------|--------------------|--------------------|
| Type               | Files              | Lines              | Blank lines        |
|--------------------|--------------------|--------------------|--------------------|
| JSON               | 1                  | 4                  | 0                  |
| PY                 | 4                  | 279                | 52                 |
| SUBLIME-COMMANDS   | 1                  | 6                  | 0                  |
| SUBLIME-KEYMAP     | 3                  | 9                  | 0                  |
| TXT                | 2                  | 11                 | 4                  |
|--------------------|--------------------|--------------------|--------------------|

Totals
------
|--------------------|--------------------|--------------------|--------------------|
| Types              | Files              | Lines              | Blank lines        |
|--------------------|--------------------|--------------------|--------------------|
| 5                  | 11                 | 309                | 56                 |
|--------------------|--------------------|--------------------|--------------------|
```

How cool is that??

### Thanks

Special thanks to [@joshearl](https://github.com/joshearl) for his awesome book [Writing Sublime Plugins](https://leanpub.com/writing-sublime-plugins) and to [Audrey Roy](https://github.com/audreyr) for [binaryornot](https://github.com/audreyr/binaryornot), it saved me a lot of time.

