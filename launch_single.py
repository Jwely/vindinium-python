import vindinium


def main():

    #while True:
        # Create a vindinium client
        client = vindinium.Client(
            server = "http://vindinium.org",
            key = "aewjd4k0",    # jbot05
            mode = "training",
            n_turns = 300,
            open_browser = True
        )

        props = {"mine" : 1.0,
                 "drink": 1.0,
                 "kill" : 1.0,
                 "flee" : 1.0}

        url = client.run(vindinium.bots.RoleBot(props))
        print 'Replay in:', url

if __name__ == '__main__':
    main()
