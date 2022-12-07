.. JSON Pointer documentation master file, created by
   sphinx-quickstart on Mon Dec  5 21:26:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Fast JSON Pointer's documentation!
=============================================

Implements `RFC 6901`_ JSON pointers, and `relative JSON pointer`_ resolution.

This module is not necissarily fast (yet), but there are enough variations on
``json-pointer`` in pypi to merit picking some prefix to differentiate, and "fast"
seemed a relatively short and punchy choice.

If you need this to *really* be fast, open an issue and let me know. I want to do
a rust extension module at some point. That ought to be fast enough to claim we're
fast.

.. include:: ../badges.rst

.. sidebar-links::
   :caption: Project Links:
   :github:
   :pypi: fast-json-pointer

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _RFC 6901: https://www.rfc-editor.org/rfc/rfc6901
.. _relative JSON pointer: https://json-schema.org/draft/2020-12/relative-json-pointer