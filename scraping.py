import time
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

link_header = 'https://sugarbind.expasy.org'

def agent_list():
    target_link = link_header + '/agents?n=407'                                                                             # set scraping target link
    file = open('data/agent_list.csv', 'w')                                                                                # open file named "agent_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Agent ID','Agent Name'])                                                                              # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find_all 'tr' elements from got html content
    for tr in tr_elements:
        a_tag_element = tr.find_all('td')[0].find('a')                                                                      # find a tag element in a tr element
        agent_id = a_tag_element.get('href')[8:]                                                                            # extracting agent id
        agent_name = a_tag_element.get_text()                                                                               # extracting agent name
        writer.writerow([agent_id, agent_name])                                                                             # inserting extracted agent id and agent name
    file.close()                                                                                                            # close file

def agent_list_2():
    target_link = link_header + '/agents?n=407'
    file = open('data/agent_list2.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Agent ID', 'Agent Name', 'Agent Type', 'taxonomy ID', 'txonomy level', 'Lineage', 'Agent properties', 'HAMAP', 'Viralzone', 'GOLD'])
    list_html = requests.get(target_link)
    list_soup = BeautifulSoup(list_html.content, "html.parser")
    list_elements = list_soup.find('tbody').find_all('tr')
    for element in list_elements:
        name = element.find_all('td')[0].find('a')
        agent_id = name.get_text()
        agent_type_link = element.find_all('td')[2].find('a')
        agent_type = element.find_all('td')[2].find('a').get_text()
        taxonomy_id_link = element.find_all('td')[3].find('a')
        taxonomy_id = element.find_all('td')[3].find('a').get_text()
        num_asterisk = taxonomy_id.count('*')
        taxonomy_id = taxonomy_id.replace('*', '')

        element_html = requests.get(link_header + name.get('href'))
        element_soup = BeautifulSoup(element_html.content, "html.parser")
        info = element_soup.find_all('div', class_='info')
        if len(info) == 10:
        # 10 count
            # 0: References
            # 1: Glycan Structure Format
            # 2: Lineage・Type
            # 3: Agent properties
            # 4: HAMAP proteome
            # 5: Viralzone
            # 6: GOLD
            # 7: Ligands
            # 8: Biological Associations
            # 9: Diseases
            lineage = info[2].find_all('p')[0].find_all('a') if info[2].find_all('p')[0].find_all('a') else None
            agent_properties = info[3].find_all('p') if info[3].find_all('p') else None
            hamap = info[4].find('p').get_text() if info[4].find('p') else None
            viralzone = info[5].find('p').get_text() if info[5].find('p') else None
            gold = info[6].find_all('p') if info[6].find_all('p') else None
            writer.writerow([agent_id, name.get_text(), agent_type, taxonomy_id, num_asterisk, lineage, agent_properties, hamap, viralzone, gold])
        elif len(info) == 9:
        # 9 count
            # 0: References
            # 1: Glycan Structure Format
            # 2: Lineage・Type
            # 3: Agent properties
            # 4: HAMAP proteome
            # 5: GOLD
            # 6: Ligands
            # 7: Biological Associations
            # 8: Diseases
            lineage = info[2].find_all('p')[0].find_all('a') if info[2].find_all('p')[0].find_all('a') else None
            agent_properties = info[3].find_all('p') if info[3].find_all('p') else None
            hamap = info[4].find('p').get_text() if info[4].find('p') else None
            viralzone = None
            gold = info[5].find_all('p') if info[5].find_all('p') else None
            writer.writerow([agent_id, name.get_text(), agent_type, taxonomy_id, num_asterisk, lineage, agent_properties, hamap, viralzone, gold])
        time.sleep(0.75)
    file.close()

def lectin_list():
    target_link = link_header + '/lectins?n=739'                                                                            # set scraping target link
    file = open('data/lectin_list.csv', 'w')                                                                               # open file named "lectin_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Lectin name','Lectin link','Uniprot ID', 'Uniprot link', 'N/S'])                         # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find_all 'tr' elements from got html content
    for tr in tr_elements:
        a_tag_element = tr.find_all('td')[0].find('a')                                                                      # find a tag element in a tr element
        lectin_id = a_tag_element.get('href')[9:]                                                                             # extracting lectin id
        lectin_name = a_tag_element.get_text()                                                                                # extracting lectin name
        html_of_individual_lectin = requests.get(link_header + a_tag_element.get('href'))                                     # set scraping target link 
        soup_of_individual_lectin = BeautifulSoup(html_of_individual_lectin.content, "html.parser")                         # get html content as Beautiful Soup object
        uniprot = soup_of_individual_lectin.find_all(class_ = 'span4')[0].find_all(class_ = 'info')[2].find('p')            # find all uniprot related information
        if lectin_name == 'N/S':                                                                                # if lectin name is named 'N/S'
            if uniprot:                                                                                                     # if uniprot information is found
                uniprot = uniprot.find('a')
                writer.writerow([lectin_id, lectin_name, link_header + a_tag_element.get('href'),\
                                uniprot.get_text(), uniprot.get('href'), 1])                                                # inserting extracted lectin id, lectin name, lectin link, uniprot id, uniprot link, identifier of N/S
            else:                                                                                                           # if uniprot information is not found
                writer.writerow([lectin_id, lectin_name,\
                                link_header + a_tag_element.get('href'), None,None, 1])                                     # inserting extracted lectin id, lectin name, lectin link, None, None, identifier of N/S
        else:                                                                                                   # if lectin name is named other than 'N/S'
            if uniprot:
                uniprot = uniprot.find('a')
                writer.writerow([lectin_id, lectin_name, link_header + a_tag_element.get('href'),\
                                uniprot.get_text(), uniprot.get('href'), 0])
            else:
                writer.writerow([lectin_id, lectin_name,\
                                link_header + a_tag_element.get('href'), None, None, 0])
        time.sleep(0.5)                                                                                                     # stop processing for avoiding continues request for server
    file.close()                                                                                                            # close file

