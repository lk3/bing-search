# bing-search

## Requirements


## Running the script

Run the script like this:

```
python bing_asgsearch.py <input.csv> <startRow> <endRow> <free|s2>
```

Last parameter (config name) should match the section name of the config file (see below).


### config.py file

Using your "<cognitiveServicesKey>" parameter from the Cognitive Services resource and the "<customConfig>" parameter of the Bing Custom Search application, create a config.cfg file in this repo root like this:

```
# Free version of Bing API
[free]
cognitiveServicesKey = <cognitiveServicesKey>
customConfig = <customConfig>
endPoint = <endPoint>
millisBetweenCalls = 1000

# Paid version of Bing API, S2 tier
[s2]
cognitiveServicesKey = <cognitiveServicesKey>
customConfig = <customConfig>
endPoint = <endPoint>
millisBetweenCalls = 10

```