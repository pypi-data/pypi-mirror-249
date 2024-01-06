# -*- coding: utf-8 -*-
"""
The `field` module is part of the `tab-dataset` package.

It contains the classes `Sfield` and `Nfield` for Field entities.

For more information, see the 
[user guide](https://loco-philippe.github.io/tab-dataset/docs/user_guide.html) 
or the [github repository](https://github.com/loco-philippe/tab-dataset).
"""
from copy import copy
import json

from json_ntv.ntv import Ntv, NtvSingle
from json_ntv.ntv_util import NtvJsonEncoder

from tab_dataset.field_interface import FieldInterface
from tab_dataset.cfield import Cfield, FieldError, Cutil

DEFAULTINDEX = '$default'


class Sfield(FieldInterface, Cfield):
    '''
    `Sfield` is a child class of `Cfield` where internal value can be different
    from external value (list is converted in tuple and dict in json-object).

    Attributes are the same as Cfield class

    The methods defined in this class are :

    *constructor (@classmethod)*

    - `Cfield.bol`
    - `Cfield.from_ntv`
    - `Cfield.ntv`
    - `Cfield.like`
    - `Sfield.merging`

    *conversion (@staticmethod)*

    - `Sfield.l_to_i`
    - `Sfield.s_to_i`
    - `Sfield.l_to_e`
    - `Sfield.s_to_e`
    - `Sfield.i_to_n`
    - `Sfield.n_to_i`
    - `Sfield.i_to_name`
    - `Cfield.ntv_to_val` (@classmethod)
    
    *dynamic value (getters @property)*

    - `Sfield.val`
    - `Sfield.cod`
    - `Cfield.hashf`
    - `Cfield.to_analysis`
    - `Cfield.values`
    - `Cfield.codec`
    - `Cfield.infos`
    - `Cfield.keys`
    
    *add - update methods*

    - `Sfield.append`
    - `Sfield.setcodecvalue`
    - `Sfield.setcodeclist`
    - `Sfield.setlistvalue`
    - `Sfield.setvalue`
    - `Cfield.add`
    - `Cfield.setname`
    - `Cfield.set_keys`
    - `Cfield.set_codec`
    - `Cfield.setkeys`

    *transform methods*

    - `Cfield.coupling`
    - `Cfield.extendkeys`
    - `Cfield.full`
    - `Cfield.reindex`
    - `Cfield.reorder`
    - `Cfield.sort`
    - `Cfield.tocoupled`
    - `Cfield.tostdcodec`
    
    *getters methods*

    - `Sfield.isvalue`
    - `Sfield.keytoval`
    - `Sfield.loc`
    - `Sfield.recordfromvalue`
    - `Sfield.valtokey`
    - `Cfield.couplinginfos`
    - `Cfield.derkeys`
    - `Cfield.getduplicates`
    - `Cfield.iscrossed`
    - `Cfield.iscoupled`
    - `Cfield.isderived`
    - `Cfield.islinked`
    - `Cfield.iskeysfromderkeys`
    - `Cfield.recordfromkeys`

    *export methods (`observation.field_interface.SfieldInterface`)*

    - `Sfield.json`
    - `Sfield.to_obj`
    - `Sfield.to_dict_obj`
    - `Sfield.to_numpy`
    - `Sfield.to_pandas`
    - `Sfield.vlist`
    - `Sfield.v_name`
    - `Sfield.vSimple`
    '''

    def __init__(self, codec=None, name=None, keys=None,
                 lendefault=0, reindex=False, fast=False):
        '''
        Sfield constructor.

        *Parameters*

        - **codec** :  list (default None) - external different values of index (see data model)
        - **keys** :  list (default None)  - key value of index (see data model)
        - **name** : string (default None) - name of index (see data model)
        - **lendefault** : integer (default 0) - default len if no keys is defined
        - **reindex** : boolean (default True) - if True, default codec is apply
        - **fast**: boolean (default False) - if True, codec is created without conversion'''
        if isinstance(codec, Sfield):
            Cfield.__init__(self, copy(codec._codec),
                            copy(codec.name), copy(codec._keys))
            return
        if codec is None:
            codec = []
        if not isinstance(codec, list):
            codec = [codec]
        leng = lendefault
        if codec and len(codec) > 0 and not leng:
            leng = len(codec)
        if not keys is None:
            leng = len(keys)
        if not name:
            name = DEFAULTINDEX
        if not (keys is None or isinstance(keys, list)):
            raise FieldError("keys not list")
        if keys is None and leng == 0:
            keys = []
        elif keys is None:
            keys = [(i*len(codec))//leng for i in range(leng)]
        if codec == []:
            keysset = Cutil.tocodec(keys)
            codec = self.l_to_i(keysset, fast=True)
        codec = self.l_to_i(codec, fast=fast)
        Cfield.__init__(self, codec, name, keys, reindex=reindex)

    def __setitem__(self, ind, item):
        ''' modify values item'''
        if isinstance(ind, slice):
            start, stop, step = ind.start or 0, ind.stop or len(self), ind.step or 1
            idxt = list(iter(range(start, stop, step)))
            if len(idxt) != len(item):
                raise FieldError("item length not consistent")
            self.setlistvalue(item, idxt, extern=True)
        elif ind < 0 or ind >= len(self):
            raise FieldError("out of bounds")
        else: 
            self.setvalue(ind, item, extern=True)

    def __str__(self):
        '''return json string format'''
        return str({self.name: self.l_to_e(self.values)})
        # return '    ' + self.to_obj(encoded=True, modecodec='full', untyped=False) + '\n'

    @classmethod
    def merging(cls, listidx, name=None):
        '''Create a new Field with values are tuples of listidx Field values

        *Parameters*

        - **listidx** : list of Field to be merged.
        - **name** : string (default : None) - Name of the new Field

        *Returns* : new Field'''
        if not name:
            name = str(list({idx.name for idx in listidx}))
        values = Cutil.transpose([idx.values for idx in listidx])
        return cls.ntv({name: values})

    @staticmethod
    def l_to_i(lis, fast=False):
        ''' converting a list of external values to a list of internal values'''
        if fast:
            return lis
        return [Sfield.s_to_i(val, fast) for val in lis]

    @staticmethod
    def s_to_i(val, fast=False):
        '''converting an external value to an internal value'''
        if fast:
            return val
        if val is None or isinstance(val, bool):
            return json.dumps(val)
        if isinstance(val, list):
            return Cutil.tupled(val)
        if isinstance(val, dict):
            return json.dumps(val, cls=NtvJsonEncoder)
        return val

    @staticmethod
    def n_to_i(ntv_lis, fast=False):
        ''' converting a NtvList value to an internal value'''
        if isinstance(ntv_lis, list) and len(ntv_lis) == 0:
            return []
        if isinstance(ntv_lis, list) and ntv_lis[0].__class__.__name__ in ('NtvSingle', 'NtvList'):
            # return [Sfield.n_to_i(ntv.val, fast) for ntv in ntv_lis]
            return [Sfield.n_to_i(ntv.to_obj(), fast) for ntv in ntv_lis]
        return Sfield.s_to_i(ntv_lis, fast)

    @staticmethod
    def l_to_e(lis, fast=False):
        ''' converting a list of internal values to a list of external values'''
        if fast:
            return lis
        return [Sfield.s_to_e(val) for val in lis]

    @staticmethod
    def s_to_e(val, fast=False):
        '''converting an internal value to an external value'''
        if fast:
            return val
        if val in ('null', 'false', 'true'):
            return json.loads(val)
        # if val is None or isinstance(val, bool):
        #    return json.dumps(val)
        if isinstance(val, tuple):
            return Cutil.listed(val)
        if isinstance(val, str) and len(val) > 0 and val[0] == '{':
            return json.loads(val)
        return val

    @staticmethod
    def i_to_n(val):
        ''' converting an internal value to a NTV value'''
        return Ntv.obj(Sfield.s_to_e(val))

    @staticmethod
    def l_to_n(lis):
        ''' converting a list of internal values to a list of NTV value'''
        #return Ntv.obj(Sfield.l_to_e(lis))
        return [Sfield.i_to_n(val) for val in lis]

    @staticmethod
    def i_to_name(val):
        ''' return the name of the internal value'''
        return ''

    @property
    def cod(self):
        '''return codec conversion to json value '''
        return self.l_to_e(self._codec)

    @property
    def val(self):
        '''return values conversion to string '''
        return [self.s_to_e(self._codec[key]) for key in self._keys]

    def append(self, value, unique=True):
        '''add a new value

        *Parameters*

        - **value** : new object value
        - **unique** :  boolean (default True) - If False, duplication codec if value is present

        *Returns* : key of value '''
        return super().append(self.s_to_i(value), unique)

    def isvalue(self, value, extern=True):
        ''' return True if value is in index values

        *Parameters*

        - **value** : value to check
        - **extern** : if True, compare value to external representation of self.value,
        else, internal'''
        if extern:
            return value in self.val
        return super().isvalue(value)

    def keytoval(self, key, extern=True):
        ''' return the value of a key

        *Parameters*

        - **key** : key to convert into values
        - **extern** : if True, return string representation else, internal value

        *Returns*

        - **int** : first key finded (None else)'''
        if extern:
            return self.s_to_e(super().keytoval(key))
        return super().keytoval(key)

    def loc(self, value, extern=True):
        '''return a list of record number with value

        *Parameters*

        - **value** : value to check
        - **extern** : if True, compare value to external representation of self.value,
        else, internal

        *Returns*

        - **list of int** : list of record number finded (None else)'''
        return self.recordfromvalue(value, extern=extern)

    def recordfromvalue(self, value, extern=True):
        '''return a list of record number with value

        *Parameters*

        - **value** : value to check
        - **extern** : if True, compare value to external representation of self.value,
        else, internal

        *Returns*

        - **list of int** : list of record number finded (None else)'''

        if extern:
            return super().recordfromvalue(self.s_to_i(value))
        return super().recordfromvalue(value)

    def setcodecvalue(self, oldvalue, newvalue, extern=True):
        '''update all the oldvalue by newvalue

        *Parameters*

        - **oldvalue** : list of values to replace
        - **newvalue** : list of new value to apply
        - **extern** : if True, the newvalue has external representation, else internal

        *Returns* : int - last codec rank updated (-1 if None)'''
        if extern:
            # ,nameonly, valueonly)
            return super().setcodecvalue(self.s_to_i(oldvalue), self.s_to_i(newvalue))
        return super().setcodecvalue(oldvalue, newvalue)  # , nameonly, valueonly)

    def setcodeclist(self, listcodec, extern=True):
        '''update codec with listcodec values

        *Parameters*

        - **listcodec** : list of new codec values to apply
        - **extern** : if True, the newvalue has external representation, else internal

        *Returns* : int - last codec rank updated (-1 if None)'''
        if extern:
            super().setcodeclist(self.l_to_i(listcodec))  # , nameonly, valueonly)
        super().setcodeclist(listcodec)  # , nameonly, valueonly)

    def setvalue(self, ind, value, extern=True):
        '''update a value at the rank ind (and update codec and keys)

        *Parameters*

        - **ind** : rank of the value
        - **value** : new value
        - **extern** : if True, the value has external representation, else internal

        *Returns* : None'''
        if extern:
            super().setvalue(ind, self.s_to_i(value))
        else:
            super().setvalue(ind, value)

    def setlistvalue(self, listvalue, listind=None, extern=True):
        '''update the values (and update codec and keys)

        *Parameters*

        - **listvalue** : list - list of new values
        - **listind** : list(default None) - list of index
        - **extern** : if True, the value has external representation, else internal

        *Returns* : None'''
        if extern:
            super().setlistvalue(self.l_to_i(listvalue), listind=listind)
        else:
            super().setlistvalue(listvalue, listind=listind)

    def valtokey(self, value, extern=True):
        '''convert a value to a key

        *Parameters*

        - **value** : value to convert
        - **extern** : if True, the value has external representation, else internal

        *Returns*

        - **int** : first key finded (None else)'''
        if extern:
            return super().valtokey(self.s_to_i(value))
        return super().valtokey(value)



class Nfield(Sfield):
    ''' Nfield is a child class of SField where values are NTV objects

    The methods defined in this class are conversion methods:

    *converting external value to internal value:*

    - `Nfield.l_to_i`
    - `Nfield.s_to_i`

    *converting internal value to external value:*

    - `Nfield.l_to_e`
    - `Nfield.s_to_e`

    *converting internal value / NTV value:*

    - `Nfield.i_to_n`
    - `Nfield.n_to_i`

    *extract the name of the value:*

    - `Nfield.i_to_name`
    '''

    def __str__(self):
        '''return json string format'''
        return str(self.to_ntv(modecodec='full'))
        # return '    ' + self.to_obj(encoded=True, modecodec='full', untyped=False) + '\n'

    @staticmethod
    def l_to_i(lis, fast=False):
        ''' converting a list of external values to a list of internal values

        *Parameters*

        - **fast**: boolean (default False) - list is created with a list of json values
        without control'''
        if fast:
            return [NtvSingle(val, fast=True) for val in lis]
        return [Ntv.from_obj(val) for val in lis]

    @staticmethod
    def s_to_i(val, fast=False):
        '''converting an external value to an internal value

        *Parameters*

        - **fast**: boolean (default False) - list is created with a list of json values
        without control'''
        if fast:
            return NtvSingle(val, fast=True)
        return Ntv.from_obj(val)

    @staticmethod
    def n_to_i(ntv_lis, fast=False):
        ''' converting a NTV value to an internal value'''
        return ntv_lis

    @staticmethod
    def l_to_e(lis, fast=False):
        ''' converting a list of internal values to a list of external values'''
        return [ntv.to_obj() for ntv in lis]

    @staticmethod
    def s_to_e(val, fast=False):
        '''converting an internal value to an external value'''
        return val.to_obj()

    @staticmethod
    def i_to_n(val):
        ''' converting an internal value to a NTV value'''
        return val

    @staticmethod
    def l_to_n(lis):
        ''' converting a list of internal values to a list of NTV value'''
        #return Ntv.obj(Nfield.l_to_e(lis))
        return [Sfield.i_to_n(val) for val in lis]
    
    @staticmethod
    def i_to_name(val):
        ''' return the name of the internal value'''
        return val.name
