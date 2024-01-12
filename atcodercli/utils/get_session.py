import rich, requests, os, yaml
from rich.console import Console
from requests.utils import cookiejar_from_dict

def get_session(console:Console) -> requests.Session:
    """
        read the file ~/.config/atcli/session.yaml and return a requests.session object
    """
    try:
        with open(os.path.join(os.path.expanduser('~'), ".config", "atcli", "session.yaml")) as read_stream:
            dat = yaml.safe_load(read_stream)
    except FileNotFoundError:
        console.log(f'[red]ERROR:no session file found at {os.path.join(os.path.expanduser("~"), ".config", "atcli", "config.yaml")}[/red]')
        console.log(r'try run "atcli login" first.')
        raise SystemExit(1)
    session = requests.session()
    session.cookies.update(cookiejar_from_dict(dat['cookies']))
    return session

if __name__ == "__main__":
    session = get_session(Console())
    username = "ricky_awa"
    res = session.get("https://atcoder.jp")
    print(username in res.text) # True

