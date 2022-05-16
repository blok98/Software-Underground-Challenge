from netCDF4 import Dataset
from dbfread import DBF
import numpy as np

'''
--sources--
loading dbf files: https://dbfread.readthedocs.io/en/latest/#:~:text=DBF%20is%20a%20file%20format,jobs%20and%20one%2Doff%20scripts.
creating netcdf files: https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing/

--installations--
pip install netCDF4 / py -m pip install netCDF4
pip install dbfread / py -m pip install dbfread
'''


def load_Nazca(lst_atribute_names,path_to_data = "C:\\Users\\tom_s\\Desktop\\Minor\\SCD\\Data\\Nazca\\"):
    '''
    loads Nazca data (.dbf file)
    input:
        lst_atribute_names: list of atributes to be selected from Nazca data
        path_to_data: folder in which the Nazca datafile is stored (datafile is named "toetsingsresultaten_database.dbf") 
    output:
        lst: list of all records of type OrderedDict (format: OrderedDict([(<atribute>,<value>),]))
    '''
    # note, path name needs to end with \\ or /
    lst = []
    for record in DBF(path_to_data + "toetsingsresultaten_database.dbf"):
        relevant_record = {i:record[i] for i in record if i in lst_atribute_names}
        lst.append(relevant_record)
    return lst

def create_empty_netCDF(path_to_netCDF = "C:\\Users\\tom_s\\Desktop\\Minor\\SCD\\Data\\Nazca\\netCDF\\"):
    '''
    creates empty netCDF file under the name 'Nazca_netCDF.nc" in path=argument <path_to_netCDF>
    input:
        path_to_netCDF: folder in which empty netCDF file must be saved
    output:
        None
    '''
    try: ncfile.close()  # just to be safe, make sure dataset is not already open.
    except: pass
    ncfile = Dataset(path_to_netCDF+"Nazca_netCDF.nc",mode='w',format='NETCDF4_CLASSIC') 
    print(ncfile)

def open_netCDF(path_to_netCDF = "C:\\Users\\tom_s\\Desktop\\Minor\\SCD\\Data\\Nazca\\netCDF\\"):
    '''
    opens netCDF in append mode, meaning this ncfile can be used to be updated
    '''
    try: ncfile.close()  # just to be safe, make sure dataset is not already open.
    except: pass
    ncfile = Dataset(path_to_netCDF+"Nazca_netCDF.nc",mode='a',format='NETCDF4_CLASSIC') 
    return ncfile

def create_dimensions(ncfile, lst_atribute_names):
    '''
    Creating the limitation of the variables.
    dimension_length = 0 or None means it is not prefixed and can grow to infinity
    'A dimension is the minimum number of coordinates necessary to accurately describe a point in any given type of space'
    input:
        lst_atribute_names: list of all relevant atribute names in Nazca dbf datafile (list of strings)
        ncfile: netCDF file opened by 'open_netCDF', in append mode
    output:
        ncfile: ncfile with added dimensions and their atribute names
    '''
    for i in lst_atribute_names:
        dimension = ncfile.createDimension(i, 100) 
    for dim in ncfile.dimensions.items():
        print(dim)
    return ncfile

def create_variables(ncfile, Nazca_dbf_data):
    '''
    Creating the variables
    'A variable is just a placeholder for a quantity that's unknown or changing'
    '''
    ncfile_variables = []
    # we loop through a random record in Nazca data, which is a dictionary. For each key (atribute name) we assign a Variable with datatype = datatype(value (datapoint))
    for key in Nazca_dbf_data[0]:
        value = Nazca_dbf_data[0][key]
        datatype = type(value)
        var = ncfile.createVariable(key, datatype, (key,))
        ncfile_variables.append(var)
    return ncfile, ncfile_variables

def writing_data_to_netCDF(ncfile, ncfile_variables, Nazca_data_dbf):
    for index in range(len(ncfile_variables)):
        # we retrieve the ncfile variable object from ncfile_variables
        var = ncfile_variables[index]
        # now we can write all Nazca data from one specific field to 'var'. Nazca data is formatted in records, so we have to get a specific field value for each record.
        # we can do this by looping through Nazca data. Than we declare the desirable key, which is the field name corresponding to 'var' (so for index=0 it is the first field 'ID'). 
        # we can use this key to get the right value for one row. 
        var = np.array([Nazca_data_dbf[i][list(Nazca_data_dbf[0].keys())[index]] for i in range(len(Nazca_data_dbf))])
    return ncfile

def print_ncfile_variables(ncfile, field, limit=10):
    ds[field][:limit]

def create_metadata(ncfile):
    ncfile.title='My model data'
    return ncfile

# ncfile = open_netCDF()
# ncfile_dim = create_dimensions(ncfile,["ID","xcoord","ycoord"])
# print(ncfile_dim)
atribute_names = ["ID","XCOORD","YCOORD"]
dbffile = load_Nazca(atribute_names)
print(dbffile[:10])
create_empty_netCDF()
ncfile = open_netCDF()
ncfile = create_dimensions(ncfile, atribute_names)
ncfile, ncfile_variables = create_variables(ncfile, dbffile)
ncfile = writing_data_to_netCDF(ncfile,ncfile_variables,dbffile)
print_ncfile_variables(ncfile, "ID")
print(ncfile)