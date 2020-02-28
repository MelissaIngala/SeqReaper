open_art = """                ...                            
             ;::::;                           
           ;::::; :;                          
         ;:::::'   :;                         
        ;:::::;     ;.                        
       ,:::::'       ;           OOO\         
       ::::::;       ;          OOOOO\        
       ;:::::;       ;         OOOOOOOO       
      ,;::::::;     ;'         / OOOOOOO      
    ;:::::::::`. ,,,;.        /  / DOOOOOO    
  .';:::::::::::::::::;,     /  /     DOOOO   
 ,::::::;::::::;;;;::::;,   /  /        DOOO  
;`::::::`'::::::;;;::::: ,#/  /          DOOO 
:`:::::::`;::::::;;::: ;::#  /            DOOO
::`:::::::`;:::::::: ;::::# /              DOO
`:`:::::::`;:::::: ;::::::#/               DOO
 :::`:::::::`;; ;:::::::::##                OO
 ::::`:::::::`;::::::::;:::#                OO
 `:::::`::::::::::::;'`:;::#                O 
  `:::::`::::::::;' /  / `:#                  
   ::::::`:::::;'  /  /   `#              
 
   ____         ___                       
  / __/__ ___ _/ _ \___ ___ ____  ___ ____
 _\ \/ -_) _ `/ , _/ -_) _ `/ _ \/ -_) __/
/___/\__/\_, /_/|_|\__/\_,_/ .__/\__/_/   
          /_/             /_/             

          Melissa Ingala
               2018
"""

print(open_art)
from Bio import Entrez
from Bio import SeqIO
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def enter_email(email):
  """This function sets your email address for NCBI access"""
  Entrez.email = email

print("\nEnter your email:")
email = input()
enter_email(email)
print("\nEmail successfully set")

print("\nPlease choose your database")
options = ["nucleotide", "EST", "protein"]

# Print out your database options
for i in range(len(options)):
    print(str(i+1) + ":", options[i])

# Take user input and get the corresponding item from the list
db = int(input("Enter a number: "))
if db in range(1, 5):
    db = options[db-1]
else:
    print("Invalid input!")

print("\nPlease type your search terms (separated by AND/OR)")
term = input()

search_handle = Entrez.esearch(db=db,term=term, idtype="acc",usehistory="n")

def ncbi_search(db, term, idtype="acc",usehistory="n"):
  """This function searches NCBI for records matching your query terms. idtype and usehistory set by default"""
  print("\nSearching database for sequences...")
  global search_handle
  search_handle = Entrez.esearch(db=db,term=term, idtype="acc",usehistory="n")
  print("\nTabulating search handle...")

ncbi_search(db, term)

search_results = Entrez.read(search_handle)
search_handle.close()
print("\nSearch Completed.")

print("\nPlease name the out_handle file here (eg. AllSeqs.gb)")
out_handle_name = input()

gi_list = search_results["IdList"]
count = int(search_results["Count"])
a = open("Numfile.txt", "a+")
a.write("The number of sequence files are :")
a.write(str(count))
a.write("\n")
a.close()
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]
batch_size = 500
out_handle = open(out_handle_name, "w")

try:
  for start in range(0,count,batch_size):
    end = min(count, start+batch_size)
    print("Now downloading record %i to %i" % (start+1, end))
    fetch_handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", retstart=start, retmax=batch_size, webenv=webenv, query_key=query_key)
    data=fetch_handle.read()
    fetch_handle.close()
    out_handle = open(out_handle_name, "w+")
    out_handle.write(data)
  print("Done. Downloaded %i records" % count)
except urllib2.HTTPError as err:
   if err.code == 502:
       print("\nHTTP Error 502: Bad Gateway. Try again later during less busy (USA 0900-1700 hrs) time")
   else:
       raise
out_handle.close()

#Using SeqIO, translate the files to FASTA format
from Bio import SeqIO

with open(out_handle_name) as input_handle:
    with open("seqs.fasta", "w+") as output_handle:
        sequences = SeqIO.parse(input_handle, "genbank")
        count = SeqIO.write(sequences, output_handle, "fasta")
print("\nConverted %i records to fasta" % count)
