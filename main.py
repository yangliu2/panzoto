""" Create a environment to interact with the system """

from panzoto.portal import Portal
from panzoto.utils import display_logo


def menu() -> None: 
    """
    This will be the prompt for interacting with the environment
    command will be in the format of:
        <command> <arg1> <arg2> <arg...>
    """
    display_logo()
    portal = Portal()
    
    response = ""
    while response != 'exit':

        response = input("> ")

        words = response.split(' ')
        command = words[0]
        args = words[1:]
        
        try:
            if command.lower() in portal.commands:
                portal.commands[command](*args)
            elif command.lower() == 'exit':
                print(f"Later ya'll!")
            else:
                print(f'Cannot recognize command!') 
        except TypeError as e:
            print(f'Command format was wrong!')
            print(e)

    # save matrix
    portal.save_matrix()

def main():
    menu()


if __name__ == "__main__":
    main()