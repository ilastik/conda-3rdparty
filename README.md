[![Anaconda-Server Badge](https://anaconda.org/ilastik-forge/conda-3rdparty/badges/version.svg)](https://anaconda.org/ilastik-forge/conda-3rdparty)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# conda 3rd party

Extract/summarize all licenses in an environment


## Installation

```
conda install -c ilastik-forge -c conda-forge conda-3rdparty
```

## Usages

```
conda 3rdparty -n <environment_name> > 3rdparty.txt
```

### jinja2 template support

A template for rendering can be supplied to the cli with `--template`.

#### Customization

All keys from `conda-meta/<package>.json` are available for rendering via elements the `license_infos` list.
Each `license_info` has the additional `'3rd_party_license_info'` key, with the following keys:
 * `license`: name of the license
 * `license_family`: name of the license family
 * `license_texts`: list of license texts (some packages have multiple)

##### Template examples

###### basic template

This is also the default template if no template file is supplied to cli:

```
3rd-party licenses

{% for info in license_infos %}
License for {{ info['name'] }} {{ info['version'] }}
    {% for license_text in info['3rd_party_license_info']['license_texts'] %}
{{ license_text }}
{% endfor %}
{% endfor %}
```


###### Example of template for rendering to markdown

This is also the default template if no template file is supplied to cli:

```markdown
# 3rd-party licenses

{% for info in license_infos %}
## {{ info['name'] }} {{ info['version'] }} {{ info['build'] }}
    {% for license_text in info['3rd_party_license_info']['license_texts'] %}
{{ license_text }}
{% endfor %}
{% endfor %}
```
