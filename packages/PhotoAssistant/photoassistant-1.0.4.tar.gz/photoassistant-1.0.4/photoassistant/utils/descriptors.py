# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import copy

class RDescriptor:
    @staticmethod
    def not_implemented(name):
        def _not_implemented(owner, *_):
            raise NotImplementedError(f"Function '{name}' of {owner} not implemented!")
        return _not_implemented

    def __set_name__(self, owner, name):
        self._fget_name = f"get_{name}"
        if not hasattr(owner, self._fget_name):
            setattr(owner, self._fget_name, RDescriptor.not_implemented(self._fget_name))

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._fget_name)()


class RWDescriptor(RDescriptor):

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self._fset_name = f"set_{name}"
        if not hasattr(owner, self._fset_name):
            setattr(owner, self._fset_name, RWDescriptor.not_implemented(self._fset_name))

    def __set__(self, obj, value):
        if obj is None:
            return self
        getattr(obj, self._fset_name)(value)


class SettingsDescriptor:
    def __init__(self, default_value, deserializer=lambda value: value, serializer=lambda value: str(value)):
        self._default_value = default_value
        self._serializer = serializer
        self._deserializer = deserializer
        self._settings_name = None

    def _set_value(self, owner, value):
        if self._settings_name is None:
            raise AttributeError("SettingsDescriptor was not initialized propertly")

        value_serialized = value
        if not isinstance(value, str):
            value_serialized = self._serializer(value_serialized)

        try:
            value_deserialized = self._deserializer(value_serialized)
            assert value_serialized == self._serializer(value_deserialized)
            if not isinstance(value, str):
                assert value == value_deserialized
            else:
                assert value == value_serialized
        except:
            raise ValueError(f"Value '{value}' is incompatible with serializer/deserializer for '{self._settings_name}'")

        settings_dict = getattr(owner, "_settings", dict())
        if getattr(owner, "_settings_owner", None) != owner:
            setattr(owner, "_settings_owner", owner)
            settings_dict = copy.deepcopy(settings_dict)
        settings_dict[self._settings_name] = value_serialized
        setattr(owner, "_settings", settings_dict)

    def __set_name__(self, owner, name):
        self._settings_name = name
        self._set_value(owner, self._default_value)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self._settings_name is None:
            raise AttributeError("SettingsDescriptor was not initialized propertly")
        return self._deserializer(getattr(obj, "_settings", dict())[self._settings_name])

    def __set__(self, obj, value):
        self._set_value(obj, value)

class Signal:
    # - observer pattern -
    # This descriptor mimics the behavior of the Qt Signals & Slots.
    # It supports only connecting/disconnecting to/from Python callables.
    # The emit function passes any arguments to the Python callable. The programmer
    # is responsible for matching arguments passed to 'emit' with the signature of all
    # connected callables.
    # Why? The Qt implementation requires inheriting from QObject and calling the
    # constructor for QObject once. This implementation is a solution if multiple
    # inheritance is not desired.
    class SignalConnector:
        def __init__(self, connectable=True):
            self.connectable = connectable
            self._registered_callables = list()

        def connect(self, callable):
            assert self.connectable
            self._registered_callables.append(callable)

        def emit(self, *args, **kwargs):
            for callable in self._registered_callables:
                callable(*args, **kwargs)

    def __set_name__(self, owner, name):
        self._signal_connector_name = name
        # initialize a SignalConnector for the class itself
        if not hasattr(owner, "_signal_connectors"):
            setattr(owner, "_signal_connectors", {self._signal_connector_name: Signal.SignalConnector()})

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # lazy-initialize a SignalConnector on first connect/first emit:
        # <signal_variable>.connect(<callable>) or <signal_variable>.emit(<args>)
        if getattr(obj, "_signal_connectors_owner", None) != obj:
            setattr(obj, "_signal_connectors_owner", obj)
            setattr(obj, "_signal_connectors", {self._signal_connector_name: Signal.SignalConnector()})
        return getattr(obj, "_signal_connectors")[self._signal_connector_name]
