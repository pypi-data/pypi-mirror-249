# mongo_operations: MongoDB Operations Simplified

*mongo_operations is a Python package designed to simplify common MongoDB operations. It provides an easy-to-use interface for interacting with MongoDB databases and collections. Whether you are inserting records, reading data, updating records, or performing bulk inserts, mongo_operations streamlines the process, making MongoDB operations straightforward.*

# Installation

Install the package using pip:

pip install PSKConnect==0.0.2

#  Usage

 ## Create an Instance of mongo_operation

   from mayyaDatabase import mongo_crud

   *Provide your MongoDB client URL and database name*
   mongo_op = mongo_crud.mongo_operation(client_url='your_mongo_client_url',database_name='your_database_name')

 ## Create a DataBase

   *Provide the name for your MongoDB collection*
   database = mongo_op.create_database()

 ## Create a Collection

   *Provide the name for your MongoDB collection*
   collection = mongo_op.create_collection(collection_name='your_collection_name')

 ## Insert Records

   *Insert a single record*
   record = {'key': 'value'}
   mongo_op.insert_record(record=record, collection_name='your_collection_name')

   *Insert multiple records*
   records = [{'key1': 'value1'}, {'key2': 'value2'}]
   mongo_op.insert_record(record=records, collection_name='your_collection_name')

 ## Read Records

   *Read all records from the collection*
   mongo_op.read_record(collection_name='your_collection_name')

 ## Delete Records

   *Provide a query to match records to be deleted*
   query = {'key': 'value'}
   mongo_op.delete_record(record=query, collection_name='your_collection_name')

 ## Update Records

   *Provide a query to match records to be updated and an update document*
   query = {'key': 'value'}
   update = {'$set': {'new_key': 'new_value'}}
   mongo_op.update_record(query=query, update=update, collection_name='your_collection_name')

 ## Bulk Insert from Data File

   *Provide the path to your data file (CSV or Excel)*
   data_file_path = 'path/to/your/datafile.csv'
   mongo_op.bulk_insert(datafile=data_file_path, collection_name='your_collection_name')

## Contributors

### SAIKIRANPATNANA


