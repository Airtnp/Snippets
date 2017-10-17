def EncodedOutput():
    def __init__(self, enc):
        self.enc = enc
        self.stdout = sys.stdout
        self.stderr = sys.stderr
    def __enter__(self):
        if sys.stdout.encoding is None:
            w = codecs.getwriter(self.enc)
            sys.stdout = w(sys.stdout)
            sys.stderr = w(sys.stderr)
    def __exit__(self, exc_ty, exc_val, tb):
        sys.stdout = self.stdout