def disease_list():
    target_link = link_header + '/diseases'                                                                                 # set scraping target link
    file = open('data/disease_list.csv', 'w')                                                                              # open file named "disease_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Disease ID', 'Disease Name'])                                                                         # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                            # find_all 'tr' elements from got html content
    for tr in tr_elements:
        disease = tr.find_all('td')[0]                                                                                      # find a tag element in a tr element
        writer.writerow([disease.find('a').get('href')[10:],disease.find('a').get_text()])                                  # inserting extracted disease id and disease name
    file.close()                                                                                                            # close file

def area_list():
    target_link = link_header + '/affectedAreaTypes'                                                                        # set scraping target link
    file = open('data/area_list.csv', 'w')                                                                                 # open file named "area_list.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Affected Area ID', 'Area Name',\
                        'Area Type'])                                                                                       # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    area_type_index = 1                                                                                                     # set area type index {1: "System", 2: "Organ", 3: "Tissue", 4: "Cell"}
    for tr in tr_elements:
        areas = tr.find_all('td')[1].find('ul').find_all('li')                                                              # find a tag element in a tr element
        for area in areas:
            area_id = area.find('a').get('href')[15:]                                                                       # extracting area id
            area_name = area.find('a').get_text()                                                                           # extracting area name
            writer.writerow([area_id, area_name,area_type_index])                                                           # inserting extracted area id, area name, and area type index
        area_type_index += 1                                                                                                # incrementing area type index
    file.close()                                                                                                            # file close

def lectin_pubmed():
    file = open('data/lectin_pubmed.csv', 'w')                                                                             # open file named "lectin_pubmed.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Pubmed ID','Pubmed link', 'Pubmed Year', 'Pubmed Authors', 'Pubmed Title'])              # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        _html = requests.get('https://sugarbind.expasy.org/references?n=183')
        _soup = BeautifulSoup(_html.content, "html.parser")
        _table_tr = _soup.find('tbody').find_all('tr')
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            references = soup.find('tbody').find_all('tr')                                                                  # find all 'tr' elements from individual lectin page
            for reference in references:
                if reference.find_all('td')[3].find('a'):
                    pmlink = reference.find_all('td')[3].find('a').get('href')
                    pmid = reference.find_all('td')[3].find('a').get_text()                                                 # if there are any reference
                    pmy = None
                    pma = None
                    pmt = None
                    for tr in _table_tr:
                        if tr.find_all('td')[4] == pmid:
                            pmy = tr.find_all('td')[1]
                            pma = tr.find_all('td')[2]
                            pmt = tr.find_all('td')[0]
                    writer.writerow([row[0], pmid, pmlink, pmy, pma, pmt])                      # inserting extracted lectin id, pubmed id, pubmed link
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close                                                                                                              # file close

def lectin_ligand():
    file = open('data/lectin_ligand.csv', 'w')                                                                             # open file named "lectin_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Ligand ID'])                                                                             # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:                                                                                                  
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for ligand in soup.find(id = 'more-ligand0ligand').find_all('li'):
                writer.writerow([row[0], ligand.find('a').get('href')[9:]])                                                 # inserting extracted lectin id, ligand id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def ligand_glycoconjugate():
    file = open('data/ligand_glycoconjugate.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Liogand ID', 'Glycoconjugate URL', 'Glycoconjugate Name'])
    url = 'https://sugarbind.expasy.org/ligands?n=204'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    table = soup.find('tbody')
    trs = table.find_all('tr')
    for tr in trs:
        # print(tr.find_all('td')[1])
        try:
            ligand = tr.find_all('td')[0].find('ul').find_all('li')[0].find('a').get('href')[9:]
            link = tr.find_all('td')[1].find('a').get('href')
            name = tr.find_all('td')[1].find('a').get_text()
            writer.writerow([ligand, link_header + link, name])
        except:
            pass
    file.close()

    

