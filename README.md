# Gerador de Senhas

Gerador de senhas em Python com interface gráfica PySide6 e armazenamento em banco de dados SQLite.

## Padrão de Senha

As senhas seguem o padrão: **Palavra + Símbolo + Palavra + Número da Unidade**

Exemplo: `Garfo@Tomate02`

## Funcionalidades

- ✅ Gera senhas seguindo o padrão: Palavra + Símbolo + Palavra + Número da Unidade
- ✅ **Armazena senhas em banco de dados SQLite**
- ✅ **Evita gerar senhas duplicadas**
- ✅ **Organiza senhas por unidade**
- ✅ **Visualizar histórico de senhas por unidade**
- ✅ Seleção de unidade (24 unidades disponíveis)
- ✅ Botão para gerar nova senha
- ✅ Botão para copiar senha para área de transferência
- ✅ Botão para visualizar todas as senhas geradas de uma unidade
- ✅ Interface gráfica moderna e intuitiva
- ✅ Palavras temáticas de restaurante em português
- ✅ Símbolos especiais: !@#$%&*+?

## Banco de Dados

O aplicativo cria automaticamente um arquivo `senhas_geradas.db` que armazena:
- Senha gerada
- Unidade associada
- Número da unidade
- Data e hora de geração

## Personalização

Você pode editar o arquivo `gerador.py` para:
- Adicionar mais palavras à lista `self.palavras`
- Modificar os símbolos disponíveis em `self.simbolos`
- Adicionar ou remover unidades no dicionário `self.unidades`
- Ajustar cores e estilos da interface

## Segurança

- Cada senha é única no sistema (não há duplicatas)
- O sistema tenta até 100 vezes gerar uma senha única antes de alertar o usuário
- Todas as senhas são armazenadas localmente no banco de dados SQLite
