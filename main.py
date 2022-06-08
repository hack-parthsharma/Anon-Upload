import argparse
import os
from pathlib import Path
from requests import get, post, ConnectionError, head
import requests
from requests.exceptions import MissingSchema
import json
import sys
import tqdm
from typing import List
import requests_toolbelt

__version__ = "1.0.8"
package_name = "anon"
url = 'https://api.anonfiles.com/upload'

class ProgressBar(tqdm.tqdm):
    def update_to(self, n: int) -> None:
        """Update the bar in the way compatible with requests-toolbelt.

        This is identical to tqdm.update, except ``n`` will be the current
        value - not the delta as tqdm expects.
        """
        self.update(n - self.n)  # will also do self.n = n

def upload(filenames:List[str]):
    for filename in filenames:
        if os.path.isdir(filename):
            print('[ERROR] You cannot upload a directory!')
            break
        else:
            yes = {'yes','y','ye',''}
            choice = input(f"Do you want change filename {filename} [Y/n]: ").lower()
            if choice in yes:
                input_name = input("Enter new file name with extension: ")
                try:
                    os.rename(filename, input_name)
                except FileNotFoundError:
                    print(f'[ERROR]: The file "{filename}" doesn\'t exist!')
                    break

                try:
                    files = {'file': (open(input_name, 'rb'))}
                except FileNotFoundError:
                    print(f'[ERROR]: The file "{input_name}" doesn\'t exist!')
                    break
            else:
                try:
                    files = {'file': (open(filename, 'rb'))}
                except FileNotFoundError:
                    print(f'[ERROR]: The file "{filename}" doesn\'t exist!')
                    break

        if (os.path.isfile(filename)==False):
            print("[UPLOADING]: ", input_name)
            filename = input_name
        else:
            print("[UPLOADING]: ", filename)

        data_to_send = []
        session = requests.session()

        with open(filename, "rb") as fp:
            data_to_send.append(
                ("file", (filename, fp))
            )
            encoder = requests_toolbelt.MultipartEncoder(data_to_send)
            with ProgressBar(
                total=encoder.len,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                file=sys.stdout,
            ) as bar:
                monitor = requests_toolbelt.MultipartEncoderMonitor(
                    encoder, lambda monitor: bar.update_to(monitor.bytes_read)
                )

                r = session.post(
                    url,
                    data=monitor,
                    allow_redirects=False,
                    headers={"Content-Type": monitor.content_type},
                )

        resp = json.loads(r.text)
        if resp['status']:
            urlshort = resp['data']['file']['url']['short']
            urllong = resp['data']['file']['url']['full']
            print(f'[SUCCESS]: Your file has been succesfully uploaded:\nFull URL: {urllong}\nShort URL: {urlshort}')
            with open('urls.txt', 'a+') as f:
                f.write(urllong)
            print('url saved in urls.txt file')
        else:
            message = resp['error']['message']
            errtype = resp['error']['type']
            print(f'[ERROR]: {message}\n{errtype}')

def download(urls:List[str], path: Path=Path.cwd()):
    for url in urls:
        try:
            filesize = int(head(url).headers["Content-Length"])
        except ConnectionError:
            print("[Error]: No internet")
            return 1
        except MissingSchema as e:
            print(e)
            return 1
        filename = os.path.basename(url)
        
        chunk_size = 1024

        try:
            with get(url, stream=True) as r, open(path, "wb") as f, tqdm(
                    unit="B",  # unit string to be displayed.
                    unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
                    unit_divisor=1024,  # is used when unit_scale is true
                    total=filesize,  # the total iteration.
                    file=sys.stdout,  # default goes to stderr, this is the display on console.
                    desc=filename  # prefix to be displayed on progress bar.
            ) as progress:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    datasize = f.write(chunk)
                    progress.update(datasize)
        except ConnectionError:
            return 1
    
example_uses = '''example:
   anon up {files_name}
   anon d {urls}'''

def main(argv = None):
    parser = argparse.ArgumentParser(prog=package_name, description="upload your files on anonfile server", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    upload_parser = subparsers.add_parser("up", help="upload files to https://anonfiles.com")
    upload_parser.add_argument("filename", type=str, nargs='+', help="one or more files to upload")

    download_parser = subparsers.add_parser("d", help="download files ")
    download_parser.add_argument("filename", nargs='+', type=str, help="one or more URLs to download")
    download_parser.add_argument('-p', '--path', type=Path, default=Path.cwd(), help="download directory (CWD by default)")

    parser.add_argument('-v',"--version",
                            action="store_true",
                            dest="version",
                            help="check version of deb")

    args = parser.parse_args(argv)

    if args.command == "up":
        return upload(args.filename)
    elif args.command == "d":
        return download(args.filename, args.path)
    elif args.version:
        return print(__version__)
    else:
        parser.print_help()

if __name__ == '__main__':
    raise SystemExit(main())
