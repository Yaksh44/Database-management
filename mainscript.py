"""
DB Final Data Engineering Scripts
David Hawbaker
Yaksh Patel
"""
import csv
import json
import os


def parse_metadata(root, synsetIds):
    # Read metadata files
    metafile = root + '/metadata_airplanes.txt'
    metafile_out = root + '/metadata_airplanes_out.txt'
    rel_out = root + '/meshRel_insert.txt'

    insert_strings = []
    rel_insert_strings = []

    print(metafile_out)
    with open(metafile, 'r') as f:
        # first line is headers. Ignore
        line = f.readline()
        while True:
            front = ""
            name = ""
            line = f.readline()
            print(line)

            if not line:
                break

            # split on ','
            elem = line.split(',"')
            # 0 Remove '3dw.' to get mesh ID

            if len(elem) >= 1:
                fullId = elem[0]
                meshId = elem[0][4:]

            # 1 Split on ',' first element is synset ID
            if len(elem) >= 2:
                wnsynset = elem[1].split(',')

                ids = []
                for syn_id in wnsynset:
                    if syn_id in synsetIds:
                        ids.append(syn_id)

            # 2
            if len(elem) >= 3:
                wnlemmas = elem[2]
            # 3 up
            if len(elem) >= 4:
                up = elem[3]

            # 4 front & Name
            if len(elem) >= 5:
                if '",' in elem[4]:
                    front, name = elem[4].split('",')
                else:
                    front = elem[4]

            # 5 Tags
            # tags = elem[5]


            for synsetID in ids:
                ins_str = "INSERT INTO MeshRel (" + synsetID + ", " + meshId + ")\n"
                rel_insert_strings.append(ins_str)

            """
            for synsetID in ids:
                ins_str = "INSERT INTO MetadataAirplanes (\"" + fullId + "\", " + synsetID + ", \"" + wnlemmas + "\", \"" \
                          + front + "\", \"" + up + "\", \"" + name[:-2] + "\")\n"
                insert_strings.append(ins_str)
            """

    # Write metadata file to database
    """
    with open(metafile_out, 'w') as outfile:
        outfile.writelines(insert_strings)
    """
    with open(rel_out, 'w') as outfile:
        outfile.writelines(rel_insert_strings)



def parse_metadata2(root, synsetIds):
    # Read metadata files
    metafile = root + '/metadata.csv'
    metafile_out = root + '/metadata_insert.txt'
    rel_out = root + '/meshRel_insert.txt'

    insert_strings = []
    rel_insert_strings = []

    print(metafile_out)
    with open(metafile, newline='') as f:
        # first line is headers. Ignore
        csvreader = csv.reader(f, delimiter=',', quotechar='"')
        next(csvreader)
        for line in csvreader:
            front = ""
            name = ""

            # 0 Remove '3dw.' to get mesh ID

            #fullId 0
            fullId = line[0]
            meshId = line[0][4:]

            # category 1
            # TODO?

            # wnsynset 2
            # 1 Split on ',' first lineent is synset ID
            wnsynset = line[2][1:] #.split(',')

            ids = []
            for syn_id in wnsynset:
                if syn_id in synsetIds:
                    ids.append(syn_id)

            # wnlemmas 3
            wnlemmas = line[3]

            # up 4
            up = line[4]

            # front 5
            front = line[5]

            # unit 6

            # aligned.dims 7

            # isContainerLike 8

            # surfaceVolume 9

            # solidVolume 10

            # supportSurfaceArea 11

            # weight 12

            # staticFrictionForce 13

            # name 14
            name = line[14]

            # tags 15
            tags = line[15]

            """
            for synsetID in ids:
                ins_str = "INSERT INTO MeshRel (" + synsetID + ", " + meshId + ")\n"
                rel_insert_strings.append(ins_str)
            """
            #for synsetID in ids:
            ins_str = "INSERT INTO Metadata (\"" + fullId + "\", " + wnsynset+ ", \"" + wnlemmas + "\", \"" \
                      + front + "\", \"" + up + "\", \"" + name[:-2] + "\"" + ", " + tags + ")\n"
            insert_strings.append(ins_str)

    # Write metadata file to database
    with open(metafile_out, 'w') as outfile:
        outfile.writelines(insert_strings)
    """
    with open(rel_out, 'w') as outfile:
        outfile.writelines(rel_insert_strings)
    """

def parse_model_json(root):
    # planes 02691156
    path = root + "/02691156"
    l = os.listdir(path)
    metafile_out = root + "/meshData_insert.txt"

    insert_strings = []

    for mesh in l:
        infile = path + '/' + mesh + '/models/model_normalized.json'

        with open(infile) as file:
            meshdata = json.load(file)

            ins_str = "INSERT INTO MeshData (" + meshdata['id'] + ", " \
                      + str(meshdata['numVertices']) + ", " \
                      + str(meshdata['min'][0]) + ", " + str(meshdata['min'][1]) + ", " + str(meshdata['min'][2]) + ", " \
                      + str(meshdata['max'][0]) + ", " + str(meshdata['max'][1]) + ", " + str(meshdata['max'][2]) + ", " \
                      + str(meshdata['centroid'][0]) + ", " + str(meshdata['centroid'][1]) + ", " \
                      + str(meshdata['centroid'][2]) + ")\n"
            insert_strings.append(ins_str)

    with open(metafile_out, 'w') as outfile:
        outfile.writelines(insert_strings)

def parse_taxonomy(root):
    # planes 02691156
    #path = root + "/02691156"
    #l = os.listdir(path)
    categories_out = root + "/categories_insert.txt"
    children_out = root + "/children_insert.txt"

    insert_strings = []
    child_insert_strings = []

    infile = root + '/' + 'taxonomy.json'

    with open(infile) as file:
        meshdata = json.load(file)

        for obj in meshdata:
            ins_str = "INSERT INTO Categories (" + obj['synsetId'] + ", '" + obj['name'] + "', " \
                      + str(obj['numInstances']) + ")\n"
            insert_strings.append(ins_str)

            for child in obj['children']:
                child_ins_str = "INSERT INTO ChildrenRel (" + obj['synsetId'] + ", " + child + ")\n"
                child_insert_strings.append(child_ins_str)

    with open(categories_out, 'w') as outfile:
        outfile.writelines(insert_strings)

    with open(children_out, 'w') as outfile:
        outfile.writelines(child_insert_strings)


def parse_images(root):
    images_out = root + "/images_insert.txt"
    image_insert_strings = []
    cat_dirs = os.listdir(root)

    for category in cat_dirs:
        print(category)

        if category.endswith((".txt", ".json")) or category.startswith("."):
            continue

        mesh_dirs = os.listdir(root + '/' + category)
        for mesh in mesh_dirs:
            mesh_contents = os.listdir(root + '/' + category + '/' + mesh)
            if 'images' in mesh_contents:
                images = os.listdir(root + '/' + category + '/' + mesh + '/images')
                for image in images:
                    image_insert_string = "INSERT INTO Images (" + mesh + ", " + image + ")\n"
                    image_insert_strings.append(image_insert_string)

    with open(images_out, 'w') as outfile:
        outfile.writelines(image_insert_strings)

if __name__ == "__main__":
    root = "/media/david/My Passport/Education/PSU/ShapeNet/ShapeNetCore.v2"
    root2 = "/media/david/My Passport/Education/PSU/ShapeNet/ShapeNetSem.v0"

    #l = os.listdir(root)
    #synsetIds = l[:-3]

    #parse_metadata(root, synsetIds)
    #parse_metadata2(root2, synsetIds)
    #parse_model_json(root)
    #parse_taxonomy(root)
    parse_images(root)


