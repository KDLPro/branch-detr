import os
import time
from PIL import Image
import xml.etree.ElementTree as ET

if __name__ == "__main__":


    img_no, annot_no = 0, 0     #for image id and annotation id

    #Initialize Dataset file
    small_filename = 'annotations/instances_train2017.json'
    smallfile = open(small_filename, "a")
    smallfile.close()

    #Clear Dataset file, if it exists
    with open(small_filename, 'r+') as file:
        file.truncate(0)
    smallfile = open(small_filename, "a")

    #Start writing Annotations file
    smallfile.write("{\n")

    smallfile.write("   \"info\": {\n")                
    smallfile.write("         \"description\": \"Vision Transformer Dataset\",\n")               
    smallfile.write("         \"url\": \"n/a\",\n")               
    smallfile.write("         \"version\": \"1.0\",\n")               
    smallfile.write("         \"year\": \"2022\",\n")               
    smallfile.write("         \"contributor\": \"Luke Heri Contrivida and Kenneth Ligutom\",\n")               
    smallfile.write("         \"date_created\": \"2022/5/1\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"licenses\": {\n")                
    smallfile.write("         \"url\": \"https://creativecommons.org/licenses/by-nd/4.0/\",\n")               
    smallfile.write("         \"id\": \"1\",\n")               
    smallfile.write("         \"name\": \"Attribution-NoDerivs License\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"images\": [\n")
    smallfile.close()

    img_no = 0
    img_len = len(os.listdir("train2017"))
    
    #Open img directory
    for filename in os.listdir("train2017"):
        print("Reading image data from ", filename, "...", sep = "")
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        new_filename = "train2017/" + filename
        image = Image.open(new_filename)
        ti_m = os.path.getmtime(new_filename)
        m_ti = time.ctime(ti_m)
        # Using the timestamp string to create a 
        # time object/structure
        t_obj = time.strptime(m_ti)
        # Transforming the time object to a timestamp 
        # of ISO 8601 format
        T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

        smallfile.write("      {\n")

        smallfile.write("         \"license\": 1, \n")

        smallfile.write("         \"file_name\": \"")
        smallfile.write(filename)
        smallfile.write("\",\n")

        smallfile.write("         \"height\": ")
        smallfile.write(str(image.height))
        smallfile.write(",\n")

        smallfile.write("         \"width\": ")
        smallfile.write(str(image.width))
        smallfile.write(",\n")

        smallfile.write("         \"date_captured\": \"")
        smallfile.write(T_stamp)
        smallfile.write("\",\n")

        smallfile.write("         \"id\": ")
        smallfile.write(str(img_no))
        smallfile.write("\n")

        if (filename != (os.listdir("train2017")[img_len - 1])):
            smallfile.write("      },\n")
        else:
            smallfile.write("      }\n")

        image.close() #close image
        
    smallfile.write("   ],\n")

    smallfile.write("   \"categories\": [\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 1, \"name\": \"leaf\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 2, \"name\": \"tree branch\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 3, \"name\": \"branch with leaves\"},\n")                 
    smallfile.write("         {\"supercategory:\": \"mahogany tree\", \"id\": 4, \"name\": \"mahogany fruit\"}\n")
    smallfile.write("   ],\n")
    
    smallfile.write("   \"annotations\": [\n")
    smallfile.close()

    img_no = 0
    wrong_cat_1 = []
    
    #Open xml directory
    for filename in os.listdir("train2017-xml"):
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        with open(os.path.join("train2017-xml", filename), 'r') as xml_file:
            print("Annotating ", filename, "...", sep = "")
            tree = ET.parse(xml_file)
            root = tree.getroot()
            xmin, xmax = [], []
            ymin, ymax = [], []
            category = []

            #Gather annotation values from xml files
            for coord in root.iter('xmin'):
                xmin.append(str(coord.text))
            for coord in root.iter('xmax'):
                xmax.append(str(coord.text))
            for coord in root.iter('ymin'):
                ymin.append(str(coord.text))
            for coord in root.iter('ymax'):
                ymax.append(str(coord.text))
            for cat in root.iter('name'):
                category.append(cat.text)

            #Write in annotations json file
            for i in range(len(xmin)):
                annot_no += 1
                smallfile.write("      {\n")
                              
                smallfile.write("         \"segmentation\": [")
                smallfile.write("[" + xmin[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymax[i] + "],\n")
                smallfile.write("                          [" + xmin[i] + ", " + ymax[i] + "]")
                smallfile.write("],\n")

                smallfile.write("         \"iscrowd\": ")
                if category[i] == "leaf":
                    smallfile.write("0")
                elif category[i] == "tree branch":
                    smallfile.write("0")
                elif category[i] == "branch with leaves":
                    smallfile.write("1")
                elif category[i] == "mahogany fruit":
                    smallfile.write("0")
                elif category[i] not in wrong_cat_1:
                    wrong_cat_1.append(category[i])
                    print(filename, i)
                else:
                    print(filename, i)
                smallfile.write(",\n")

                smallfile.write("         \"area\": ")
                smallfile.write(str(int((int(float(xmax[i])) - int(float(xmin[i]))) *
                                    (int(float(ymax[i])) - int(float(ymin[i]))))))
                smallfile.write(",\n")

                smallfile.write("         \"image_id\": ")
                smallfile.write(str(img_no))
                smallfile.write(",\n")

                smallfile.write("         \"bbox\": [")
                smallfile.write(str(float(xmin[i])) + ", " + str(float(ymin[i])) + ", ")
                smallfile.write(str(float(xmax[i])) + ", " + str(float(ymax[i])) + "],\n")

                smallfile.write("         \"category_id\": ")
                if category[i] == "leaf":
                    smallfile.write("1")
                elif category[i] == "tree branch":
                    smallfile.write("2")
                elif category[i] == "branch with leaves":
                    smallfile.write("3")
                elif category[i] == "mahogany fruit":
                    smallfile.write("4")
                elif category[i] not in wrong_cat_1:
                    wrong_cat_1.append(category[i])
                smallfile.write(",\n")

                smallfile.write("         \"id\": ")
                smallfile.write(str(annot_no))
                smallfile.write("\n")
                
                if (filename != (os.listdir("train2017-xml")[img_len - 1]) or i != len(xmin) - 1):
                    smallfile.write("      },\n")
                else:
                    smallfile.write("      }\n")
                
    smallfile.write("   ]\n")
    smallfile.write("}")
    smallfile.close()       #close json file

    wrong_cat_2 = []

    #Initialize Dataset file
    small_filename = 'annotations/instances_val2017.json'
    smallfile = open(small_filename, "a")
    smallfile.close()

    #Clear Dataset file, if it exists
    with open(small_filename, 'r+') as file:
        file.truncate(0)
    smallfile = open(small_filename, "a")

    #Start writing Annotations file
    smallfile.write("{\n")

    smallfile.write("   \"info\": {\n")                
    smallfile.write("         \"description\": \"Vision Transformer Dataset\",\n")               
    smallfile.write("         \"url\": \"n/a\",\n")               
    smallfile.write("         \"version\": \"1.0\",\n")               
    smallfile.write("         \"year\": \"2022\",\n")               
    smallfile.write("         \"contributor\": \"Luke Heri Contrivida and Kenneth Ligutom\",\n")               
    smallfile.write("         \"date_created\": \"2022/5/1\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"licenses\": {\n")                
    smallfile.write("         \"url\": \"https://creativecommons.org/licenses/by-nd/4.0/\",\n")               
    smallfile.write("         \"id\": \"1\",\n")               
    smallfile.write("         \"name\": \"Attribution-NoDerivs License\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"images\": [\n")
    smallfile.close()

    img_no = 0
    img_len = len(os.listdir("val2017"))
    
    #Open img directory
    for filename in os.listdir("val2017"):
        print("Reading image data from ", filename, "...", sep = "")
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        new_filename = "val2017/" + filename
        image = Image.open(new_filename)
        ti_m = os.path.getmtime(new_filename)
        m_ti = time.ctime(ti_m)
        # Using the timestamp string to create a 
        # time object/structure
        t_obj = time.strptime(m_ti)
        # Transforming the time object to a timestamp 
        # of ISO 8601 format
        T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

        smallfile.write("      {\n")

        smallfile.write("         \"license\": 1, \n")

        smallfile.write("         \"file_name\": \"")
        smallfile.write(filename)
        smallfile.write("\",\n")

        smallfile.write("         \"height\": ")
        smallfile.write(str(image.height))
        smallfile.write(",\n")

        smallfile.write("         \"width\": ")
        smallfile.write(str(image.width))
        smallfile.write(",\n")

        smallfile.write("         \"date_captured\": \"")
        smallfile.write(T_stamp)
        smallfile.write("\",\n")

        smallfile.write("         \"id\": ")
        smallfile.write(str(img_no))
        smallfile.write("\n")

        if (filename != (os.listdir("val2017")[img_len - 1])):
            smallfile.write("      },\n")
        else:
            smallfile.write("      }\n")

        image.close() #close image
        
    smallfile.write("   ],\n")

    smallfile.write("   \"categories\": [\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 1, \"name\": \"leaf\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 2, \"name\": \"tree branch\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 3, \"name\": \"branch with leaves\"},\n")                 
    smallfile.write("         {\"supercategory:\": \"mahogany tree\", \"id\": 4, \"name\": \"mahogany fruit\"}\n")
    smallfile.write("   ],\n")
    
    smallfile.write("   \"annotations\": [\n")
    smallfile.close()

    img_no = 0
    
    #Open xml directory
    for filename in os.listdir("val2017-xml"):
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        with open(os.path.join("val2017-xml", filename), 'r') as xml_file:
            print("Annotating ", filename, "...", sep = "")
            tree = ET.parse(xml_file)
            root = tree.getroot()
            xmin, xmax = [], []
            ymin, ymax = [], []
            category = []

            #Gather annotation values from xml files
            for coord in root.iter('xmin'):
                xmin.append(str(coord.text))
            for coord in root.iter('xmax'):
                xmax.append(str(coord.text))
            for coord in root.iter('ymin'):
                ymin.append(str(coord.text))
            for coord in root.iter('ymax'):
                ymax.append(str(coord.text))
            for cat in root.iter('name'):
                category.append(cat.text)

            #Write in annotations json file
            for i in range(len(xmin)):
                annot_no += 1
                smallfile.write("      {\n")
                              
                smallfile.write("         \"segmentation\": [")
                smallfile.write("[" + xmin[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymax[i] + "],\n")
                smallfile.write("                          [" + xmin[i] + ", " + ymax[i] + "]")
                smallfile.write("],\n")

                smallfile.write("         \"iscrowd\": ")
                if category[i] == "leaf":
                    smallfile.write("0")
                elif category[i] == "tree branch":
                    smallfile.write("0")
                elif category[i] == "branch with leaves":
                    smallfile.write("1")
                elif category[i] == "mahogany fruit":
                    smallfile.write("0")
                elif category[i] not in wrong_cat_2:
                    wrong_cat_2.append(category[i])
                    print(filename, i)
                else:
                    print(filename, i)
                smallfile.write(",\n")

                smallfile.write("         \"area\": ")
                smallfile.write(str(int((int(float(xmax[i])) - int(float(xmin[i]))) *
                                    (int(float(ymax[i])) - int(float(ymin[i]))))))
                smallfile.write(",\n")

                smallfile.write("         \"image_id\": ")
                smallfile.write(str(img_no))
                smallfile.write(",\n")

                smallfile.write("         \"bbox\": [")
                smallfile.write(str(float(xmin[i])) + ", " + str(float(ymin[i])) + ", ")
                smallfile.write(str(float(xmax[i])) + ", " + str(float(ymax[i])) + "],\n")

                smallfile.write("         \"category_id\": ")
                if category[i] == "leaf":
                    smallfile.write("1")
                elif category[i] == "tree branch":
                    smallfile.write("2")
                elif category[i] == "branch with leaves":
                    smallfile.write("3")
                elif category[i] == "mahogany fruit":
                    smallfile.write("4")
                elif category[i] not in wrong_cat_2:
                    wrong_cat_2.append(category[i])
                smallfile.write(",\n")

                smallfile.write("         \"id\": ")
                smallfile.write(str(annot_no))
                smallfile.write("\n")
                
                if (filename != (os.listdir("val2017-xml")[img_len - 1]) or i != len(xmin) - 1):
                    smallfile.write("      },\n")
                else:
                    smallfile.write("      }\n")
                
    smallfile.write("   ]\n")
    smallfile.write("}")
    smallfile.close()       #close json file
	
    wrong_cat_3 = []

    #Initialize Dataset file
    small_filename = 'annotations/instances_test2017.json'
    smallfile = open(small_filename, "a")
    smallfile.close()

    #Clear Dataset file, if it exists
    with open(small_filename, 'r+') as file:
        file.truncate(0)
    smallfile = open(small_filename, "a")

    #Start writing Annotations file
    smallfile.write("{\n")

    smallfile.write("   \"info\": {\n")                
    smallfile.write("         \"description\": \"Vision Transformer Dataset\",\n")               
    smallfile.write("         \"url\": \"n/a\",\n")               
    smallfile.write("         \"version\": \"1.0\",\n")               
    smallfile.write("         \"year\": \"2022\",\n")               
    smallfile.write("         \"contributor\": \"Luke Heri Contrivida and Kenneth Ligutom\",\n")               
    smallfile.write("         \"date_created\": \"2022/5/1\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"licenses\": {\n")                
    smallfile.write("         \"url\": \"https://creativecommons.org/licenses/by-nd/4.0/\",\n")               
    smallfile.write("         \"id\": \"1\",\n")               
    smallfile.write("         \"name\": \"Attribution-NoDerivs License\"\n")
    smallfile.write("      },\n")

    smallfile.write("   \"images\": [\n")
    smallfile.close()

    img_no = 0
    img_len = len(os.listdir("val2017"))
    
    #Open img directory
    for filename in os.listdir("val2017"):
        print("Reading image data from ", filename, "...", sep = "")
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        new_filename = "val2017/" + filename
        image = Image.open(new_filename)
        ti_m = os.path.getmtime(new_filename)
        m_ti = time.ctime(ti_m)
        # Using the timestamp string to create a 
        # time object/structure
        t_obj = time.strptime(m_ti)
        # Transforming the time object to a timestamp 
        # of ISO 8601 format
        T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

        smallfile.write("      {\n")

        smallfile.write("         \"license\": 1, \n")

        smallfile.write("         \"file_name\": \"")
        smallfile.write(filename)
        smallfile.write("\",\n")

        smallfile.write("         \"height\": ")
        smallfile.write(str(image.height))
        smallfile.write(",\n")

        smallfile.write("         \"width\": ")
        smallfile.write(str(image.width))
        smallfile.write(",\n")

        smallfile.write("         \"date_captured\": \"")
        smallfile.write(T_stamp)
        smallfile.write("\",\n")

        smallfile.write("         \"id\": ")
        smallfile.write(str(img_no))
        smallfile.write("\n")

        if (filename != (os.listdir("val2017")[img_len - 1])):
            smallfile.write("      },\n")
        else:
            smallfile.write("      }\n")

        image.close() #close image
        
    smallfile.write("   ],\n")

    smallfile.write("   \"categories\": [\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 1, \"name\": \"leaf\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 2, \"name\": \"tree branch\"},\n")                
    smallfile.write("         {\"supercategory:\": \"plant part\", \"id\": 3, \"name\": \"branch with leaves\"},\n")                 
    smallfile.write("         {\"supercategory:\": \"mahogany tree\", \"id\": 4, \"name\": \"mahogany fruit\"}\n")
    smallfile.write("   ],\n")
    
    smallfile.write("   \"annotations\": [\n")
    smallfile.close()

    img_no = 0
    
    #Open xml directory
    for filename in os.listdir("val2017-xml"):
        smallfile = open(small_filename, "a")   #open json file
        img_no += 1
        with open(os.path.join("val2017-xml", filename), 'r') as xml_file:
            print("Annotating ", filename, "...", sep = "")
            tree = ET.parse(xml_file)
            root = tree.getroot()
            xmin, xmax = [], []
            ymin, ymax = [], []
            category = []

            #Gather annotation values from xml files
            for coord in root.iter('xmin'):
                xmin.append(str(coord.text))
            for coord in root.iter('xmax'):
                xmax.append(str(coord.text))
            for coord in root.iter('ymin'):
                ymin.append(str(coord.text))
            for coord in root.iter('ymax'):
                ymax.append(str(coord.text))
            for cat in root.iter('name'):
                category.append(cat.text)

            #Write in annotations json file
            for i in range(len(xmin)):
                annot_no += 1
                smallfile.write("      {\n")
                              
                smallfile.write("         \"segmentation\": [")
                smallfile.write("[" + xmin[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymin[i] + "],\n")
                smallfile.write("                          [" + xmax[i] + ", " + ymax[i] + "],\n")
                smallfile.write("                          [" + xmin[i] + ", " + ymax[i] + "]")
                smallfile.write("],\n")

                smallfile.write("         \"iscrowd\": ")
                if category[i] == "leaf":
                    smallfile.write("0")
                elif category[i] == "tree branch":
                    smallfile.write("0")
                elif category[i] == "branch with leaves":
                    smallfile.write("1")
                elif category[i] == "mahogany fruit":
                    smallfile.write("0")
                elif category[i] not in wrong_cat_3:
                    wrong_cat_3.append(category[i])
                    print(filename, i)
                else:
                    print(filename, i)
                smallfile.write(",\n")

                smallfile.write("         \"area\": ")
                smallfile.write(str(int((int(float(xmax[i])) - int(float(xmin[i]))) *
                                    (int(float(ymax[i])) - int(float(ymin[i]))))))
                smallfile.write(",\n")

                smallfile.write("         \"image_id\": ")
                smallfile.write(str(img_no))
                smallfile.write(",\n")

                smallfile.write("         \"bbox\": [")
                smallfile.write(str(float(xmin[i])) + ", " + str(float(ymin[i])) + ", ")
                smallfile.write(str(float(xmax[i])) + ", " + str(float(ymax[i])) + "],\n")

                smallfile.write("         \"category_id\": ")
                if category[i] == "leaf":
                    smallfile.write("1")
                elif category[i] == "tree branch":
                    smallfile.write("2")
                elif category[i] == "branch with leaves":
                    smallfile.write("3")
                elif category[i] == "mahogany fruit":
                    smallfile.write("4")
                elif category[i] not in wrong_cat_3:
                    wrong_cat_3.append(category[i])
                smallfile.write(",\n")

                smallfile.write("         \"id\": ")
                smallfile.write(str(annot_no))
                smallfile.write("\n")
                
                if (filename != (os.listdir("val2017-xml")[img_len - 1]) or i != len(xmin) - 1):
                    smallfile.write("      },\n")
                else:
                    smallfile.write("      }\n")
                
    smallfile.write("   ]\n")
    smallfile.write("}")
    smallfile.close()       #close json file


    print(wrong_cat_1)
    print(wrong_cat_2)
    print(wrong_cat_3)
