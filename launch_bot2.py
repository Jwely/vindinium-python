import vindinium

def read_keys():

    keys = []
    with open("trash_bots.txt", 'r') as f:
        for lines in f:
            keys.append(lines.split(", ")[1].replace("\n",""))
    return keys


def launch_bot(bot, key, continuous = False, mode = "training", tmap = "m1"):

    # read some trash bots keys in

    if continuous:
        while True:
            # Create a vindinium client
            client = vindinium.Client(
                server = "http://vindinium.org",
                key = key,
                mode = mode,
                n_turns = 300,
                open_browser = True
            )

            client.run(bot)

    else:
        # Create a vindinium client
        client = vindinium.Client(
            server = "http://vindinium.org",
            key = key,
            mode = mode,
            training_map = tmap,
            n_turns = 300,
            open_browser = True
        )

        client.run(bot)


if __name__ == '__main__':

    launch_bot(vindinium.bots.MinerBot(),
               read_keys()[0],
               continuous = False,
               mode = "arena",
               tmap = "m3")