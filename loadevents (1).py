import json
import re
import datetime

# python3 -i loadevents.py

# http://www.vizgr.org/historical-events/
# http://www.vizgr.org/historical-events/wikieventRDF_en_year.n3
# http://www.vizgr.org/historical-events/wikieventRDF_en_month.n3


with open('hist_month.js', encoding='utf8') as json_data:
   hEvents = json.load(json_data)

# returns a 'event' JSON object
# An example looks like this:
"""
{
  "@id" : "http://lod.gesis.org/historicalevents/HEafc61975e9ce41603037502e491329d0",
  "http://linkedevents.org/ontology/atTime" : [ {
    "@type" : "http://www.w3.org/2001/XMLSchema#Date",
    "@value" : "2001-09-11"
  } ],
  "http://linkedevents.org/ontology/illustrate" : [ {
    "@id" : "http://upload.wikimedia.org/wikipedia/commons/thumb/8/88/1WTC28Jan2012.png/150px-1WTC28Jan2012.png"
  } ],
  "http://linkedevents.org/ontology/involvedAgent" : [ {
    "@id" : "http://dbpedia.org/resource/September_11_attacks"
  }, {
    "@id" : "http://dbpedia.org/resource/New_York_City"
  }, {
    "@id" : "http://dbpedia.org/resource/The_Pentagon"
  }, {
    "@id" : "http://dbpedia.org/resource/Pennsylvania"
  } ],
  "http://purl.org/dc/terms/description" : [ {
    "@language" : "en",
    "@value" : "The September 11 terrorist attacks take place in New York City, The Pentagon, and in Pennsylvania, killing 2,977 people."
  } ],
  "http://purl.org/dc/terms/isPartOf" : [ {
    "@id" : "http://lod.gesis.org/historicalevents/"
  } ]
}
"""
def event_date(event):
    return event['http://linkedevents.org/ontology/atTime'][0]['@value']

def event_description(event):
    return event['http://purl.org/dc/terms/description'][0]['@value']

# returns list of image uri's 
def event_images(event):
    if "http://linkedevents.org/ontology/illustrate" in event:
        return list(map(lambda entry: entry['@id'] , event["http://linkedevents.org/ontology/illustrate"]))
    else:
        return None

def event_involved_agents(event):
    if "http://linkedevents.org/ontology/involvedAgent" in event:
        return list(map(lambda entry: entry['@id'], event["http://linkedevents.org/ontology/involvedAgent"]))
    else:
        return None


# return list of urls
def event_is_part_of(event):
    return list(map(lambda entry: entry['@value'] , event['http://purl.org/dc/terms/isPartOf']))


def lookup_event_by_date(mydate):
    matching_events = []
    # loop over events, looking for matching date
    for event in hEvents:
        if 'http://linkedevents.org/ontology/atTime' in event:
            etime = event['http://linkedevents.org/ontology/atTime']
            if len(etime) > 0:
                edate = etime[0]['@value']
                if edate == mydate:
                    matching_events.append(event)
    # if no event with matching date was found, return None
    return matching_events

# e.g., lookup_event_by_date('1997-11-19')

# datetime.datetime.strptime('2001-09-11', '%Y-%m-%d')
# datetime.date(2011, 1, 1)

# lookup_event_between_datesstrings('2001-09-01', '2001-09-12')
def lookup_event_between_datestrings(start, end):
    # parse start and end  strings into datetime objects
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    return lookup_event_between_datetimes(start_date, end_date)

# example usage
# lookup_event_between_datetimes(datetime.date(2011, 1, 1), datetime.date(2011, 1, 5))
def lookup_event_between_datetimes(start_date, end_date):
    matching_events = []
    # loop over events, looking for matching date
    for event in hEvents:
        if 'http://linkedevents.org/ontology/atTime' in event:
            etime = event['http://linkedevents.org/ontology/atTime']
            if len(etime) > 0:
                edate = etime[0]['@value']
                try:
                    edatetime = datetime.datetime.strptime(edate, '%Y-%m-%d')
                    if start_date <= edatetime and end_date >= edatetime:
                        matching_events.append(event)
                except: # if event date parse fails
                    continue
    # if no event with matching date was found, return None
    return matching_events


# example usage
# lookup_event_by_date_regexp('199.-09-..')
def lookup_event_by_date_regexp(mydate):
    matching_events = []
    # loop over events, looking for matching date
    for event in hEvents:
        if 'http://linkedevents.org/ontology/atTime' in event:
            etime = event['http://linkedevents.org/ontology/atTime']
            if len(etime) > 0:
                edate = etime[0]['@value']
                if re.match(mydate, edate):
                    matching_events.append(event)
    # if no event with matching date was found, return None
    return matching_events

   
   