def lectin_agent():
    file = open('data/lectin_agent.csv', 'w')                                                                              # open file named "lectin_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Agent ID'])                                                                              # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for agent in soup.find(id = 'more-taxonomy0bioassociations').find_all('li'):
                writer.writerow([row[0], agent.find('a').get('href')[8:]])                                                  # inserting extracted lectin id, agent id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def lectin_area():
    file = open('data/lectin_affect.csv', 'w')                                                                             # open file named "lectin_affect.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Lectin ID', 'Affect ID'])                                                                             # describe header title
    with open('data/lectin_list.csv') as lectin_file:
        reader = csv.reader(lectin_file)                                                                                    # set csv reader
        _ = next(reader)                                                                                                    # pass_header_row
        for row in reader:
            html = requests.get(row[2])                                                                                     # get html via request
            soup = BeautifulSoup(html.content, "html.parser")                                                               # get html content as Beautiful Soup object
            for area in soup.find(id = 'more-source0bioassociations').find_all('li'):
                writer.writerow([row[0], area.find('a').get('href')[15:]])                                                  # inserting extracted lectin id, agent id
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def structure_ligand():
    target_link = link_header + '/ligands?n=204'                                                                            # set scraping target link
    file = open('data/ligand_names.csv', 'w')                                                                              # open file named "ligand_names.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Ligand ID', 'Ligand name', 'Unnamed'])                                                                # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for tr in tr_elements:
        if tr.find_all('td')[0].find('ul'):                                                                     # if there are more than 1 ligand or not
            for ligand in tr.find('ul').find_all('li'):
                writer.writerow([ligand.find('a').get('href')[9:], ligand.find('a').get_text(), 0])                         # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
        else:
            ligand_id = tr.find('a').get('href')[9:]
            if tr.find('a').get_text() == 'Unnamed':                                                            # if ligand name is named as 'Unnamed' or not
                writer.writerow([ligand_id, tr.find('a').get_text(), 1])                                                    # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
            else:
                writer.writerow([ligand_id, tr.find('a').get_text(), 0])                                                    # inserting extracted ligand id, ligand name, and identifier wheather 'Unnamed'
    file.close()                                                                                                            # file close

    file = open('data/structure_ligand.csv', 'w')                                                                          # open file named "structure_ligand.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Ligand ID', 'Structure ID', 'Structure link', 'Glytoucan ID', 'Glytoucan link'])                      # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for tr in tr_elements:
        ligand_id = tr.find('a').get('href')[9:]                                                                            # extracting ligand id
        structure_link = tr.find_all('td')[4].find('a').get('href')                                                         # extracting structure link
        structure_id = structure_link[12:]                                                                                  # extracting structure id
        if structure_link:                                                                                      # if structure link exist
            structure_html = requests.get('https://sugarbind.expasy.org' + structure_link)                                  # get structure html via request 
            structure_soup = BeautifulSoup(structure_html.content, "html.parser")                                           # get structure html content as Beautiful Soup object
            glytoucan = structure_soup.find_all(class_ = 'info')[2]                                                         # find all 'info' elements, related to glytoucan, from got html content
            if glytoucan.find('a'):
                glytoucan_link = glytoucan.find('a').get('href')                                                                    # extracting glytoucan link
                glytoucan_id = glytoucan.find('a').get_text()                                                                       # extracting glytoucan id
                writer.writerow([ligand_id, structure_id, link_header + structure_link, glytoucan_id, glytoucan_link])      # inserting extracted ligand id, structure id, structure link, glytoucan id, glytoucan link
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def agent_disease():
    target_link = link_header + '/agents?n=407'                                                                             # set scraping target link
    file = open('data/agent_disease.csv', 'w')                                                                             # open file named "agent_disease.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Agent ID','Agent Name','Disease ID','Disease Name'])                                                  # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for row in tr_elements:
        agent = row.find_all('td')[0].find('a')                                                                             # find all 'td, a' elements, related to agent, from got html content
        agent_id = agent.get('href')[8:]                                                                                    # extracting agent id
        agent_name = agent.get_text()                                                                                       # extracting agent name
        agent_html = requests.get(link_header + agent.get('href'))                                                          # get agent html via request
        agent_soup = BeautifulSoup(agent_html.content, "html.parser")                                                       # get agent html content as Beautiful Soup object
        for disease in agent_soup.find(id = 'more-disease0disease').find_all('li'):                                         
            disease_id = disease.find('a').get('href')[10:]                                                                 # extracting disease id
            disease_name = disease.find('a').get_text()                                                                     # extracting disease name
            writer.writerow([agent_id, agent_name, disease_id, disease_name])                                               # inserting extracted agent id, agent name, disease id, and disease name
        time.sleep(0.5)                                                                                                     # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def area_disease():
    target_link = link_header + '/affectedAreaTypes'                                                                        # set scraping target link
    file = open('data/area_disease.csv', 'w')                                                                              # open file named "area_disease.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Affected Area ID', 'Affected Area Name', 'Disease ID', 'Disease Name'])                               # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                       # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                         # find all 'tr' elements from got html content
    for row in tr_elements:
        for area in row.find_all('td')[1].find('ul').find_all('li'):
            area_id = area.find('a').get('href')[15:]                                                                       # extracting area id
            area_name = area.find('a').get_text()                                                                           # extracting area name
            area_html = requests.get(link_header + area.find('a').get('href'))                                              # get area html via request
            area_soup = BeautifulSoup(area_html.content, "html.parser")                                                     # get area html content as Beautiful Soup object
            for disease in area_soup.find( id = "more-disease0disease").find_all('li'):
                disease_id = disease.find('a').get('href')[10:]                                                             # extracting disease id
                disease_name = disease.find('a').get_text()                                                                 # extracting disease name
                writer.writerow([area_id, area_name, disease_id, disease_name])                                             # inserting extracted area id, area name, disease id, and disease name
            time.sleep(0.5)                                                                                                 # stop processing for avoiding continues request for server
    file.close()                                                                                                            # file close

