## Usage

```shell
# Establish a venv, probably
$ python3 -m venv venv
$ source venv/bin/activate

# Install FontTools in your venv
$ pip install fonttools

# Add a BASE table
$ python add_base.py myfont.ttf

# Inspect it
$ ttx -o - -t BASE myfont.ttf
```