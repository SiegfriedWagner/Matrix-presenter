# Requirements
1. Python 3 installed od system. [Tutorial can be found here](https://www.youtube.com/watch?v=yNLw5G1Y65o)
2. (On Windows system) K-Lite codecs pack [Can be downloaded from here](https://www.codecguide.com/download_kl.htm)
# Instalation
 - (On Windows system) After installing all required software to install experiment software execute install.bat
# Execution
- (On Windows system) To run experiment software execute run.bat.
# Resources
To execute properly application needs both videos in `Resources/videos` and matrices in `Resources/images`.
# New language text files
To create new task description follow instruction:
1. Create new file with that follow pattern **\[name\].py** in directory `Resources/text`
2. Fill file with text. File must contain 7 variables which are [python character strings](https://docs.python.org/3.9/library/string.html):
- `introduction` - text showed just after the experiment begins.
- `description` - experiment description. In description you can use `{duration_of_matrices:.0f}` which will show how long panel with matrices will be presented before timeout.
- `example` - text preceding experiment tutorial.
- `correct` - text shown after correct answer in tutorial.
- `incorrect` - text shown after inccorect answer in tutorial.
- `end_of_tutorial` - text shown just after tutorial.
- `close` - text shown after last experiment task.

Hint: Python string character strings sarts and ends with **single or triple** quotation marks. If you use triple quotation marks text in application will keep same structure as in text file.

3. After application restart new language should be enabled as option in dropdown menu.