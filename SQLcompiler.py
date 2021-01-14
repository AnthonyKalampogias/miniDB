import re
from database import Database
import sys
from io import StringIO


def sqlCompiler(usrInput,db=None):   
    sanitizedUsrInput = usrInput.upper()
    # dataBase = db
    #Removes unnecessary  '', "", and ()
    sanitizedUsrInput = re.sub(re.compile('[^A-Za-z\s,*1234567890<>=]'), "", sanitizedUsrInput)
    # Splits the input in a list of 4 (so you can select the first 3 to determine what to do) i.e. create database/table etc
    args = sanitizedUsrInput.split(" ", 3)
    #The main principle is that you split the usrInput and see what combination of 1st, 2nd etc. elements matches the SQL syntax
    if args[0] == "CREATE":
        if args[1] == "DATABASE":
            try:
                if args[2] != "":
                    db = Database(args[2], load=False)
                    return(db, "Successfully created the db")
                    #,"Created database {}".format(args[2])
                else:
                    return("Please provide a name for your database")
            except:
                pass
        elif args[1] == "TABLE":
            if args[2] != "":
                #removes the (now unnecessary) first 2 elements 
                args.pop(0)
                args.pop(0)
                #takes the name of the table
                tableName = args.pop(0)
                args2 = ''.join(args)
                args2 = args2.split(',')
                #args2 now contains elements in the form 'fieldname datatype'
                newstr = ""
                fieldNames = []
                dataTypes = []
                #loops through args2 and splits the fieldnames and the datatypes in 2 different lists
                for x in args2:
                    newstr += x
                    args3 = newstr.split(' ')
                    fieldNames.append(args3[1])
                    dataTypes.append(args3[2])
                    newstr = ""
                #loops through datatypes and converts the varchar and int to their appropriate 'str' and 'int' counterparts
                for item in dataTypes:
                    if item == 'VARCHAR':
                        index = dataTypes.index(item)
                        dataTypes.remove(item)
                        dataTypes.insert(index, str)
                    elif item == 'INT':
                        index = dataTypes.index(item)
                        dataTypes.remove(item)
                        dataTypes.insert(index, int)
                    else:
                        pass
                #Sets as PK the FIRST column 
                db.create_table(tableName, fieldNames, dataTypes, fieldNames[0])
                return(db, "Successfully created the table")
                # return(db,"Successfully created the table")
            else:
                pass
        elif args[1] == "INDEX":
            if args[2] != "":
                try:
                    args.pop(0)
                    args.pop(0)
                    indexName = args.pop(0)
                    args2 = ''.join(args)
                    args2 =  args2.replace("ON ", "")
                    args3 = args2.split(" ")
                    tbName = args3[0]
                    db.create_index(tbName, indexName)
                    return(db,"Successfully created the index")
                except:
                    pass
        else:
            return(usrInput, " Is a wrong format")
    elif args[0] == "DROP":
        if args[1] == "DATABASE":
            if args[2] != "":
                #Again,you remove the first 2 elements and save the database name so you can use it to delete the db later
                try:
                    args.pop(0)
                    args.pop(0)
                    dbName = args.pop(0)
                    db.drop_db()
                    return(db,"Successfully dropped the database")
                except:
                    pass
            else:
                return("Wrong format")
        elif args[1] == "TABLE":
            if args[2] != "":
                #You save the name, you drop the table
                try:
                    args.pop(0)
                    args.pop(0)
                    tbName = args.pop(0)
                    db.drop_table(tbName)
                    return(db,"Successfully dropped the table")
                except:
                    pass
        else:
            pass
    elif args[0] == "SELECT":
        if args[1] == "*":
            #TODO maybe implement select with conditions, right now only supports the select all (*) 
            args.pop(0)
            args.pop(0)
            args.pop(0)
            tbName = args.pop(0)

            old_stdout = sys.stdout

            result = StringIO()

            sys.stdout = result

            db.select(tbName, '*')

            sys.stdout = old_stdout

            result_string = result.getvalue()

            #print(result_string)

            return(db, result_string)
            
        else:
            try:
                args.pop(0)
                leftTableName = args.pop(0)
                leftTableName = leftTableName.replace(",", "")
                rightTableName = args.pop(0)
                rightTableName = rightTableName.replace(",", "")
                newstr = args[0]
                args2 = newstr.split(" ")
                condition = args2[-1]
                # Does not work...
                db.inner_join(leftTableName, rightTableName, condition)
                return(db, "Successfully created the index")
            except:
                pass
    elif args[0] == "UPDATE":
        if args[1] !="":
            try:
                tbName = args[1]
                args.pop(0)
                args.pop(0)
                args.pop(0)
                newstr = ""
                newstr += args[0]
                temp = newstr.split("WHERE ")
                condition = temp[1]
                columnsAndValues = temp[0]
                listOfcolmnsAndVals = columnsAndValues.split(',')
                newstr = ""
                setColumns = []
                setValues = []
                args3 = []
                for i in listOfcolmnsAndVals:
                    newstr += i
                    newstr = newstr.replace(" ", "")
                    args3 = newstr.split('=')
                    setColumns.append(args3[0])
                    setValues.append(args3[1])
                    newstr = ""
                # Doesn't work for multiple values i.e. cant use the lists i have created.
                # Also, to change the values the condition must be the same column as the value you want to change
                # For example, if you want to change the personid from 10 to 15 the condition would be 'where personid > 2'
                # Still dont know how that works... 
                db.update(tbName, setValues[0], setColumns[0], condition)
                return(db, "Successfully updated the row(s)")
            except:
                pass
    elif args[0] == "INSERT":
        if args[1] == "INTO":
            try:
                args.pop(0)
                args.pop(0)
                #You take the table name
                tbName = args.pop(0)
                if tbName != "":
                    newstr = ""
                    newstr += args[0]
                    #All the values you want to insert you split them in a list so
                    #Right now the only supported way (by the database.py base code) is to insert a value in every column
                    newstr = newstr.replace("VALUES ", "")
                    newstr = newstr.replace(" ", "")
                    values = []
                    values = newstr.split(',')
                    db.insert(tbName, values)
                    return(db, "Successfully inserted the data")
            except:
                pass
            else:
                return(db,"Please provide a name for your table")
    elif args[0] == "DELETE":
        if args[2] != "":
            try:
                args.pop(0)
                args.pop(0)
                tbName = args.pop(0)
                #You take the name of the table you want to delete rows from
                conditions = args[0]
                conditions = conditions.replace("WHERE ", "")
                #You sanitize the conditions sting (the function takes input as 'id>10') thats why you take the "conditions" part as a hole string
                db.delete(tbName, conditions)
                return(db, "Successfully deleted the row(s)")
                #TODO if i use the equal ("=") in the condition part, it breaks... (no idea why)
            except:
                pass
    elif args[0] == "USE":
        if args[1] == "DATABASE":
            #In order to select something from a database you have to create a new db
            #No way to just select from an existing db, hence the need to "select" the desired db
            #It uses the same create function from database.py BUT the "load" flag is TRUE
            args.pop(0)
            args.pop(0)
            dbName = args.pop(0)
            if dbName != "":
                # return(db,type(dbName))
                # return(db,dbName)
                db = Database(dbName, load=True)
                return(db, "Loaded the database")
        else:
            return(db,"Wrong format")

    else:
        return(db,usrInput, " Is a wrong format")



# createdDB, msg = sqlCompiler("create database sampleData123456")

# print(msg)

# createdDB, msg = sqlCompiler("CREATE TABLE Persons7 ( PersonID int, LastName varchar, FirstName varchar, Hight int)", createdDB)

# print(msg)

# createdDB, samplestr = sqlCompiler("select * from persons", createdDB)

# print(samplestr)

# sqlCompiler("CREATE TABLE Persons ( PersonID int, LastName varchar, FirstName varchar, Hight int)", createdDB)