def agent_area():
    target_link = link_header + '/affectedAreaTypes'                                                                        # set scraping target link
    file = open('data/agent_affected_area.csv', 'w')                                                                       # open file named "agent_affected_area.csv" in "data" folder
    writer = csv.writer(file)                                                                                               # set csv writer
    writer.writerow(['Agent ID', 'Agent Name', 'Affected Area ID', 'Affected Area Name', 'Area Type'])                      # describe header title
    html = requests.get(target_link)                                                                                        # get html via request
    soup = BeautifulSoup(html.content, "html.parser")                                                                          # get html content as Beautiful Soup object
    tr_elements = soup.find('tbody').find_all('tr')                                                                            # find all 'tr' elements from got html content

    index = 1                                                                                                               # set area type identifier
    for row in tr_elements:
        for agent in row.find_all('td')[2].find('ul').find_all('li'):
            agent_a = agent.find('a')                                                                                       # extracting agent a tag element
            agent_html = requests.get(link_header + agent_a.get('href'))                                                    # get agent html via request
            agent_soup = BeautifulSoup(agent_html.content, "html.parser")                                                   # get agent html content as Beautiful Soup object
            for agent_area in agent_soup.find(id = 'more-source0bioassociations').find_all('li'):
                area_id = agent_area.find('a').get('href')[15:]                                                             # extracting area id
                area_name = agent_area.find('a').get_text()                                                                 # extracting area name
                writer.writerow([agent_a.get('href')[8:], agent_a.get_text(), area_id, area_name, index])                   # inserting extracted agent id, agent name, area id, area name, and type identifier
            time.sleep(0.5)                                                                                                 # stop precessing for avoiding continues request for server
            index += 1                                                                                                      # incrementing identifier
    file.close()                                                                                                            # file close

