#!/bin/sh
#
# Este script serve para inserir os diretórios que contém binário na
# HOME('~/bin' e '~/.local/bin') na variável PATH do usuario atual.
#
VERSION='2020-05-16'
#

# NÃO pode ser root.
[ $(id -u) -eq 0 ] && {
	echo "\033[1;31mVocê NÃO pode ser o [root] para executar esse programa\033[m"
	exit 1
}


# Inserir ~/.local/bin em PATH.
echo "$PATH" | grep -q "$HOME/.local/bin" || {
	PATH="$HOME/.local/bin:$PATH"
}


path_bash()
{
	# Criar o arquivo ~/.bashrc se não existir
	if [ ! -f "$HOME/.bashrc" ]; then
		echo ' ' >> "$HOME/.bashrc"
	fi

	# Se a linha de configuração já existir, encerrar a função aqui.
	grep "$HOME/.local/bin" "$HOME/.bashrc" 1> /dev/null && return 0

	# Continuar
	echo "Configurando o arquivo [$HOME/.bashrc]"
	echo "export PATH=$PATH" >> "$HOME/.bashrc"
}

path_zsh()
{
	# Criar o arquivo ~/.zshrc se não existir
	if [ ! -f "$HOME/.zshrc" ]; then
		echo ' ' >> "$HOME/.zshrc"
	fi

	# Se a linha de configuração já existir, encerrar a função aqui.
	grep "$HOME/.local/bin" "$HOME/.zshrc" 1> /dev/null && return 0

	# Continuar
	echo "Configurando o arquivo [$HOME/.zshrc]"
	echo "export PATH=$PATH" >> "$HOME/.zshrc"
}

main()
{

	path_bash
	path_zsh

	Bash_Shell=$(command -v bash)
	Zsh_Shell=$(command -v zsh)

	if [ -x "$Bash_Shell" ]; then
		bash -c ". $HOME/.bashrc"
	fi

	if [ -x "$Zsh_Shell" ]; then
		zsh -c ". ~/.zshrc"
	fi
}

main

