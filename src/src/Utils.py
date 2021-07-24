import _pickle as cPickle

def copySimulation(simulation):
    return cPickle.loads(cPickle.dumps(simulation, -1))
#   return copy.deepcopy(simulation)

def get_printable_action(action):
    if action.type.name == "MOVE":
        return (action.source_cell.get_position(), action.target_cell.get_position(), action.type)
    elif action.type.name == "EXTRACT":
        return (action.source_cell.get_position(), "-", action.type)
    elif action.type.name == "END":
        return ("-", "-", action.type)