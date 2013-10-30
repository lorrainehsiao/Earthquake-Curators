import sys
import urllib
import os
import pandas as pd

def download_extract_data(src_url,file_name, extract_dir):
    '''
    Given a src_url, downloads the archived earthquake data.
    Then, extracts the data into the extract_dir. 
    Will create extract_dir if it doesn't exist.
    '''
    print "Download initialized"
    urllib.urlretrieve(src_url, file_name)
    print "Download complete"

    #create the directory, if it doesn't exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    #tar into the target file
    os.system("tar -xvzf %s -C %s" % (file_name, extract_dir))
    print "extracted data into %s" % extract_dir

    #moving the downloaded file into the extract_dir
    os.system("mv %s %s" % (file_name, extract_dir))


def get_catalog_dict(catalog_dir):
    ''' 
    Given a directory, dict of  *.catalog in the directory.
    Includes RELATIVE location of the file, as well as the name.
    dict <K,V> format of <relative_path_dir+file_name, file_name>
    Will traverse sub-directories.
    example:
    {"temp/SCEC_DC/1999.catalog":"1999.catalog"}
    '''
    catalogs = {}
    for curdir, dirs, files in os.walk(catalog_dir):
        for check_file in files:
            if '.catalog' in check_file: #TODO change to regex to make fancy
                catalogs[os.path.join(curdir,check_file)] = check_file
    return catalogs

def parse_and_output(catalog_dict, output_dir, format):

    #create the directory, if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for catalog_path, catalog_name in catalog_dict.items():
        if format == "csv":
            output_csv(catalog_path, catalog_name, output_dir)
            break #TODO REMOVE
        else:
            raise ValueError("Undefined format: '%s'" % format)

def output_csv(catalog_path, catalog_name, output_dir):
    '''
    Given the path and the name of the catalog,
    Outputs the catalog into output_dir.
    '''
    head_size = 0 
    f = open(catalog_path, 'r')
    #figure out how many lines to skip!
    for line in f:
        if line.startswith("#"):
            head_size += 1
        else:
            break

    skip_length = head_size-1
    head_row_loc = head_size-2

    data_frame = pd.read_csv(catalog_path, header=head_row_loc, skiprows=skip_length, delimiter=r"\s+")
    #data_frame.rename(columns={"#YYY/MD/DD": "YYYY/MD/DD"}, inplace=True)
    data_frame.rename(columns=lambda x: x.replace("#", ""), inplace=True)
    #TODO: this replacing of hash-tag is a bit weird, fix later.
    #print data_frame.columns
    data_frame.to_csv(os.path.join(output_dir, catalog_name+".csv"), index = False)


target_catalogs =  get_catalog_dict('temp/')

parse_and_output(target_catalogs, 'clean_data', 'csv')

sys.exit()


#url= 'http://www.data.scec.org/ftp/catalogs/SCEC_DC/SCEDC_catalogs.tar.gz'
#file_name = 'SCED_catalogs.tar.gz'



SCSN= 'http://www.data.scec.org/ftp/catalogs/SCSN/SCSN_catalogs.tar.gz'
file_name = 'SCSN_catalogs.tar.gz'

dirty_dir = "dirty_data"
clean_dir = "clean_data"
download_extract_data(url,file_name, dirty_dir)
target_catalogs =  get_catalog_list(dirty_dir)
parse_and_output(catalog_dict, clean_dir, 'csv')
