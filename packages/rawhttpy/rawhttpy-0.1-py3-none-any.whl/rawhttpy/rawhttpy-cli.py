import sys
from rawhttpy import RawHTTPy

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f: r = f.read()
        else:
            print(f"Usage: {sys.argv[0]} {{file}}")
            print("Provide a file containing a valid raw HTTP request")
            sys.exit(0)
        
        httpy = RawHTTPy(r)

        print(f'Method: {httpy.method}')
        print(f'URL: {httpy.url}')
        print(f'Host: {httpy.host}')
        print(f'Path: {httpy.path}')
        print(f'HTTP Version: {httpy.http_version}')

        print('# HEADERS')
        for k,v in httpy.headers.items(): print(f'{k}: {v}')

        print('# BODY')
        for k,v  in httpy.body.items(): print(f'{k}: {v}')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
