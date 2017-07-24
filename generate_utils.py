import os
import stat

def is_user_writable(filename):
  return bool(os.stat(filename).st_mode & stat.S_IWUSR)

class OutFile:
    """
    with OutFile("compiled.txt") as f: f.write('stuff')
    # compiled.txt is read only, you can repeat this process
    """
    def __init__(self, filename, supargs=''):
        self.filename = filename
        self.supargs = supargs
    
    def unlock(self):
        if is_user_writable(self.filename):
            raise ValueError('{} exists and is writable'.format(self.filename))
        if os.path.isfile(self.filename):
            os.chmod(self.filename, 0o644)
    
    def lock(self):
        os.chmod(self.filename, 0o444)
    
    def __enter__(self):
        self.unlock()
        self.f = open(self.filename, ''.join({'w'} | set(self.supargs)))
        self.f.__enter__()
        return self.f
    
    def __exit__(self, type, value, traceback):
        self.lock()
        self.f.__exit__(type, value, traceback)