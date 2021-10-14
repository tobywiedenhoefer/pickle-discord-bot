class Keys:
    token = 0
    guild_id = 1

    def get_key(num: int) -> str:
        key = ''
        try:
            with open("secrets.txt", "r") as f:
                text = f.read()
                keys = text.split('\n')
                key = keys[num]
        except Exception as e:
            print(e)
        return str(key)
