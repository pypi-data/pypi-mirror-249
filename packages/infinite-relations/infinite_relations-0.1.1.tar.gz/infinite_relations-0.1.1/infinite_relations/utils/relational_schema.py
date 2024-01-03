class RelationalSchema:
    """Class providing static functions for work with relational schemas in the form of lists"""

    def cross(l_schema: list, r_schema: list) -> list:
        """Creates a new schema for cross join of relations

        Parameters
        ----------
        l_schema : list
            A list of attribute names
        r_schema : list
            Another list of attribute names

        Returns
        -------
        list
            Combined list of attribute names, duplicate attributes are renamed and kept
        """
        new_schema: list = l_schema.copy()
        for attr in r_schema:
            if attr in new_schema:
                unique_name = RelationalSchema.get_unique_attr_name(attr, new_schema)
                new_schema.append(unique_name)
            else:
                new_schema.append(attr)
        return new_schema

    def join(l_schema: list, r_schema: list) -> (list, list):
        """Creates a new schema for natural join of relations

        Parameters
        ----------
        l_schema : list
            A list of attribute names
        r_schema : list
            Another list of attribute names

        Returns
        -------
        (list, list)
            Tuple containing a joined schema and a list of common attributes
        """
        new_schema = l_schema.copy()
        common_attrs: list = []
        for attr in r_schema:
            if attr in new_schema:
                common_attrs.append(attr)
            else:
                new_schema.append(attr)
        return (new_schema, common_attrs)

    def print(schema: list):
        """Prints attribute names in a line separated by spaces

        Parameters
        ----------
        schema : list
            A list of attribute names to print
        """
        for attr in schema:
            print(attr, end=" ")
        print("")

    def get_unique_attr_name(attr_name: str, attr_names: list) -> str:
        """Creates a new attribute name not contained in a list of names by appending '

        Parameters
        ----------
        attr_name : str
            Non-unique attribute name
        attr_names : list
            List of attribute names to check uniqueness

        Returns
        -------
        str
            Unique attribute name
        """
        new_name = attr_name
        while new_name in attr_names:
            new_name += "'"
        return new_name
