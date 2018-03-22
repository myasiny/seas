#-*-coding:utf-8-*-
class DBTable:
    def __init__(self, name, columns, primary_key=None, foreign_keys_tuple=None, uniques=None, database=None, indexes=None):
        """
        Creates SQL query codes for creating a table in MySQL DBs.
        Also Can directly create table with Database param.
        :param name: string, name of table in database.
        :param columns: list of tuples; ( ColumnName, ColumnType, ColumnsSettings )
        :param primary_key: string, primary key column name
        :param foreign_keys_tuple: list of tuples, each foreign key as a tuple; ( ColumnName, referenceTable, referenceColumn)
        :param uniques: list of tuples, a tuple for a unique constraint; ( *ColumnNames )
        :param database: Database object, optional, for use direct table creation.
        """

        self.command = "CREATE TABLE %s ( " %name
        self.columns = columns
        self.name = name
        self.pk = primary_key
        self.foreign_keys = foreign_keys_tuple
        self.uniques = uniques
        self.db = database
        self.indexes = indexes

        for column in columns:
            self.command += "%s %s %s, " % column

        self.command = self.command[:len(self.command)-2] + " "

        if primary_key is not None:
            self.PrimaryKey(primary_key)

        if foreign_keys_tuple is not None:
            for foreign in foreign_keys_tuple:
                col = foreign[0]
                ref = foreign[1], foreign[2]
                behavior = foreign[3]
                self.ForeignKey(col, ref, behavior)

        if uniques is not None:
            for unique in uniques:
                self.Unique(unique)

        if indexes is not None:
            for index in indexes:
                self.Index(index)

        self.command = self.command + ");\n" if self.command != "" else ""
        print self.command
        self.db.execute(self.command)

    def PrimaryKey(self, column):
        self.command += ", primary key (%s)" % column

    def ForeignKey(self, column, referenceTuple, behavior):
        self.command += ", foreign key (%s) references %s (%s) %s" % (column, referenceTuple[0], referenceTuple[1], behavior)

    def Unique(self, columnTuple):
        if type(columnTuple) == tuple:
            self.command += ", Unique %s" % str(columnTuple).replace("\'", "")
        else:
            self.command += ", Unique (%s)" % columnTuple


    def Index(self, columnTuple):
        if type(columnTuple) == tuple:
            self.command += ", Index %s" % str(columnTuple).replace("\'", "")
        else:
            self.command += ", Index (%s)" % columnTuple

    def insert(self, key_values):
        """
        :param key_values: list of tuples, each tuple contains column nmae-value pairs, *( ColumnName, ColumnValue )
        :return: None
        """
        pass

    def get_command(self):
        return self.command

