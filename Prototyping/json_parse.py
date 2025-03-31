import json

#open json file
f = open('fa21-fa24.json')

#return json object as dictionary
data = json.load(f)

#create dictionary object to hold deparment codes
#dept_codes = {}

#create output files for parsed data
#class_list_PKI will contain information for all classes in all departments scheduled to a room in PKI
class_list_PKI = open("class_list_PKI.txt", "w", encoding="utf-8")

#class_info_list will contain the information from PKI_class_list as well as the information for each class
class_info_list = open("class_info_list.txt", "w", encoding="utf-8")

#department_codes contains the codes of departments scheduling to PKI **contains duplicates**
department_codes = open("department_codes.txt", "w", encoding="utf-8")


general_output = open("general_output.txt", "w", encoding="utf-8")

#define substrings for location search
substring = "Peter Kiewit Institute"

#access first level of json structure. key1: semester code
for key1, value1 in data.items():
    #write semester code to output files
    class_list_PKI.write('Semester Code: ' + key1 + '\n')
    class_info_list.write('Semester Code: ' + key1 + '\n')

    general_output.write('Semester Code: ' + key1 + '\n')

    #access second level of json structure. key2: department code
    for key2, value2 in value1.items():
    
        #access third level of json structure. key3: course code
        for key3, value3 in value2.items():
            
            #access fourth level of json structure. key4: string attributes under course code
            #title, desc, prereqs, sections
            for key4, value4 in value3.items():
                
                #access fifth level of json structure through 'sections' attribute. key5: section number
                if key4 == 'sections':
                    for key5, value5 in value4.items():

                        #access sixth level of json structure. key6: string attributes under each section
                        #search for classes located in PKI by searching the 'Location' attribute for 
                        #substring: "Peter Kiewit Institute"
                        #print relevant class details to general_output file
                        for key6, value6 in value5.items():
                            if key6 == 'Location':
                                #output.write('\t\t\t' + str(value6) + '\n')
                                if substring in str(value6):
                                   
                                    #output.write(key1 + '\n\n')
                                    #output.write('\t' + key2 + '\n\n')
                                    department_codes.write(key1 + '\t' + key2 + '\n')
                                    #dept_codes.update(key2)
                                    
                                    general_output.write('\t' + key2 + '\t\t' + key3 + '\t\t' + 'Section: ' + key5 + '\t\t' + str(value6) + '\n')
                                    class_list_PKI.write('\t' + key2 + '\t\t' + key3 + '\t\t' + 'Section: ' + key5 + '\t\t' + str(value6) + '\n')
                                    class_info_list.write('\t' + key2 + '\t\t' + key3 + '\t\t' + 'Section: ' + key5 + '\t\t' + str(value6) + '\n')
                                    class_info_list.write('\t\t' + str(value5) + '\n')
                                    #general_output.write('\t' + key3)
                                    #general_output.write('\t' + 'Section: ' + key5)
                                    #general_output.write('\t' + str(value6) + '\n')
                                    

