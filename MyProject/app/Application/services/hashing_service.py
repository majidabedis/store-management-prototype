import bcrypt


class HashingService:

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        # for strong salt
        salt_strong = bcrypt.gensalt(rounds=14)

        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    @staticmethod
    def check_password(password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
