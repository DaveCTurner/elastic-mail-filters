#!/usr/bin/python

from xml.etree.ElementTree import Element, SubElement, ElementTree, QName
from sys import stdout

def atom(tag):
  return QName('http://www.w3.org/2005/Atom', tag)

def apps(tag):
  return QName('http://schemas.google.com/apps/2006', tag)

feed = Element(atom('feed'))

for project, label in [
    ['elasticsearch', 'Elasticsearch/OSS'],
    ['x-pack-elasticsearch', 'Elasticsearch/X-pack'],
    ['kibana', 'Kibana/OSS'],
    ['x-pack-kibana', 'Kibana/X-pack'],
    ['logstash', 'Logstash/OSS'],
    ['x-pack-logstash', 'Logstash/X-pack'],
    ['docs', 'Docs'],
    ['apm-server', 'APM Server'],
    ['release-manager', 'Release Manager']]:

  for branch in ['5.6', '6.0', '6.1', '6.x', 'master']:

    entry = SubElement(feed, atom('entry'))

    SubElement(entry, atom('category')).set(atom('term'), 'filter')
    SubElement(entry, atom('title')).text = 'Mail Filter'

    def addProperty(name, value):
      property = SubElement(entry, apps('property'))
      property.set(atom('name'), name)
      property.set(atom('value'), value)

    addProperty('from', 'build@elastic.co')
    addProperty('subject', '"FAILURE elastic/' + project + '#' + branch + '"')
    addProperty('label', 'CI/' + label + '/' + branch)
    addProperty('sizeOperator', 's_sl')
    addProperty('sizeUnit', 's_smb')

ElementTree(feed).write(stdout, encoding='utf-8', xml_declaration=True, default_namespace='http://www.w3.org/2005/Atom')