def ttl_ReferenceInteraction():
    df_lectin = pd.read_csv('data/lectin_list.csv').sort_values(by = 'Lectin ID', ascending = True)                        # open file as pandas data frame
    df_lectin_ns = df_lectin[df_lectin['N/S'] == 1]                                                                         # open file as pandas data frame
    df_lectin_ = df_lectin[df_lectin['N/S'] == 0]                                                                           # open file as pandas data frame
    df_lectin_agent = pd.read_csv('data/lectin_agent.csv')                                                                 # open file as pandas data frame
    df_lectin_area = pd.read_csv('data/lectin_affect.csv')                                                                 # open file as pandas data frame
    df_lectin_ligand = pd.read_csv('data/lectin_ligand.csv').sort_values(by = 'Ligand ID', ascending = True)               # open file as pandas data frame
    df_lectin_pubmed = pd.read_csv('data/lectin_pubmed.csv').sort_values(by = 'Pubmed ID', ascending = True)               # open file as pandas data frame
    df_ligand_structure = pd.read_csv('data/structure_ligand.csv')                                                         # open file as pandas data frame
    df_ligand_names = pd.read_csv('data/ligand_names.csv')                                                                 # open file as pandas data frame
    
    file = open('output/referenced_interaction.ttl', 'w', encoding='UTF-8')                                                # open file named "referenced_interaction.ttl" in "output" folder
    file.write('#######################################################\n')                                                 
    file.write('### Individuals (lectin including N/S) \n')                                                                 # inserting ttl header title
    file.write('#######################################################\n\n')

    for index, item in df_lectin_ns.iterrows():
        lectin_id = item['Lectin ID']                                                                                       # extracting lectin id
        filtered_ligand = df_lectin_ligand.loc[df_lectin_ligand['Lectin ID'] == lectin_id]                                  # filtering loaded data frame with lectin id
        filtered_pubmed = df_lectin_pubmed.loc[df_lectin_pubmed['Lectin ID'] == lectin_id]                                  
        filtered_area = df_lectin_area.loc[df_lectin_area['Lectin ID'] == lectin_id]                                        
        filtered_agent = df_lectin_agent.loc[df_lectin_agent['Lectin ID'] == lectin_id]                                     
        title = 'LEC' + str(lectin_id) + '_'                                                                                # initiate title string
        for index, item in filtered_ligand.iterrows():
            title += 'LIG' + str(item['Ligand ID']) + '_'                                                                   # add ligand information to title
        for index, item in filtered_pubmed.iterrows():
            title += 'PUB' + str(item['Pubmed ID']) + '_'                                                                   # add pubmed information to title
        for index, item in filtered_area.iterrows():
            title += 'ARE' + str(item['Affect ID']) + '_'                                                                   # add area information to title
        for index, item in filtered_agent.iterrows():
            title += 'AGE' + str(item['Agent ID']) + '_'                                                                    # add agent information to title
        title = title[:-1]                                                                                                  # cut off last '-' from title string
        file.write(f'interaction:{title} rdf:type owl:NamedIndividual ,\n')                                                            # add ttl type description
        file.write('\t\t\t:ReferencedInteraction ;\n')                                                                      # add ttl class type description
        # lectin
        file.write(f'\t\t:has_lectin <https://sugarbind.expasy.org/lectins/{lectin_id}> ;\n')                               # add ttl object property and lectin URI

        # ligand
        if len(filtered_ligand) > 0:                                                                                        # if ligand exists in filtered data frame
            document = ''                                                                                                   # initiate document as string data
            for index2, item2 in filtered_ligand.iterrows():
                document += f'<https://sugarbind.expasy.org/ligands/{item2["Ligand ID"]}> ,\n\t\t\t'                        # add ligand URI to document
            document = document[:-5] + ';\n'                                                                                # cut off last 5 letters and add \n
            file.write('\t\t:has_ligand ')                                                                                  # add ttl object property
            file.write(document)                                                                                            # inserting ligand information to ttl
        # pubmed
        if len(filtered_pubmed) > 0:                                                                                        # if pubmed exists in filtered data frame
            document = ''
            for index2, item2 in filtered_pubmed.iterrows():
                document += f'<http://www.ncbi.nlm.nih.gov/pubmed/{item2["Pubmed ID"]}> ,\n\t\t\t'                          # add pubmed URI to document
            document = document[:-5] + ';\n'
            file.write('\t\t:has_pubmed ')
            file.write(document)
        # agent
        if len(filtered_agent) > 0:                                                                                         # if agent exists in filtered data frame
            document = ''
            for index2, item2 in filtered_agent.iterrows():
                document += f'<https://sugarbind.expasy.org/agents/{item2["Agent ID"]}> ,\n\t\t\t'                          # add agent URI to document
            document = document[:-5] + ';\n'
            file.write('\t\t:has_agent ')
            file.write(document)
        # area
        if len(filtered_area) > 0:                                                                                          # if agent exists in filtered data frame
            document = ''
            for index2, item2 in filtered_area.iterrows():
                document += f'<https://sugarbind.expasy.org/affectedAreas/{item2["Affect ID"]}> ,\n\t\t\t'                  # add agent URI to document
            document = document[:-5] + ';\n'
            file.write('\t\t:has_area ')
            file.write(document)
        file.write(f'\t\trdfs:label "{title}"^^xsd:string .\n\n')                                                           # inserting closing ttl statement

        
    # f.close()
    file.write('\n\n\n#######################################################\n')
    file.write('### Individuals (lectin without N/S) \n')                                                                   # inserting ttl header title
    file.write('#######################################################\n\n')

    for index, item in df_lectin_.iterrows():
        lectin_id = item['Lectin ID']                                                                                       # extracting lectin id
        filtered_ligand = df_lectin_ligand.loc[df_lectin_ligand['Lectin ID'] == lectin_id]                                  # filtering loaded data frame with lectin id
        filtered_pubmed = df_lectin_pubmed.loc[df_lectin_pubmed['Lectin ID'] == lectin_id]
        filtered_area = df_lectin_area.loc[df_lectin_area['Lectin ID'] == lectin_id]
        filtered_agent = df_lectin_agent.loc[df_lectin_agent['Lectin ID'] == lectin_id]
        title = 'LEC' + str(lectin_id) + '_'                                                                                # initiate title string
        for index, item in filtered_ligand.iterrows():
            title += 'LIG' + str(item['Ligand ID']) + '_'                                                                   # add ligand information to title
        for index, item in filtered_pubmed.iterrows():
            title += 'PUB' + str(item['Pubmed ID']) + '_'                                                                   # add pubmed information to title
        for index, item in filtered_area.iterrows():
            title += 'ARE' + str(item['Affect ID']) + '_'                                                                   # add area information to title
        for index, item in filtered_agent.iterrows():
            title += 'AGE' + str(item['Agent ID']) + '_'                                                                    # add agent information to title
        title = title[:-1]
        
        file.write(f'interaction:{title} rdf:type owl:NamedIndividual ,\n')                                                            # add ttl type description
        file.write('\t\t\t:ReferencedInteraction ;\n')                                                                      # add ttl class type description
        # lectin
        file.write(f'\t\t:has_lectin <https://sugarbind.expasy.org/lectins/{lectin_id}> ;\n')                               # add ttl object property and lectin URI

        # ligand
        if len(filtered_ligand) > 0:                                                                                        # if ligand exists in filtered data frame
            document = ''                                                                                                   # initiate document as string data
            for index2, item2 in filtered_ligand.iterrows():
                document += f'<https://sugarbind.expasy.org/ligands/{item2["Ligand ID"]}> ,\n\t\t\t'                        # add ligand URI to document
            document = document[:-5] + ';\n'                                                                                # cut off last 5 letters and add \n
            file.write('\t\t:has_ligand ')                                                                                  # add ttl object property
            file.write(document)                                                                                            # inserting ligand information to ttl
        # pubmed
        if len(filtered_pubmed) > 0:                                                                                        # if pubmed exists in filtered data frame
            document = ''
            for index2, item2 in filtered_pubmed.iterrows():
                document += f'<http://www.ncbi.nlm.nih.gov/pubmed/{item2["Pubmed ID"]}> ,\n\t\t\t'
            document = document[:-5] + ';\n'
            file.write('\t\t:has_pubmed ')
            file.write(document)
        # agent
        if len(filtered_agent) > 0:                                                                                         # if agent exists in filtered data frame
            document = ''
            for index2, item2 in filtered_agent.iterrows():
                document += f'<https://sugarbind.expasy.org/agents/{item2["Agent ID"]}> ,\n\t\t\t'
            document = document[:-5] + ';\n'
            file.write('\t\t:has_agent ')
            file.write(document)
        # area
        if len(filtered_area) > 0:                                                                                          # if area exists in filtered data frame
            document = ''
            for index2, item2 in filtered_area.iterrows():
                document += f'<https://sugarbind.expasy.org/affectedAreas/{item2["Affect ID"]}> ,\n\t\t\t'
            document = document[:-5] + ';\n'
            file.write('\t\t:has_area ')
            file.write(document)
        file.write(f'\t\trdfs:label "{title}"^^xsd:string .\n\n')
    file.close()

