## Spy Pixel Finder

This Python script will find spy pixels (aka tracking pixels) in your emails. To use this script, you have to export the
emails you want to scan to `.eml` files and place them in the `emails` subdirectory. The script will generate a
`results.csv` file that you can use for analysis of all 1x1 pixels the script has found in the provided emails.

Say [No to Spy Pixels](https://notospypixels.com/).

### Example Output

The output in the `results.csv` file should look something like this:

```csv
,src,sender,filename,attributes
1,http://ad.doubleclick.net/activity;...;sz=1x1;ord=1?,"""Adobe Systems"" <mail@info.adobesystems.com>","emails/test.eml","{""src"": ""http://ad.doubleclick.net/activity;...;sz=1x1;ord=1?"", ""width"": ""1"", ""height"": ""1"", ""border"": ""0"", ""alt"": """"}"
...
```

#### Columns

* `src` – Source URL of the 1x1 image.
* `sender` – Value of the `From` email header. This does not necessarily have to be correct since this header is
  manipulable.
* `filename` – Path of the `.eml` file that contained the image.
* `attributes` – JSON-encoded dictionary of all HTML attributes along with their values on the `img` tag.

### Installation

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
cd /path/to/emails && cp * /path/to/spy-pixel-finder/

# Execute the script, this may take a while
python main.py

# See which spy pixels the script has identified
less results.csv
```

### License

This script is licenced under the [MIT license](./LICENSE).
