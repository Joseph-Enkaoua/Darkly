# Darkly
a project to find vulnerabilities in an http website

Modify the .iso file path and run this command in the terminal, the site will be available at localhost:8080:

qemu-system-x86_64 -m 2048 -cdrom <PATH TO THE .ISO FILE> -boot d \
-netdev user,id=net0,hostfwd=tcp::8080-:80 -device e1000,netdev=net0