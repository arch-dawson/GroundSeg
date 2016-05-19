#!/usr/bin/python3

import subprocess

uftpCall = ("uftp"
            " -L uftp.log"
            " -Y aes256-gcm"
            " -h sha512"
            " -c" 

# -L: Specifies the log file
# -Y: Specifies the encryption standard. ccm is similar but slower
# -h: Specifies Secure Hash Algorithm type.  
# -c: forces clients to authenticate by sending RSA key

