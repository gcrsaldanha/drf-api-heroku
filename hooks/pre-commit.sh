#!/bin/sh

# Se estiver usando windows
# #!C:/Program\ Files/Git/usr/bin/sh.exe  (caminho para o sh.exe do Git Bash)
# Créditos: https://www.tygertec.com/git-hooks-practical-uses-windows/

# Outra opção para windows, criar um arquivo chamado pre-commit.ps1 com o script
# E aqui adicionar a linha:
# exec powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.git\hooks\pre-commit.ps1"


black --check .
