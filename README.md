# SistemaAmbulancia

Protótipo acadêmico desenvolvido na disciplina de Arquitetura de Software da Universidade Católica de Brasília (UCB). O projeto parte do estudo das falhas do sistema de despacho de ambulâncias de Londres e simula o registro de chamadas, a triagem, a seleção e o despacho de ambulâncias, o acompanhamento dos atendimentos e a visualização de ocorrências no mapa.

A aplicação usa Python e PySide6 na interface, MySQL na persistência e Leaflet no mapa.

## Estrutura do projeto

| Diretório em `SistemaAmbulancia/` | Responsabilidade |
| --- | --- |
| [`app/`](SistemaAmbulancia/app) | Inicialização em `main.py` e simulação dos deslocamentos em `simulacao.py`. |
| [`domain/`](SistemaAmbulancia/domain) | Regras de negócio e entidades. `Modulo_Ambulancia` reúne ambulâncias, equipes, despachos e atendimentos. `Modulo_Chamada` trata chamadas, endereços, prioridades e estados. `Modulo_Triagem` concentra a triagem e a seleção de ambulâncias. `Modulo_Usuario` reúne os papéis de usuário. |
| [`events/`](SistemaAmbulancia/events) | Gerenciamento de eventos e comunicação entre componentes. |
| [`services/`](SistemaAmbulancia/services) | Conexão com o MySQL em `Modulo_Banco_Dados`, mapa em `Modulo_Mapa` e integração opcional com o Ollama em `IA_Ollama`. |
| [`ui/`](SistemaAmbulancia/ui) | Telas, recursos visuais e navegação da aplicação. |

## Antes de executar

- Use Windows com PowerShell e Python 3.11 de 64 bits para seguir o roteiro abaixo.
- Tenha acesso a um servidor MySQL e a uma cópia do esquema do projeto. O repositório ainda não inclui o script de criação ou as migrações do banco.
- Importe o esquema no banco indicado em `DB_NAME`. O aplicativo usa as tabelas `endereco`, `chamada`, `ambulancia`, `atendimento` e `atendimento_ambulancia`. Use um usuário com permissão para consultar, inserir e atualizar os dados. Para simular despachos, o banco deve conter ambulâncias disponíveis com placa e coordenadas válidas.

## Executar em dois terminais

Abra os dois terminais na raiz do repositório.

### Terminal 1 — servidor do mapa

```powershell
Set-Location SistemaAmbulancia/services/Modulo_Mapa/mapa_html
python -m http.server 8000 --bind 127.0.0.1
```

Mantenha o servidor aberto enquanto usa a aplicação. Para verificar se ele está servindo a página, abra `http://127.0.0.1:8000/mapa.html`. A aplicação carrega esse endereço fixo.

### Terminal 2 — aplicação

Crie o ambiente virtual, instale as dependências e copie a configuração de exemplo. Na primeira execução, rode os comandos abaixo.

```powershell
Set-Location SistemaAmbulancia
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha o arquivo `SistemaAmbulancia/.env` com os valores do seu MySQL.

| Variável | Valor esperado |
| --- | --- |
| `DB_HOST` | Endereço do servidor. Use `127.0.0.1` se estiver na mesma máquina. |
| `DB_PORT` | Porta TCP do MySQL, geralmente `3306`. |
| `DB_NAME` | Nome do banco com o esquema importado. |
| `DB_USER` | Usuário autorizado a acessar o banco. |
| `DB_PASSWORD` | Senha desse usuário. |

O Git ignora o arquivo `.env`. Quando definidas, as variáveis de ambiente têm precedência sobre o arquivo. Para preservar as configurações já preenchidas, copie o exemplo apenas na primeira configuração.

Com o ambiente virtual ativo e o terminal em `SistemaAmbulancia/`, inicie a aplicação.

```powershell
python -m app.main
```

Se o PowerShell bloquear a ativação, use o Python do ambiente virtual diretamente nos comandos de instalação e execução, por exemplo `.\venv\Scripts\python.exe -m app.main`.

Se aparecer `ModuleNotFoundError: No module named 'ui.screens'` no Windows, execute os comandos abaixo no mesmo terminal. O ajuste vale para essa sessão do PowerShell e contorna a diferença de maiúsculas e minúsculas nos nomes das pastas em um sistema de arquivos que não distingue a grafia.

```powershell
$env:PYTHONCASEOK = '1'
python -m app.main
```

## Limitações atuais

- A triagem em [`IATriagem.py`](SistemaAmbulancia/domain/Modulo_Triagem/IATriagem.py) usa uma resposta fixa de demonstração. A chamada ao Ollama está desativada, então iniciar um servidor Ollama é dispensável para o roteiro.
- O mapa, a busca de endereços e a simulação de rotas dependem de serviços externos, entre eles OpenStreetMap, BrasilAPI, Nominatim e OSRM. A seleção padrão de ambulâncias usa a estratégia por distância aproximada, chamada de hipotenusa no código.
- A página do mapa ainda referencia dois arquivos locais de Leaflet Routing Machine ausentes no repositório. Essas referências retornam 404. O código atual usa Leaflet para desenhar o mapa e consulta o OSRM diretamente para obter as rotas.
- As telas estão distribuídas entre `ui/Screens` e `ui/screens` no Git, mas os imports usam `ui.screens`. Em sistemas de arquivos que distinguem maiúsculas de minúsculas, é preciso uniformizar esses caminhos para executar a aplicação.

## Revisão das mudanças

Abra uma issue para descrever a mudança, trabalhe em uma branch e abra um pull request com o vínculo à issue. Registre as verificações feitas e peça a revisão de outro integrante antes do merge. Use o [modelo de pull request](.github/pull_request_template.md) para registrar o tipo de manutenção, os resultados das verificações e o checklist de revisão.
