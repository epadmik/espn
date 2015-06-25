import pdb
from lxml import etree
import urllib2
import json
import unicodedata
import csv
 
def unicode_to_string(types):
    try:
        types = unicodedata.normalize("NFKD", types).encode('ascii', 'ignore')
        return types
    except:
        return types

def main():
	start_urls = [
	"http://espn.go.com/nba/players"
		]

	master = []
	master_arry = []
	for s in start_urls:
		#Loops through all of the start urls
		responses = urllib2.urlopen(s).read()
		trees = etree.HTML(responses) #makes it into a HTML tree to call xpath on
		teams = trees.xpath('//ul[@class="small-logos"]//div//a//text()')
		links = trees.xpath('//ul[@class="small-logos"]//div//a//@href')
		for lk in links:
			print lk
			base = "http://espn.go.com"
			response = urllib2.urlopen(base + lk).read()
			tree = etree.HTML(response)
			table = tree.xpath('//tr')
			i = 3
			data = []
			while(i< len(table)):
				data.append(table[i].xpath('//tr['+str(i) +']//text()'))
				i+=1

			for dd in data:
				player = {}
				player['team'] = unicode_to_string(lk.split("=")[-1])
				player['number'] = unicode_to_string(dd[0])
				player['name'] = unicode_to_string(dd[1])
				player['position'] = unicode_to_string(dd[2])
				player['age'] = unicode_to_string(dd[3])
				player['height'] = unicode_to_string(dd[4])
				player['weight'] = unicode_to_string(dd[5])
				player['college'] = unicode_to_string(dd[6])
				player['salary'] = unicode_to_string(dd[7])
				master.append(player)
				master_arry.append([player['team'], player['number'], player['name'], player['position'],
					player['age'], player['height'], player['weight'], player['college'], player['salary']])
				print player

	with open("data.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(master_arry)

	with open('dataaa.json', 'a') as outfile:
		json.dump(master, outfile, indent=4)

main()
