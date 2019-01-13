# -*-coding:utf-8-*-
class DBTable:
    def __init__(self, name, columns, primary_key=None, foreign_keys_tuple=None,
                 uniques=None, database=None, indexes=None):
        """
        Creates SQL query codes for creating a table in MySQL DBs.
        Also Can directly create table with Database param.
        :param name: string, name of table in database.
        :param columns: list of tuples; ( ColumnName, ColumnType, ColumnsSettings )
        :param primary_key: string, primary key column name
        :param foreign_keys_tuple: list of tuples, each foreign key as a tuple;
                (ColumnName, referenceTable, referenceColumn)
        :param uniques: list of tuples, a tuple for a unique constraint; ( *ColumnNames )
        :param database: Database object, optional, for use direct table creation.
        """

        self.command = "CREATE TABLE %s ( " % name
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
            self.primary_key(primary_key)

        if foreign_keys_tuple is not None:
            for foreign in foreign_keys_tuple:
                col = foreign[0]
                ref = foreign[1], foreign[2]
                behavior = foreign[3]
                self.foreign_key(col, ref, behavior)

        if uniques is not None:
            for unique in uniques:
                self.unique(unique)

        if indexes is not None:
            for index in indexes:
                self.index(index)

        self.command = self.command + ");\n" if self.command != "" else ""
        print self.command
        self.db.execute(self.command)

    def primary_key(self, column):
        self.command += ", primary key (%s)" % column

    def foreign_key(self, column, reference_tuple, behavior):
        self.command += ", foreign key (%s) references %s (%s) %s" \
                        % (column, reference_tuple[0], reference_tuple[1], behavior)

    def unique(self, column_tuple):
        if type(column_tuple) == tuple:
            self.command += ", unique %s" % str(column_tuple).replace("\'", "")
        else:
            self.command += ", unique (%s)" % column_tuple

    def index(self, column_tuple):
        if type(column_tuple) == tuple:
            self.command += ", index %s" % str(column_tuple).replace("\'", "")
        else:
            self.command += ", index (%s)" % column_tuple

    def insert(self, key_values):
        """
        :param key_values: list of tuples, each tuple contains column nmae-value pairs, *( ColumnName, ColumnValue )
        :return: None
        """
        pass

    def get_command(self):
        return self.command

