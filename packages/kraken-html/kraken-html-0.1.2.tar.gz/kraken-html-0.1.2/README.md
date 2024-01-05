
# kraken_html
<definition>


## How to use

```
from kraken_html import kraken_html as m



```


## Records
Converts a record into a HTML record, where url are transformed as a links for example

### HTML record format
```
from kraken_html import kraken_html as m

record = {...}
html_record = m.html_record.html_record(record)

```

### HTML record list
```
from kraken_html import kraken_html as m

records = [{...}, {...}]
records_list = m.html_record.to_list(records)
```

### HTML record form
```
from kraken_html import kraken_html as m

record = {...}
record_form = m.html_record.to_json(record)

```

## Pages
Pages are full website pages that includes navigation, heaters and footers. 

```
from kraken_html import kraken_html as m

page_content = 'some content...'
webpage = m.pages.blank(page_content)

```


## Sections
Sections are components of pages, building blocks to build full pages

### Hero
Image with key benefit 
```
record = {
    "headline": "Headline 1",
    "text": "Some text"
}

theme = 'dark'
page_content = m.section.hero(record, theme)
webpage = m.pages.blank(page_content)
```


    