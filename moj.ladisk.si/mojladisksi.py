import numpy as np
import os
import json
from sys import getsizeof
import requests

ALLOWED_TYPES = ['str', 'int', 'float', 'ndarray', 'tuple', 'list', 'dict']
MAX_LEN = 15
MAX_SIZE = 10e3 #bit

int_type_names = [dtype.__name__ for dtype in np.signedinteger.__subclasses__() + np.unsignedinteger.__subclasses__()] + ['int']
float_type_names = [dtype.__name__ for dtype in np.floating.__subclasses__()] + ['float', 'Float', 'Zero']

def pripravi_resitev(answer):
    """
    The function prepares the solution for submission to the server.
    The naming of the keys is important when checking the answers - it should not be changed!
    The result is: tip                (all)
                   vrednost           (NOT ndarray)
                   dtype              (ndarray)
                   mean               (ndarray)
                   shape              (ndarray)
                   flat               (ndarray)
                   flat_size          (ndarray)
    """
    allowed_types = ', '.join(ALLOWED_TYPES)
    out = dict()

    type_name = type(answer).__name__

    if type_name in int_type_names:
        out['tip'] = 'int'
        out['vrednost'] = int(answer)
        return out

    elif type_name in float_type_names:
        out['tip'] = 'float'
        out['vrednost'] = float(answer)
        return out

    elif type_name in ['str', 'list', 'tuple', 'dict']:
        bit_size = getsizeof(answer)
        if bit_size < MAX_SIZE:
            out['tip'] = type_name
            out['vrednost'] = answer
            return out
        elif type_name in ['list', 'tuple'] and len(answer) > MAX_LEN:
            step = len(answer) // MAX_LEN + 1
            out['tip'] = type_name
            out['korak'] = step
            out['vrednost'] = answer[::step]
            return out
        else:
            raise Exception(f'Error: The submitted answer, with a size of {bit_size/1e3:5.2f} kb, exceeds the maximum allowed size {MAX_SIZE/1e3:5.2f} kb.')

    elif type_name in ['ndarray']:
        out.update(prepare_ndarray(answer))
        return out

    else:
        raise Exception('Error: result of type \'{0:s}\' does not match the expected types: {1:s}!'.format(type_name, allowed_types))


def prepare_ndarray(array, MAX_LEN=15):
    """
    Prepares a numpy.ndarray for submission - flatten, shorten to MAX_LEN, convert to a list
    and pack into a dict (tip:'ndarray', dtype, mean, shape, flat, flat_size).
    The naming of the keys is important when checking the answers - it should not be changed!
    """
    flat = array.flatten()
    inc = 1
    if len(flat) > MAX_LEN:
        inc = len(flat) // MAX_LEN + 1
        flat = flat[::inc]
    flat_list = flat.tolist()
    return {
        'tip': 'ndarray',
        'dtype': array.dtype.name,
        'mean': np.mean(array),
        'shape': array.shape,
        'flat': flat_list,
        'flat_size': len(flat_list),
        'korak': inc
    }


def data_to_json(object):
    """
    Prepares the passed object for JSON serialization. Used in the case when
    an error occurs during conversion of the object to JSON.
    """
    if isinstance(object, np.ndarray):
        return prepare_ndarray(object)

    if isinstance(object, complex):
        return (object.real, object.imag)

    if type(object).__name__ in int_type_names:
        return int(object)

    if type(object).__name__ in float_type_names:
        return float(object)

    raise TypeError(f'Error converting data of type {type(object)} to JSON. Check the submitted answer!')


def poslji(answer, id, st):
    """ The function sends the solution to the server.
    :param answer: variable holding the answer
    :param id: identification number of the problem
    :param st: sequential number of the answer
    """
    url = 'https://moj.ladisk.si/'
    client = requests.session()
    r = client.get(url + 'get_token')
    csrftoken = client.cookies['csrftoken']
    cookies = dict(client.cookies)
    headers = {'Content-type':'application/json', "X-CSRFToken":csrftoken, 'Referer':url}

    data = {
        'sa_id': id,
        'odgovor': pripravi_resitev(answer),
        'st': st,
       }

    json_data = json.dumps(data, default=data_to_json)

    r = requests.post(url + 'StudentData',
                        json=json_data, #json_data, if you need the default data_to_json function
                        headers=headers,
                        cookies=cookies)

    return r.json()['status']
