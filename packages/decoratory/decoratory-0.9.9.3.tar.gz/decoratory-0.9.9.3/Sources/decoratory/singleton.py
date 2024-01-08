#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Singleton**

    A singleton pattern is a design pattern that limits the instantiation of a
    class to a single (unique) instance. This is useful when exactly one
    unique object is needed i.e. to manage an expensive resource or coordinate
    actions across module boundaries.

    Attributes
    ----------
    Singleton (class):
        Creates a singleton instance as a callable object.

    SemiSingleton (class):
        Creates a resettable semi singleton instance as a callable object.

    Methods
    -------
        None.

    Examples
    --------

    from decoratory.singleton import Singleton

    # -------------------------------------------------------------------------
    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Create Instances
    a = Animal(name='Teddy')        # Creates Teddy, the primary instance
    b = Animal(name='Roxie')        # Returns Teddy, no Roxi is created

    # Case 1: Static decoration using @Singleton or @Singleton()
    print(f"a = {a}")               # a = Animal('Teddy')
    print(f"b = {b}")               # b = Animal('Teddy')
    print(f"a is b: {a is b}")      # a is b: True
    print(f"a == b: {a == b}")      # a == b: True

    # Case 2: Dynamic decoration providing extra initial default values
    Animal = Singleton(Animal, 'Teddy')
    Animal()                        # Using the decorator's default 'Teddy'
    a = Animal(name='Roxie')        # Returns Teddy
    print(a)                        # Animal('Teddy')

    # -------------------------------------------------------------------------
    @Singleton(resettable=True)     # Exposes an additional reset method
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Case 3: Decoration using @Singleton(resettable=True)
    print(Animal(name='Teddy'))     # Animal('Teddy')
    print(Animal(name='Roxie'))     # Animal('Teddy')   (=primary instance)
    Animal.reset()                  # Reset the singleton
    print(Animal(name='Roxie'))     # Animal('Roxie')
    print(Animal(name='Teddy'))     # Animal('Roxie')   (=primary instance)

    # -------------------------------------------------------------------------
    from decoratory.singleton import SemiSingleton

    @SemiSingleton                  # or @SemiSingleton()
    class Animal:
        pass                        # Some code ...

    # -------------------------------------------------------------------------
    from decoratory.singleton import Singleton
    from concurrent.futures import ThreadPoolExecutor, as_completed

    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Create Instances
    names = ["Teddy", "Roxie", "Molly", "Benny"]
    with ThreadPoolExecutor(max_workers=2) as tpe:
        futures = [tpe.submit(Animal, name) for name in names]

    # Case 4: Decoration using @Singleton
    for future in futures:
        instance = future.result()  # All the same instances, i.e.
        print(instance)             # Animal('Teddy') -- four times!
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Singleton"
__module__ = "singleton.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "https://decoratory.app"
__copyright__ = f"(c) Copyright 2020-2024, {__author__}, {__company__}."
__created__ = "2020-01-01"
__version__ = "0.9.9.2"
__date__ = "2024-01-07"
__time__ = "14:35:47"
__state__ = "Beta"
__license__ = "MIT"

__all__ = ["Singleton", "SemiSingleton"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from threading import Lock
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Classes
class Singleton:
    """**Singleton**

    Singleton(substitute, *args, resettable, **kwargs)

    Attributes
    ----------
    substitute (callable|type):
        A type to be made a singleton

    resettable (bool):
        If True exposes a reset() method

    instance (object):              (property)
        Gets/Sets a singleton instance

    Methods
    -------
    reset(self) -> None:            (if resettable=True, only!)
        Resets the singleton instance (None)
    """

    def __init__(self,
                 substitute: Union[type, callable, None] = None,
                 *args: object,
                 resettable: bool = False,
                 **kwargs: object) -> None:
        """Set up a singleton.

        Parameters:
            substitute (object): A type to be made a singleton
            resettable (bool): If True exposes a reset() method

        Returns:
            self (object): Singleton decorator instance
        """
        self.__set__substitute(substitute)
        self.__set__lock(Lock())  # For threadsafety

        # The unique instance
        self._instance = None

        # If resettable == True exposes a reset() method
        if bool(resettable):
            def reset(s: object = self) -> None:
                """Define reset method"""
                s._instance = None

            # Add the reset method
            setattr(self, 'reset', reset)

        # --- Decorator Arguments Template (1/2)
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__substitute.callee, updated=())

    def __call__(self, *args, **kwargs):
        """Apply the decorator."""

        # --- Decorator Arguments Template (2/2)
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__substitute.callee, updated=())
            return self
        else:  # *** Decorator ***
            # Create and store new or return existing instance
            if self._instance is None:
                with self.__lock:
                    if self._instance is None:
                        if args or kwargs:
                            self._instance = F(self.__substitute.callee,
                                               *args, **kwargs).eval()
                        else:
                            self._instance = self.__substitute.eval()
            return self._instance

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__lock(self):
        return self.__lock

    def __set__lock(self, value):
        self.__lock = value

    lock = property(__get__lock, __set__lock)

    # Methods
    def get_instance(self) -> object:
        """Returns the singleton instance"""
        return self._instance

    def set_instance(self, value: dict = None) -> None:
        """Sets the singleton instance"""
        self._instance = value

    instance = property(get_instance, set_instance)


class SemiSingleton(Singleton):
    """SemiSingleton

    A subclass shortcut for a resettable singleton.
    """

    def __init__(self,
                 substitute: object = None,
                 *args: object,
                 **kwargs: object) -> None:
        """Set up a semi singleton.

        Parameters:
            substitute (object): A type to be made a semi singleton

        Returns:
            self (object): Semi singleton decorator instance
        """
        kwargs["resettable"] = True
        super().__init__(substitute, *args, **kwargs)


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    import decoratory.singleton as module
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(module, Singleton),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