def ttl_pubmed():
    df_pubmed = pd.read_csv('data/lectin_pubmed.csv').sort_values(by = 'Pubmed ID', ascending = True)                      # open file as pandas data frame
    file = open('output/pubmed.ttl', 'w', encoding='UTF-8')                                                                # open file named "pubmed.ttl" in "output" folder
    file.write('#######################################################\n')
    file.write('### Individuals (Pubmed) \n')                                                                               # inserting ttl header title
    file.write('#######################################################\n\n')
    for index, item in df_pubmed.iterrows():
        file.write(f'<http://www.ncbi.nlm.nih.gov/pubmed/{item["Pubmed ID"]}> rdf:type owl:NamedIndividual ,\n\t\t\t:Pubmed ;\n\t\t:pubmedId "http://www.ncbi.nlm.nih.gov/pubmed/{item["Pubmed ID"]}"^^xsd:anyURI ;\n\t\trdfs:label "{item["Pubmed ID"]}"^^xsd:string .\n\n')
                                                                                                                            # inserting ttl content
    file.close()

def ttl_structure():
    df_structure = pd.read_csv('data/structure_ligand.csv').sort_values(by = 'Structure ID', ascending = True)             # open file as pandas data frame
    file = open('output/structure.ttl', 'w', encoding= 'UTF-8')                                                            # open file named "structure.ttl" in "output" folder
    file.write('#######################################################\n')
    file.write('### Individuals (Structure) \n')                                                                            # inserting ttl header
    file.write('#######################################################\n\n')
    for index, item in df_structure.iterrows():
        file.write(f'<https://sugarbind.expasy.org/structures/{item["Structure ID"]}> rdf:type owl:NamedIndividual ,\n\t\t\t:Structure ;\n\t\t:glytoucanId glycoinfo:{item["Glytoucan ID"]} ;\n\t\t:structureId "{item["Structure link"]}"^^xsd:anyURI ;\n\t\trdfs:label "{item["Structure ID"]}"^^xsd:string .\n\n')
                                                                                                                            # inserting ttl content
    file.close()

def ttl_ligand():
    df_ligand = pd.read_csv('data/lectin_ligand.csv').sort_values(by = 'Ligand ID', ascending = True)                      # open file as pandas data frame
    df_ligand_names = pd.read_csv('data/ligand_names.csv').sort_values(by = 'Ligand ID', ascending = True)                 
    df_structure_ligand = pd.read_csv('data/structure_ligand.csv').sort_values(by = 'Ligand ID', ascending = True)         
    file = open('output/ligand.ttl', 'w', encoding='UTF-8')                                                                # open file named "ligand.ttl" in "output" folder
    file.write('#######################################################\n')
    file.write('### Individuals (Ligand) \n')                                                                               # inserting ttl header
    file.write('#######################################################\n\n')
    for index in range(1, 205):
        file.write(f'''<https://sugarbind.expasy.org/ligands/{ index }> rdf:type owl:NamedIndividual ,\n\t\t\t:Ligand ;\n\t\t:ligandId "https://sugarbind.expasy.org/ligands/{ index }"^^xsd:anyURI ;\n''')
                                                                                                                            # inserting ttl content

        filtered_structure_ligand = df_structure_ligand.loc[df_structure_ligand['Ligand ID'] == index]                      # filtering loaded data frame with ligand id
        if len(filtered_structure_ligand) > 0:                                                                              # if structure ligand exists in filtered data frame
            document = ''                                                                                                   # initiate document as string data
            for index2, item2 in filtered_structure_ligand.iterrows():
                document += f'<https://sugarbind.expasy.org/structures/{ item2["Structure ID"] }> ,\n\t\t\t'                # add structure URI to document
            file.write('\t\t:has_structure ')                                                                               # add ttl object property
            file.write( document[:-5] + ';\n')                                                                              # inserting ligand information to ttl

        filtered_ligand_names = df_ligand_names.loc[df_ligand_names['Ligand ID'] == index]                                  # filtering loaded data frame with ligand id

        if len(filtered_ligand_names) > 0:                                                                                  # if ligand names exists in filtered data frame
            document = ''
            for index2, item2 in filtered_ligand_names.iterrows():
                if item2["Unnamed"]:
                    document += f'"{item2["Ligand ID"] }"^^xsd:string ,\n\t\t\t\t\t'
                else:
                    document += f'"{item2["Ligand name"]}"^^xsd:string ,\n\t\t\t\t\t'
            file.write('\t\trdfs:label ')
            file.write(document[:-7] + '.\n\n')
    file.close()

