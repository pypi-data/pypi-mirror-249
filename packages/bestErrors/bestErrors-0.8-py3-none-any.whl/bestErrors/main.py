from erodecor import Error


@Error
class MathError:
    ...


@Error
class AuthenticationError:
    ...


@Error
class PermissionDeniedError:
    ...


@Error
class OutOfRangeError:
    ...


@Error
class InvalidTypeError:
    ...
