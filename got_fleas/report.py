from prettytable import PrettyTable


def rprint(pmap, title):
    report = PrettyTable()
    for column, players in pmap.items():
        header = '{} [{}]'.format(column, len(players))
        if len(players) == 0:
            report.add_column(header, ' ')  # Needs a space or everything shifts left
        else:
            report.add_column(header, ['\n'.join(players)])
    print(title + ':')
    print(report)
    print('')


def build(report_str, players):
    pass
