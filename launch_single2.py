import vindinium


def main():

    #while True:
        # Create a vindinium client
        client = vindinium.Client(
            server = "http://vindinium.org",
            key = "mpsm2rzk",   #jbot03
            mode = "arena",
            n_turns = 300,
            open_browser = False
        )

        props = {"mine" : 10.0,
                 "drink": 3.0,
                 "kill" : 4.0,
                 "flee" : 3.0}

        url = client.run(vindinium.bots.DecisionBot(props))
        print 'Replay in:', url

if __name__ == '__main__':
    main()