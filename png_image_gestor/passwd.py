import controller.SecurityController as security

passwd = input("[+] > ")

passwd_encripted = security.encrypt_passwd(passwd)

print(passwd_encripted)