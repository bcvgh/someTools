import queue
import re
import sys
from optparse import OptionParser


def f_read(file, method):
    with open(file, 'r', encoding='utf-8') as f:
        url = f.readlines()
        q = queue.Queue()
        method_dict = {
            'web': re.compile(r'https?://\d+\.\d+\.\d+\.\d+\D?\d*'),
            'ssh': re.compile(r'\d+\.\d+\.\d+\.\d+:22'),
            'smb': re.compile(r'\d+\.\d+\.\d+\.\d+:445'),
            'wmi': re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:139'),
            'rdp': re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:3389')
        }
        pat = method_dict[method]
        for i in url:
            # pat_web = re.compile('https?://[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\D?\d*')
            # pat_ssh = re.compile('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]:22')
            # pat_smb = re.compile('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]:(445)(135)')
            # pat_rdp = re.compile('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]:3389')
            try:
                # method = 'pat_'+method
                res = pat.findall(i)
                if not method == 'web':
                    res = res[0].split(':')
                if res[0][-1] == '/':
                    res[0] = res[0][0:-1]
                if res[0][-1] == ' ':
                    res[0] = res[0][0:-1]
                q.put(res[0])  ##ip
                # q.put(i) ##域名
            except BaseException:
                pass
    return q


def f_put(file, q):
    arr = []
    while not q.empty():
        res = q.get()+'\n'
        arr.append(res)
    with open(file, 'w') as f:
        f.writelines(arr)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", help="read from file")
    parser.add_option("-o", "--output", help="output file")
    parser.add_option("-m", "--method", help="methods")
    (options, args) = parser.parse_args()
    que = f_read(options.file, options.method)                       #读取文件路径
    if not options.output:
        options.output = options.method+'.txt'
    f_put(options.output, que)                       #输出文件路径
    print("成功输出fscan内{0}资源到{1}".format(options.method, options.output))
