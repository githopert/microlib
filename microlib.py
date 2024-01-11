""" `microlib` is a script that implements a digital Zettelkasten.

author: fat_fox
creation date: 31-Aug-2021
last modified: 11-Jan-2024
"""
import argparse
import json
import os
from random import randrange


# Globals ------------------------------------------------------------ #
C_NAME_SYMBOLS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    '1234567890')
C_NAME_LENGTH = 20
C_SETTINGS_FILE_NAME = 'microlib_settings.json'


class MicroLibrary:
    """ A primitive implementation of a digital zettelkasten. """

    def __init__(self):
        self.settings = None

        with open(C_SETTINGS_FILE_NAME, 'r', encoding='utf-8') as r:
            self.settings = json.load(r)

    # ---------------------------------------------------------------- #
    # PUBLIC METHODS
    # ---------------------------------------------------------------- #
    def find_cards(self, args: argparse.Namespace) -> None:
        """ Searches for an index card using the specified arguments. """
        relevant_cards = []

        if (args.date == '' and args.number == '' and args.reference == ''
            and args.type == '' and args.words == ''):
            print('No arguments => Nothing to do.')
            return

        # Searching for cards in the current directory
        for file in os.listdir(self.settings['cards_dir']):
            if not os.path.splitext(file)[1] == '.txt':
                continue

            card_full_path = os.path.join(
                self.settings['cards_dir'], file)
            
            checks = [False] * 5
            checked = [False] * 5

            with open(card_full_path, 'r', encoding='utf-8') as rf:
                # Reading the header of the file
                current_number = rf.readline().strip('\n')
                current_references = rf.readline().strip('\n')
                current_date = rf.readline().strip('\n')
                current_type = rf.readline().strip('\n')
                current_body = " ".join(
                    [l.strip('\n') for l in rf.readlines()
                    if l.strip('\n') != '']
                )

            # Reading the header of the file
            if args.number.strip() != '':
                checks[0] = self._compare_card_number(
                    args.number.strip(), current_number)
                checked[0] = True

            if args.reference.strip() != '':
                checks[1] = self._compare_card_references(
                    args.reference.strip(), current_references)
                checked[1] = True

            # Date
            if args.date.strip() != '':
                checks[2] = self._compare_card_date(
                    args.date.strip(), current_date)
                checked[2] = True

            # Type
            if args.type.strip() != '':
                checks[3]= self._compare_card_type(
                    args.type.strip(), current_type)
                checked[3] = True

            # Reading the rest of the file
            if args.words.strip() != '':
                checks[4] = self._compare_words(args.words, current_body)
                checked[4] = True

            # Accept or reject this card
            if True in checks and checks == checked:
                relevant_cards.append(
                    '{:<12} | {:<22}'.format(current_number, file)
                )

        self._print_card_list(relevant_cards)

    def generate_card_name(self) -> str:
        """ Generates a name for the new index card. """
        new_name = ""

        while len(new_name) < C_NAME_LENGTH:
            new_name += C_NAME_SYMBOLS[randrange(0, len(C_NAME_SYMBOLS)) - 1]
        
        return new_name + '.txt'

    # ---------------------------------------------------------------- #
    # PRIVATE METHODS
    # ---------------------------------------------------------------- #
    def _compare_card_date(self, input_date: str, card_date: str) -> bool:
        """ Compares the date in the string with the specified date. """
        return input_date == card_date[:len(input_date)]

    def _compare_card_number(self, input_number: str, card_number: str) -> bool:
        """ Compares the card number with the specified number. """
        return (
            False 
            if len(input_number) > len(card_number)
            else card_number[:len(input_number)] == input_number
        )

    def _compare_card_references(self, input_reference: str,
                                card_references: str) -> bool:
        """ Checks if the reference is cited in the index card. """
        return input_reference in card_references.split('/')
    
    def _compare_card_type(self, input_type: str, card_type: str):
        """ Checks the type of the given card. """
        return input_type == card_type

    def _compare_words(self, input_words: str, card_body: str) -> bool:
        """ Checks if the specified words are in the index card body. """
        return input_words.lower() in card_body.lower()

    def _print_card_list(self, card_list: list) -> None:
        """ Prints the specified list of index cards. """
        if len(card_list) > 0:
            print('{:<5} {:<12} | {:<22}'.format('#.', 'card number', 'card file'))
            print('-' * 40)

            for i, card_file_name in enumerate(sorted(card_list)):
                print(f'{str(i + 1) + ".":<5} {card_file_name}')
        else:
            print('Nothing was found!')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='`microlib v0.1` - searching'
        ' for an index card in the specified directory. To select the '
        'directory, modify the file `microlib_settings.json`')
    
    # Search arguments
    parser.add_argument('-n', dest='number', default='', type=str,
                        help='an index card number. Example: 1_111_a_2')
    parser.add_argument('-r', dest='reference', default='', type=str,
                        help='references in card. Example: 1_1/1_111_2/0')
    parser.add_argument('-d', dest='date', default='', type=str,
                        help='a creation date in the YYYYMMDD-format. '
                        'Example: 20210831')
    parser.add_argument('-t', dest='type', default='', type=str,
                        help='n - for notes, a - for auxiliary cards, ' +
                        's - for summaries.')
    parser.add_argument('-w', dest='words', default='', type=str,
                        help='keywords. Example: INDEX')
    # Card manipulation arguments
    parser.add_argument('--generate', dest='generate',
                        action='store_true', help='generates a new card')
 
    args = parser.parse_args()
    microlib = MicroLibrary()
    card_dir = microlib.settings['cards_dir']
    editor = microlib.settings['editor']

    if not os.path.exists(card_dir):
        os.makedirs(card_dir)

    if args.generate:
        new_name = microlib.generate_card_name()
        print("Creating the file: " + os.path.join(card_dir, new_name))
        os.system(editor + ' ' + os.path.join(card_dir, new_name))
    else:
        microlib.find_cards(args)
