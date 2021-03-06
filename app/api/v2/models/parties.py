# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class PartiesModel:
    """
        v2 parties model
    """

    def __init__(self, name, hqAddress, logoUrl):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def save_party(self):
        """
        Add a new party to db
        """
        save_party_query = """
        INSERT INTO parties(name, hqAddress, logoUrl) VALUES(
            '{}', '{}', '{}'
        ) RETURNING id;""".format(self.name, self.hqAddress, self.logoUrl)
        return db.queryData(save_party_query, True)

    @staticmethod
    def formatParties(iterable):
        """
            This function will help in formatting the parties data 
            in a record format
        """
        data = []
        for party in iterable:
            formattedparty = {'id': party[0],
                              'name': party[1],
                              'hqAddress': party[2],
                              'logoUrl': party[3]}
            data.append(formattedparty)
        return data

    @staticmethod
    def get_all_parties():
        """
            Get all parties from the database.
        """
        get_all_parties_query = """
        SELECT id, name, hqAddress, logoUrl FROM parties
        """
        return PartiesModel.formatParties(db.select_data_from_db(get_all_parties_query))

    @staticmethod
    def get_specific_party(party_id):
        """
            This method gets to select a specific PARTY
            which matches the id provided in the function args
        """
        select_single_party = """
        SELECT id, name, hqAddress, logoUrl FROM parties
        WHERE parties.id = '{}'""".format(party_id)

        return PartiesModel.formatParties(db.select_data_from_db(select_single_party))

    @staticmethod
    def update_specific_party(name, party_id):
        """
            This method gets a party by Id and updates it.
        """
        update_party = """
        UPDATE parties SET name = '{}' WHERE parties.id = '{}'
        """.format(name, party_id)

        db.queryData(update_party)

    @staticmethod
    def delete_specific_party(party_id):
        """
        This method deletes a party by its Id
        from the db parties table.
        """
        delete_query = """
        DELETE FROM parties
        WHERE parties.id = '{}'""".format(party_id)

        db.queryData(delete_query)
