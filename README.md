# glycobot

Twitter bot for posting of glyco-related preprint literature from BioRxiv and ChemRxiv.

----

# BioRxiv 

The script use requests package to scrape html page from BioRxiv search result of the term "glycosylation" within abstract and title of articles. For each page of the search result, the script retrieve author lists, title, and doi link for each article found.

# ChemRxiv

The script directly scrape JSON data package from ChemRxiv search result of the term "glycosylation". After unmarshalling the data package, each items within will be parsed for list of authors together with article title and hyperlink to each article within ChemRxiv.