""" Matrix object to create the world """

from uuid import UUID
from panzoto.person import Person
from panzoto.baby import Baby
from panzoto.food import Food
from panzoto.thing import Thing
from panzoto.utils import log_output, log
from panzoto.enums import Logging


class Matrix():

    def __init__(self):
        self.people_dict = {}
        self.thing_dict = {}

    @staticmethod
    def get_full_name(first_name: str,
                      last_name: str) -> str:
        """Generate the name of the person as a continous string

        Args:
            first_name (str): first name
            last_name (str): last name

        Returns:
            str: full name in continous string
        """
        return f'{first_name.capitalize()}_{last_name.capitalize()}'

    @log_output
    def create_person(self,
                      first_name: str,
                      last_name: str) -> str:
        """create a person using first and last name

        Args:
            first_name (str): first name    
            last_name (str): last name

        Returns:
            str: all the output in from the function
        """

        output = ""

        person = Person(first_name, last_name)
        output += f'{person.name} created.'
        self.people_dict[person.uid] = person

        return output

    @log_output
    def delete_person(self,
                      uid: str) -> str:
        """Remove a person from the matrix using uid string

        Args:
            uid (str): uuid string

        Returns:
            str: output from this function
        """

        output = ""

        try:
            uid = UUID(uid)
        except ValueError:
            log(text=f"Maybe try a valid uuid?",
                level=Logging.ERROR.value)
            return output

        if uid in self.people_dict:
            output += f"{self.people_dict[uid].name} have been removed!"
            del self.people_dict[uid]
        else:
            output += 'That person does not exist!'

        return output

    @log_output
    def create_baby(self) -> str:
        """Create a baby based on Baby class settings

        Returns:
            str: output string
        """
        output = ""
        baby = Baby()
        self.people_dict[baby.uid] = baby

        return output

    @log_output
    def list_people(self) -> str:
        """List all the people in Matrix

        Returns:
            str: output string
        """
        output = ""
        if not self.people_dict:
            output += 'No people exist.'

        for person in self.people_dict:
            output += f'{self.people_dict[person].name}\n'

        return output

    @log_output
    def show_person(self,
                    first_name: str,
                    last_name: str) -> str:
        """Show info about a specific person

        Args:
            first_name (str): first name
            last_name (str): last name

        Returns:
            str: output of this function
        """
        output = ""
        name = self.get_full_name(first_name=first_name,
                                  last_name=last_name)
        target_list = [str(self.people_dict[x]) for x in self.people_dict
                       if name == self.people_dict[x].full_name]

        if target_list:
            output += "\n".join(target_list)
        else:
            output += f'Cannot find the person you are searching.'

        return output

    def assign_item(self,
                    thing_uid: str,
                    person_uid: str) -> str:
        """Assign an item to a person

        Args:
            thing_uid (str): item uid
            person_uid (str): person uid

        Returns:
            str: output string
        """

        output = ""

        thing_uid = UUID(thing_uid)
        person_uid = UUID(person_uid)

        # only assing item if both item and person exisit
        if (person_uid in self.people_dict) and (thing_uid in self.thing_dict):
            person_object = self.people_dict[person_uid]
            thing_object = self.thing_dict[thing_uid]
            thing_object.owner = person_object.uid
            person_object.possession.append(thing_object)
            person_object.check_status()
            thing_object.check_status()
        # error messages if either peron or item doesn't exist
        elif (person_uid in self.people_dict) and \
            (thing_uid not in self.thing_dict):
            output += "That thing doesn't exist!"
        elif (person_uid not in self.people_dict) and \
            (thing_uid in self.thing_dict):
            output += "That person doesn't exist!"
        else:
            output += "Neither that person nor the thing exist!"

        return output

    @log_output
    def create_food(self,
                    name: str,
                    value: str) -> str:
        """Create a new food item

        Args:
            name (str): name of the food time
            value (str): how many times can the item be eaten

        Returns:
            str: output string
        """
        output = ""

        food = Food(name=name,
                    value=int(value))
        output += f'{food.name} created.'
        self.thing_dict[food.uid] = food

        return output

    @log_output
    def show_thing(self,
                   name: str) -> str:
        """Show info about a specific thing

        Args:
            name (str): name of item

        Returns:
            str: output of this function
        """
        output = ""
        name = name.capitalize()
        target_list = [str(self.thing_dict[x]) for x in self.thing_dict
                       if name == self.thing_dict[x].name]

        if target_list:
            output += "\n".join(target_list)
        else:
            output += f'Cannot find the thing you are searching.'

        return output

    @log_output
    def focus(self, *args) -> str:
        """Display stats about either a person or a thing

        Returns:
            str: output string 
        """
        output = ""
        if len(args) == 1:
            self.show_thing(*args)
        elif len(args) == 2:
            self.show_person(*args)
        else:
            output += "The thing to focus is neither a person or a thing."

    @log_output
    def remove_item_possession(self,
                               uid: UUID) -> str:
        """Remove the owner's possession of the given item

        Args:
            uid (UUID): uid of the thing for deletion

        Returns:
            str: output string
        """
        output = ""
        thing_object = self.thing_dict[uid]
        if thing_object.owner:
            owner_uid = thing_object.owner
            person = self.people_dict[owner_uid]
            person.possession.remove(thing_object)
        else:
            output += f"{thing_object.name} was not owned by anybody!"
        del self.thing_dict[uid]

        return output

    @log_output
    def delete_thing(self,
                     thing_id: str) -> str:
        """Remove a thing from the matrix

        Args:
            thing_id (str): uid of item

        Returns:
            str: output string
        """
        output = ""

        try:
            uid = UUID(thing_id)
        except ValueError:
            log(text=f"Maybe try a valid uuid?",
                level=Logging.ERROR.value)
            return output

        if uid in self.thing_dict:
            self.remove_item_possession(thing_object=self.thing_dict[uid],
                                        uid=uid)
        else:
            output += 'That thing does not exist!'

        return output

    @log_output
    def list_thing(self) -> str:
        """List all the items in matrix

        Returns:
            str: output string
        """

        output = ""
        if not self.thing_dict:
            output += f"Nothing exisit yet."

        for thing in self.thing_dict:
            thing_object = self.thing_dict[thing]
            output += thing_object.name + "\n"

        return output

    @log_output
    def run_n_turn(self,
                   num: int) -> None:
        """run n number of turns for a world simulation

        Args:
            num (int): number of iterations
        """
        output = ""
        output += f'Iter: {num} turns.'

        for _ in range(int(num)):
            self.run_one_turn()

        return output

    @log_output
    def check_people(self) -> str:
        """Update all the person object in maxtrix

        Returns:
            str: output string
        """
        output = ""
        for key in list(self.people_dict):
            person_object = self.people_dict[key]

            person_object.run_one_turn()

            if not person_object.alive:
                self.delete_person(uid=person_object.uid)
                output += f'{person_object.name} died.'
        return output

    @log_output
    def check_things(self) -> str:
        """Update all the item object in matrix

        Returns:
            str: output string
        """
        output = ""
        for key in list(self.thing_dict):
            item_object = self.thing_dict[key]

            if item_object.value <= 0:
                del self.thing_dict[key]

                owner = item_object.owner
                owner.possession.remove(item_object)
                owner.check_status()
        return output

    def run_one_turn(self) -> None:
        """Calculate all the changes in one turn"""
        self.check_people()
        self.check_things()