def ttl_lectin():
    df_lectin = pd.read_csv('data/lectin_list.csv').sort_values(by = 'Lectin ID', ascending = True)                        # open file as pandas data frame
    df_lectin_ns = df_lectin[df_lectin['N/S'] == 1]                                                                         # filtering loaded data frame with N/S
    file = open('output/lectin.ttl', 'w', encoding='UTF-8')                                                                # open file named "lectin.ttl" in "output" folder
    file.write('#######################################################\n')
    file.write('### Individuals (Lectin including N/S) \n')                                                                 # inserting ttl header
    file.write('#######################################################\n\n')
    for index, item in df_lectin_ns.iterrows():
        if type(item["Uniprot ID"]) is str:
            file.write(f'<https://sugarbind.expasy.org/lectins/{ item["Lectin ID"] }> rdf:type owl:NamedIndividual ,\n\t\t\t:Lectin ;\n\t:lectinId "https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}"^^xsd:anyURI ;\n\t:uniprotId <http://purl.uniprot.org/uniprot/{ item["Uniprot link"][32:] }> ;\n\trdfs:label "{item["Lectin ID"]}"^^xsd:string .\n\n')
        else:
            file.write(f'<https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}> rdf:type owl:NamedIndividual ,\n\t\t\t:Lectin ;\n\t:lectinId "https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}"^^xsd:anyURI ;\n\trdfs:label "{item["Lectin ID"]}"^^xsd:string .\n\n')
    file.write('#######################################################\n')
    file.write('### Individuals (Lectin without N/S) \n')
    file.write('#######################################################\n\n')
    df_lectin_ = df_lectin[df_lectin['N/S'] == 0]
    for index, item in df_lectin_.iterrows():
        if type(item["Uniprot ID"]) is str:
            file.write(f'<https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}> rdf:type owl:NamedIndividual ,\n\t\t\t:Lectin ;\n\t:lectinId "https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}"^^xsd:anyURI ;\n\t:uniprotId <http://purl.uniprot.org/uniprot/{ item["Uniprot link"][32:] }> ;\n\trdfs:label "{item["Lectin name"]}"^^xsd:string .\n\n')
        else:
            file.write(f'<https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}> rdf:type owl:NamedIndividual ,\n\t\t\t:Lectin ;\n\t:lectinId "https://sugarbind.expasy.org/lectins/{item["Lectin ID"]}"^^xsd:anyURI ;\n\trdfs:label "{item["Lectin name"]}"^^xsd:string .\n\n')
    file.close()

def ttl_disease():
    df_disease_agent = pd.read_csv('data/agent_disease.csv').sort_values(by = 'Disease ID', ascending = True)              # open file as pandas data frame
    df_disease_area = pd.read_csv('data/area_disease.csv').sort_values(by = 'Disease ID', ascending = True)
    df_disease_list = pd.read_csv('data/disease_list.csv').sort_values(by = 'Disease ID', ascending = True)

    file = open('output/disease.ttl', 'w', encoding = 'UTF-8')                                                             # open file named "disease.ttl" in "output" folder
    file.write('#######################################################\n')
    file.write('### Individuals (Disease)\n')                                                                               # inserting ttl header
    file.write('#######################################################\n\n')
    for index in range(1, 48):
        disease_name = df_disease_list.loc[df_disease_list['Disease ID'] == index]['Disease Name']                          # filtering loaded data frame with disease name
        filtered_disease_agent = df_disease_agent.loc[df_disease_agent['Disease ID'] == index]
        filtered_disease_area = df_disease_area.loc[df_disease_area['Disease ID'] == index]
        if len(filtered_disease_agent) > 0 or len(filtered_disease_area) > 0:
            text = f'<https://sugarbind.expasy.org/diseases/{ index }> rdf:type owl:NamedIndividual ,\n\t\t:Disease ;\n'
            if len(filtered_disease_agent) == 1:                                                                            # if the number related to disease is 1 or not
                for ind, item in filtered_disease_agent.iterrows():
                    text += f"""\t:caused_by <https://sugarbind.expasy.org/agents/{ str(item['Agent ID']) }> ;\n"""         # inserting

            elif len(filtered_disease_agent) > 1:
                firstLoop = True
                for ind, item in filtered_disease_agent.iterrows():
                    if firstLoop:
                        text += f"""\t:caused_by <https://sugarbind.expasy.org/agents/{ str(item['Agent ID']) }> ,\n"""
                        firstLoop = False
                    else:
                        text += f"""\t\t<https://sugarbind.expasy.org/agents/{ str(item['Agent ID']) }> ,\n"""
                text = text[:-2] + ';\n'


            if len(filtered_disease_area) == 1:
                for ind, item in filtered_disease_area.iterrows():
                    text += f"""\t:caused_at <https://sugarbind.expasy.org/affectedAreas/{ str(item['Affected Area ID']) }> ;\n"""
            elif len(filtered_disease_area) > 1:
                firstLoop = True
                for ind, item in filtered_disease_area.iterrows():
                    if firstLoop:
                        text += f"""\t:caused_at <https://sugarbind.expasy.org/affectedAreas/{ str(item['Affected Area ID']) }> ,\n"""
                        firstLoop = False
                    else:
                        text += f"""\t\t<https://sugarbind.expasy.org/affectedAreas/{ str(item['Affected Area ID']) }> ,\n"""
                text = text[:-2] + ';\n'
            text += f'\t:diseaseId "{ index }"^^xsd:string ;\n\trdfs:label "{ disease_name.values[0] }"^^xsd:string .\n'

            file.write(text + '\n')
    file.close()

def ttl_area():
    df_area_list = pd.read_csv('data/area_list.csv').sort_values(by = 'Affected Area ID', ascending = True)

    file = open('output/area.ttl', 'w', encoding = 'UTF-8')                                                                
    file.write('#######################################################\n')
    file.write('### Individuals (Area)\n')
    file.write('#######################################################\n\n')
    for index, item in df_area_list.iterrows():
        category = ''
        text = f'<https://sugarbind.expasy.org/affectedAreas/{item["Affected Area ID"]}> rdf:type owl:NamedIndividual ,\n'
        if item["Area Type"] == 1:
            category = 'System'
        elif item["Area Type"] == 2:
            category = 'Organ'
        elif item["Area Type"] == 3:
            category = 'Tissue'
        else:
            category = 'Cell'
        text += f'\t\t:Area ,\n'
        text += f'\t\t:{category} ;\n'
        text += f'\t:areaId "{item["Affected Area ID"]}"^^xsd:string ;\n'
        text += f'\trdfs:label "{item["Area Name"]}"^^xsd:string .\n\n'
        file.write(text)
    file.close()

