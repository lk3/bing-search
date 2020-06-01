# bing-search

## Requirements


## Running the script

Run the script like this:

```
python bing_asgsearch.py <input.csv> <startRow> <endRow> <free|s2>
```

These are the required parameters:

```
input.csv: path to csv input file with format: ID in 1st column, search key in 2nd column

startRow: starts processing from this csv row

endRow: stops processing at this csv row

Last parameter (config name): should match the section name of the config file (see below).
```


### config.py file

Create a config.cfg file in this repo root like this:

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