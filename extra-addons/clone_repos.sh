#!/bin/bash

# Define o caminho para o arquivo oca-dependencies.txt
dependencies_file="./l10n-brazil/oca_dependencies.txt"

# Loop through the dependencies file
while read repo; do
  # Clona o repositório usando o comando git clone
  git clone -b 16.0 --single-branch --depth=1 https://github.com/OCA/$repo.git ./$repo
  sudo rm -rf ./$repo/.git
  sudo rm -rf ./$repo/.github
  sudo rm -rf ./$repo/.copier-answers.yml
  sudo rm -rf ./$repo/.pre-commit-config.yaml
  sudo rm -rf ./$repo/LICENSE
done < "$dependencies_file"