# BTC Analytics

Projeto de análise e backtesting de estratégias de trading para Bitcoin.

## Requisitos

- Python 3.12 ou superior
- Poetry (gerenciador de dependências)
- Git Bash
- VS Code

## Configuração do Ambiente

1. **Instalar Python 3.12**
   - Baixe e instale o Python 3.12 do [site oficial](https://www.python.org/downloads/)
   - Durante a instalação, marque a opção "Add Python to PATH"

2. **Instalar Poetry**
   ```bash
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

3. **Instalar Git Bash**
   - Baixe e instale o Git Bash do [site oficial](https://git-scm.com/downloads)

4. **Configurar VS Code**
   - Instale o VS Code do [site oficial](https://code.visualstudio.com/)
   - Instale as extensões:
     - Python
     - Jupyter
     - Git

## Configuração do Projeto

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/btc-analytics.git
   cd btc-analytics
   ```

2. **Configurar o ambiente virtual com Poetry**
   ```bash
   poetry install
   ```

3. **Configurar o VS Code para usar Git Bash e ativar o ambiente virtual automaticamente**
   - Crie/edite o arquivo `.vscode/settings.json`:
   ```json
   {
       "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
       "python.terminal.activateEnvironment": true,
       "python.terminal.activateEnvInCurrentTerminal": true,
       "python.envFile": "${workspaceFolder}/.env",
       "terminal.integrated.defaultProfile.windows": "Git Bash",
       "terminal.integrated.profiles.windows": {
           "Git Bash": {
               "path": "C:\\Program Files\\Git\\bin\\bash.exe",
               "args": []
           }
       },
       "jupyter.notebookFileRoot": "${workspaceFolder}",
       "jupyter.alwaysTrustNotebooks": true,
       "jupyter.enableAutoSave": true,
       "jupyter.cleanOutputsOnSave": true,
       "jupyter.cleanOutputsOnSave.exclude": [
           "**/data/**"
       ]
   }
   ```

   Esta configuração:
   - Usa Git Bash como terminal padrão
   - Ativa o ambiente virtual automaticamente
   - Limpa os resultados das células do notebook antes de salvar
   - Mantém os resultados apenas em notebooks dentro da pasta `data/`

## Estrutura do Projeto

```
btc-analytics/
├── scripts/
│   ├── extract.ipynb
│   └── regras_de_negocio.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── scores/
├── .vscode/
│   └── settings.json
├── pyproject.toml
└── README.md
```

## Uso

1. **Abrir o projeto no VS Code**
   - Abra o VS Code
   - Abra a pasta do projeto (File > Open Folder)
   - O terminal já estará configurado com Git Bash e o ambiente virtual ativado

2. **Executar o notebook**
   - Abra o arquivo `scripts/extract.ipynb`
   - Execute as células do notebook
   - Os resultados serão limpos automaticamente ao salvar

## Dependências

O projeto usa as seguintes bibliotecas principais:
- pandas
- yfinance
- matplotlib
- mplcyberpunk

Todas as dependências estão listadas no arquivo `pyproject.toml` e serão instaladas automaticamente pelo Poetry.

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 