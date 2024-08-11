# render-alloy-templates
A tool for rendering [Grafana Alloy](https://grafana.com/docs/alloy) configurations from a set of templates.

The tool expects the following directory structure (this can be customized somewhat, see below):

```
.
├── templates
│   └── default
│       ├── example_1.yaml
│       ├── example_2.yaml
│       └── template.alloy.j2
└── pipelines
```

which will then result in a matching directory structure in the outputs directory, e.g.:

```
.
├── pipelines
│   └── default
│       ├── collector_1.alloy
│       └── collector_2.alloy
└── templates
    └── default
        ├── collector_1.yaml
        ├── collector_2.yaml
        └── template.alloy.j2
```

## Run with Docker

You can use the tool with Docker by running:
```bash
docker container run -v ./templates:/app/templates -v ./pipelines:/app/pipelines mischathompson/render-alloy-templates:jinja2 
```

If you would like to use different input/output directories than the defaults, you can set env vars to change them. Make sure that the directories exist beforehand!
```bash
docker container run -v ./<INPUTS DIR>:/app/templates -v ./<OUTPUTS DIR>:/app/pipelines mischathompson/render-alloy-templates:jinja2 
```

## Run Locally
You can run the tool by running:
```bash
pip install -r requirements.txt
python3 render_templates.py
```

If you would like to alter the inputs/outputs directories, you can run the following:
```bash
INPUT_INPUTS_DIR=<INPUTS DIR> INPUT_OUTPUTS_DIR=<OUTPUTS DIR> python3 render_templates.py 
``
