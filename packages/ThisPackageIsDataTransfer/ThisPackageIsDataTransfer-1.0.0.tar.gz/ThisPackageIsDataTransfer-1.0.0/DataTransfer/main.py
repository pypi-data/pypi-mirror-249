from optparse import OptionParser

from module.network.network import SenderNetwork, ReceiverNetwork
from module.transferer.sender import SenderTransferer
from module.transferer.receiver import ReiceiverTransferer


def return_arguments():
    parser = OptionParser()
    parser.add_option('--send', dest='sender', action='stored_false', help='sender')
    parser.add_option('--receive', dest='receiver', action='stored_false', help='receiver')
    parser.add_option('-p', '--port', dest='port', help='port')
    parser.add_option('-i', '--ip', dest='ip', help='ip address')
    options = parser.parse_args()[0]
    _check_arguments(options, parser)
    return options


def _check_arguments(options, parser):
    if options.sender and options.receiver:
        parser.error('[-] Choose one option only "--send" or "--receive"')
    if not options.sender or not options.receiver:
        parser.error('[-] Role not found')
    if not options.port:
        parser.error('[-] Port not found')
    if not options.ip:
        parser.error('[-] Ip address not found')


def run_sender(ip, port):
    network = SenderNetwork(ip, port)
    sender = SenderTransferer(network)
    sender.run()


def run_receiver(ip, port):
    network = ReceiverNetwork(ip, port)
    receiver = ReiceiverTransferer(network)
    receiver.run()


def main():
    options = return_arguments()

    ip = options.ip
    port = options.port

    if options.sender:
        run_sender(ip, port)
    elif options.receiver:
        run_receiver(ip, port)


if __name__ == '__main__':
    main()
