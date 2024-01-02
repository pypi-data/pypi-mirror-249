# dub.py

A wrapper built around the [dub.co API](https://dub.co/docs/api-reference/introduction) written in python.

## Installation
```
$ pip install dub.py
```

## Usage
```py
import dub

dub.api_key = "API_KEY_HERE"

tag = dub.Tag(slug="project")
tag.create(name="tag_name")
```