
# kraken_boilerplate
Library of commonly used templates

Templates are stored at https://github.com/tactik8/boilerplates


## How to use

```
from kraken_boilerplate import kraken_boilerplate as k

# Get content from privacy template
content = k.get('privacy', record, 'EN-US')

# Get record template for a specific template
record = k.get_record('privacy')

# Get list of all files
record = k.get_files()

# Refresh templates from github
k.refresh()

```


    
    