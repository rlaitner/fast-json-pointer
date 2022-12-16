API
========================================

JSON Pointer
++++++++++++
.. automodule:: fast_json_pointer

.. autoclass:: JsonPointer
    :members:
    :special-members: __str__, __eq__
    
.. autoclass:: RelativeJsonPointer
    :members:
    :special-members: __str__, __eq__

RFC 6901 Parser
+++++++++++++++
.. automodule:: fast_json_pointer.rfc6901_parser

.. autofunction:: validate
.. autofunction:: parse
.. autofunction:: unparse
.. autofunction:: escape
.. autofunction:: unescape


Relative Pointer Parser
+++++++++++++++++++++++
.. automodule:: fast_json_pointer.rel_parser

.. autofunction:: parse
.. autofunction:: unparse


Exceptions
++++++++++
.. automodule:: fast_json_pointer.exceptions

.. autoexception:: JsonPointerException
.. autoexception:: ParseException