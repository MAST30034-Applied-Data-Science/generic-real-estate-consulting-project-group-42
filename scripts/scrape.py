



# for each url, scrape some basic metadata
for property_url in url_links[1:]:
    bs_object = BeautifulSoup(urlopen(property_url), "lxml")

    # looks for the header class to get property name
    property_metadata[property_url]['name'] = bs_object \
        .find("h1", {"class": "css-164r41r"}) \
        .text

    # may need preprocessing 
    # looks for the div containing a summary title for cost
    property_metadata[property_url]['cost_text'] = bs_object \
        .find("div", {"data-testid": "listing-details__summary-title"}) \
        .text

    # extract coordinates from the hyperlink provided
    # finds latitude and longitude from integrated Google Map
    property_metadata[property_url]['coordinates'] = [
        float(coord) for coord in re.findall(
            r'destination=([-\s,\d\.]+)', # use regex101.com here if you need to
            bs_object \
                .find(
                    "a",
                    {"target": "_blank", 'rel': "noopener noreferer"}
                ) \
                .attrs['href']
        )[0].split(',')
    ]

    property_metadata[property_url]['rooms'] = [
        re.findall(r'\d\s[A-Za-z]+', feature.text)[0] for feature in bs_object \
            .find("div", {"data-testid": "property-features"}) \
            .findAll("span", {"data-testid": "property-features-text-container"})
    ]

    property_metadata[property_url]['desc'] = re \
        .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
        .strip('</p>')

# output to example json in data/raw/
with open('../data/raw/example.json', 'w') as f:
    dump(property_metadata, f)

