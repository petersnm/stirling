import stirling

def do_sim(entity, *a):
    """ sim (Stirling Improvement Manager)

        sim is a commmand for interacting with the Stirling Improvement 
        Manager, a daemon which helps handle the decisions made to help 
        guide Stirling's development.

        There are various subcommands of SIM:
        proposals, help
    """
    if len(a) > 0:
        if len(a) == 1:
            if a[0] == 'help':
                entity.send(str(do_sim.__doc__))
                return
        elif len(a) == 2 and a[0] == 'help':
            entity.send('No help found for ' + str(a[1]) + '.')
            return
        elif len(a) >= 2:
            if a[1] == 'proposals':
                entity.send('The proposal system is being written.')
                return
    entity.send('Incorrect syntax; see \'help vacp\'.')
