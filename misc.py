# for cwe in root.findall("./" + URL + "severity/[@level='3']/" + URL + "category/" + URL + "cwe/" + URL + "staticflaws/" + URL + "flaw"):

# [print(elem.tag) for elem in root.iter()]

# View entire document
# print(ET.tostring(root, encoding='utf8').decode('utf8'))

# for description in root.iter('description'):
#     print(description.text)

# for movie in root.findall("./genre/decade/movie/[year='1992']"):

# for child in root:
#     print(child.tag, child.attrib)

# for movie in root.iter(URL + "category"):
#     print(movie.attrib["categoryname"])

#for modu in root.findall("./" + URL + "severity/"):