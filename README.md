# Spy Pixel Finder

This Python script will find spy pixels (aka tracking pixels) in your emails. To use this script, you have to export the
emails you want to scan to `.eml` files and place them in the `emails` subdirectory. The script will generate a
`results.csv` file that you can use for analysis of all 1x1 pixels the script has found in the provided emails.

Say [No to Spy Pixels](https://notospypixels.com/).

## Example Output

The output in the `results.csv` file should look something like this:

```csv
,src,domain,sender,filename,attributes
1,ad.doubleclick.net,http://ad.doubleclick.net/activity;...;sz=1x1;ord=1?,"""Adobe Systems"" <mail@info.adobesystems.com>","emails/test.eml","{""src"": ""http://ad.doubleclick.net/activity;...;sz=1x1;ord=1?"", ""width"": ""1"", ""height"": ""1"", ""border"": ""0"", ""alt"": """"}"
...
```

### What Do These Columns Mean?

* `src` – Source URL of the 1x1 image.
* `domain` – Extracted domain of the image URL.
* `sender` – Value of the `From` email header. This does not necessarily have to be correct since this header is
  manipulable.
* `filename` – Path of the `.eml` file that contained the image.
* `attributes` – JSON-encoded dictionary of all HTML attributes along with their values on the `img` tag.

## Prerequisites

You need Python 3 installed, optionally with the virtual environment extension. Other than that, the script should be
able to run everywhere.

## Installation

Follow these instructions to run this script on your machine:

```sh
# Clone the repository
git clone https://github.com/martbock/spy-pixel-finder.git
cd spy-pixel-finder/

# Create a Python3 virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the necessary libraries
pip install -r requirements.txt

# Copy your emails into the correct directory
cd /path/to/emails && cp * /path/to/spy-pixel-finder/emails/

# Execute the script, this may take a while
python main.py

# See which spy pixels the script has identified
less results.csv
```

## Console Arguments

The script provides multiple options what to filter out when creating the `results.csv` file.
Please see the `--help` output of the script for details:

```sh
$ python3 main.py -h
usage: main.py [-h] [--no-drop-src-duplicates] [-d] [--remove-subdomains]

Find spy pixels in your emails.

optional arguments:
  -h, --help            show this help message and exit
  --no-drop-src-duplicates
                        Don't drop rows that have the same image source URL. Defaults to false.
  -d, --drop-domain-duplicates
                        Drop rows that have a duplicate domain of the image URL. Defaults to false.
  --remove-subdomains   Remove subdomains of image URLs. This way you can get rid of customer subdomains. Defaults to false.
```

## Inspiration

Thank you to [@dhh](https://github.com/dhh) and the [Basecamp team](https://github.com/basecamp) for bringing attention
to this issue. Also, thanks to [@apparition47](https://github.com/apparition47) for developing the Apple Mail
extension [MailTrackerBlocker](https://github.com/apparition47/MailTrackerBlocker) that blocks spy pixels.

## License

This script is licenced under the [MIT license](./LICENSE).