def ttl_agent():
    df_agent_list = pd.read_csv('data/agent_list.csv').sort_values(by = 'Agent ID', ascending = True)
    df_agent_disease = pd.read_csv('data/agent_disease.csv').sort_values(by = 'Agent ID', ascending = True)
    df_agent_area = pd.read_csv('data/agent_affected_area.csv').sort_values(by = 'Agent ID', ascending = True)

    file = open('output/agent.ttl', 'w', encoding = 'UTF-8')
    file.write('#######################################################\n')
    file.write('### Individuals (Agent)\n')
    file.write('#######################################################\n\n')
    count = 0
    for index, item in df_agent_list.iterrows():
        filtered_agent_disease = df_agent_disease.loc[df_agent_disease['Agent ID'] == item['Agent ID']]
        filtered_agent_area = df_agent_area.loc[df_agent_area['Agent ID'] == item['Agent ID']]
        if len(filtered_agent_disease) > 0 or len(filtered_agent_area) > 0:
            text = f'<https://sugarbind.expasy.org/agents/{ item["Agent ID"] }> rdf:type owl:NamedIndividual ,\n\t\t:Agent ;\n'
            if len(filtered_agent_disease) == 1:
                for ind, ite in filtered_agent_disease.iterrows():
                    text += f'\t:causes <https://sugarbind.expasy.org/diseases/{ ite["Disease ID"] }> ;\n'
            elif len(filtered_agent_disease) > 1:
                firstLoop = True
                for ind, ite in filtered_agent_disease.iterrows():
                    if firstLoop:
                        text += f'\t:causes <https://sugarbind.expasy.org/diseases/{ ite["Disease ID"] }> ,\n'
                        firstLoop = False
                    else:
                        text += f'\t\t<https://sugarbind.expasy.org/diseases/{ ite["Disease ID"] }> ,\n'
                text = text[:-2] + ';\n'
            if len(filtered_agent_area) == 1:
                for ind, ite in filtered_agent_area.iterrows():
                    count += 1
                    text += f'\t:found_in <https://sugarbind.expasy.org/affectedAreas/{ ite["Affected Area ID"] }> ;\n'
            elif len(filtered_agent_area) > 1:
                firstLoop = True
                for ind, ite in filtered_agent_area.iterrows():
                    if firstLoop:
                        text += f'\t:found_in <https://sugarbind.expasy.org/affectedAreas/{ ite["Affected Area ID"] }> ,\n'
                        firstLoop = False
                        count += 1
                    else:
                        text += f'\t\t<https://sugarbind.expasy.org/affectedAreas/{ ite["Affected Area ID"] }> ,\n'
                        count += 1
                text = text[:-2] + ';\n'
            text += f'\t:agentId "{ item["Agent ID"] }"^^xsd:string ;\n\trdfs:label "{ item["Agent Name"] }"^^xsd:string .\n'
        else:
            text = f'<https://sugarbind.expasy.org/agents/{ item["Agent ID"] }> rdf:type owl:NamedIndividual ,\n\t\t:Agent ;\n\t:agentId "{ item["Agent ID"] }"^^xsd:string ;\n\trdfs:label "{ item["Agent Name"] }"^^xsd:string .\n'
        file.write(text + '\n')
    file.close()

def merge_ttl(files):
    for a in files:
        print(a + '.ttl')

if __name__ == "__main__":
    agent_list_2()
    # ### scraping from sugarbind ( https://sugarbind.expasy.org )
    # agent_list()
    #     # creating agent_list.csv
    # lectin_list()
    #     # creating lectin_list.csv
    # disease_list()
    #     # creating disease_list.csv
    # area_list()
    #     # creating area_list.csv
    # lectin_pubmed()
    #     # creating lectin_pubmed.csv
    # lectin_ligand()
    #     # creating lectin_ligand.csv
    # structure_ligand()
    #     # creating ligand_names.csv, structure_ligand
    # area_disease()
    #     # creating area_disease.csv
    # agent_area()
    #     # creating agent_affected_area.csv
    # agent_disease()
    #     # creating agent_disease.csv
    # lectin_area()
    #     # creating lectin_area.csv
    # lectin_agent()
    #     # creating lectin_agent.csv
    
    # ### making ttl file from csv created above
    # ttl_ReferenceInteraction()  
    #     # requires lectin_list.csv, lectin_agent.csv, lectin_affect.csv, lectin_ligand.csv, lectin_pubmed.csv, structure_ligand.csv, ligand_names.csv
    # ttl_pubmed()                
    #     # requires lectin_pubmed.csv
    # ttl_structure()             
    #     # requires structure_ligand.csv
    # ttl_ligand()                
    #     # requires lectin_ligand.csv, ligand_names.csv, structure_ligand.csv
    # ttl_lectin()                
    #     # requires lectin_list.csv
    # ttl_area()                  
    #     # requires area_list.csv
    # ttl_agent()                 
    #     # requires agent_list.csv, agent_disease.csv, agent_affected_area.csv
    # ttl_disease()               
    #     # requires agent_disease.csv, area_disease.csv, disease_list.csv

    merge_ttl(['agent', 'area', 'disease', 'lectin', 'ligand', 'pubmed', 'referenced_interaction', 'structure'])
    # passing string arguments which corresponds to the file name stored in the output folder
