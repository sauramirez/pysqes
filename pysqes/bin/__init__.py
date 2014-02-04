def main(argv=None):
    print "entered main"
    cmd = PysqesCommand()
    cmd.execute()

if __name__ == '__main__':          # pragma: no cover
    print "entry point"
