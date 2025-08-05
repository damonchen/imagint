import re

pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
p = re.compile(pattern)


def password_type(value):
    if p.match(value):
        return value
    else:
        raise ValueError(
            "Invalid password format, should be minimum eight characters, at least one letter, one number and one special character:"
        )


def email_type(value):
    return value
