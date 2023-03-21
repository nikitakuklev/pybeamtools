def sd(d):
    status_dict = {'disable': 0, 'enable': 0, 'read': 0, 'read_now': 0, 'scan': 0, 'update': 0,
                   'write': 0,
                   }
    status_dict.update(d)
    return status_dict
