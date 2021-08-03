# glycovid_sugarbind
This project includes 
- scraping file [scraping.py]
- virtual environment [venv]
- base ontology [ontology.owl]
- example data and output folder  
for scraping [SugarBind](https://sugarbind.expasy.org "リンク") and making ttl files.

## Steps to make integrated ttl file
### Step 0
create folders to store output files.

* glycovid_sugarbind
  * venv
  * scraping.py
  * ontology.owl
  * example_data    *[example data folder, storing csv files]*
  * example_output  *[example output folder, storing ttl files]*
  * data            ***[create this folder for storing csv files]***
  * output          ***[create this folder for storing ttl files]***
    
### Step 1
clone this project and then execute commands below
```
$cd glycovid_sugarbind
$python3 -m venv venv [if you are needed to create new virtualenv]
$. venv/bin/activate [if you are needed to switch to virtualenv]

[when you are required to install those]
$pip install requests, bs4, numpy, pandas

[execute python file]
$python3 scraping.py
```

### Step 2
make sure that csv files and ttl files would be created and stored in data and output folder respectively.

### Step 3
open ontology.owl file in your editor, and inserting ttl file content respectively.
- ***EXAMPLE Class Name [Class comment line in ontology.owl]***
- ReferencedInteraction class [line 1284] from referenced_interaction.ttl
- Pubmed class [line 1289] from pubmed.ttl
- Area class [line 1294] from area.ttl
- Agent class [line 1300] from agent.ttl
- Disease class [line 1306] from disease.ttl
- Lectin class [line 1312] from lectin.ttl
- Ligand class [line 1318] from ligand.ttl
- Structure class [line 1324] from structure.ttl

## Memo
Base ontology owl file was created on [Protege](https://protege.stanford.edu).

Required modules are **requests**, **bs4**, **numpy**, **pandas**.
