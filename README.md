# Mayara Fogaça - Redirecionador de Leads

Este repositório contém uma aplicação web simples para redirecionamento automático de leads para WhatsApp com contador de fila dinâmico.

## Estrutura do Projeto

- **index.html** - Página principal com interface de redirecionamento
- **script.js** - Lógica JavaScript para redirecionamento e contadores
- **style.css** - Estilos da aplicação
- **config.py** - Configuração Python para gerenciamento de variáveis de ambiente
- **wtz-thumb-mayara.png** - Imagem da interface

## Funcionalidades

1. **Redirecionamento Automático**: Redireciona usuários após 5 segundos para WhatsApp
2. **Contador de Fila Dinâmico**: Simula pessoas na fila com atualizações aleatórias
3. **Rotação de Números**: Alterna entre números de WhatsApp baseado em acessos
4. **Suporte a Variáveis de Ambiente**: Configuração flexível do número principal via `LEAD_PHONE_NUMBER`

## Configuração de Variáveis de Ambiente

### Para Netlify (Recomendado)

O sistema foi otimizado para deploy no Netlify. Para configurar:

1. **Acesse o painel do Netlify**:
   - Vá para seu site no Netlify Dashboard
   - Clique em "Site settings" > "Environment variables"

2. **Adicione a variável**:
   - Nome: `LEAD_PHONE_NUMBER`
   - Valor: Seu número de telefone (apenas dígitos, ex: `5511999999999`)

3. **Redeploy o site**:
   - Vá para "Deploys" e clique em "Trigger deploy" > "Deploy site"

### Para Desenvolvimento Local

Se a variável não estiver configurada, o sistema usará o número padrão definido no código (`553288654795`).

## Como o Sistema de Variáveis Funciona

### No JavaScript (Frontend)

O arquivo `script.js` contém:

```javascript
function getLeadPhoneNumber() {
    // Número padrão para desenvolvimento
    const DEFAULT_LEAD_PHONE = '553288654795';
    
    // Em produção no Netlify, usará a variável de ambiente
    const LEAD_PHONE = '%%LEAD_PHONE_NUMBER%%' || DEFAULT_LEAD_PHONE;
    
    return LEAD_PHONE.replace(/[^\d]/g, '');
}
```

**Importante**: O placeholder `%%LEAD_PHONE_NUMBER%%` é substituído automaticamente pelo Netlify durante o build se a variável estiver configurada.

### No Python (Backend - Opcional)

O arquivo `config.py` fornece uma classe Python para gerenciamento mais avançado:

```python
from config import Config

# Modo produção (requer variável)
config = Config(require_env_var=True)
phone = config.get_lead_phone_number()

# Modo desenvolvimento (usa padrão se não encontrar)
config = Config(require_env_var=False)
phone = config.get_lead_phone_number()
```

## Deploy no Netlify

### Método 1: Conectar Repositório GitHub

1. Faça login no [Netlify](https://www.netlify.com/)
2. Clique em "New site from Git"
3. Conecte sua conta GitHub e selecione este repositório
4. Configure as variáveis de ambiente conforme descrito acima
5. Deploy automaticamente

### Método 2: Deploy Manual

1. Faça download dos arquivos do repositório
2. Faça upload da pasta no Netlify (drag & drop)
3. Configure as variáveis de ambiente

## Estrutura do Redirecionamento

O sistema funciona com dois números de WhatsApp:

1. **Número Principal**: Definido pela variável `LEAD_PHONE_NUMBER`
2. **Número Secundário (Backup)**: Hardcoded como `554391386878`

Os acessos são alternados entre os dois números usando `localStorage` para rastreamento.

## Personalização

### Alterar Tempo de Redirecionamento

Em `script.js`, modifique:

```javascript
// Alterar de 5 para X segundos
setTimeout(() => {
    window.location.href = linkParaRedirecionar;
}, 5000); // 5000ms = 5 segundos
```

### Alterar Mensagem do WhatsApp

Em `script.js`, modifique o texto na URL:

```javascript
const whatsappLinks = [
    `https://api.whatsapp.com/send/?phone=${leadPhone}&text=SUA_MENSAGEM_AQUI`,
    `https://api.whatsapp.com/send/?phone=554391386878&text=SUA_MENSAGEM_AQUI`
];
```

### Alterar Parâmetros da Fila

Em `script.js`:

```javascript
let pessoasNaFila = 298; // Valor inicial
const maxPessoas = 495;  // Valor máximo
const saltos = [7, 11, 15, 20]; // Incrementos aleatórios
```

## Troubleshooting

### Variável de Ambiente Não Funciona

1. Verifique se a variável está corretamente nomeada: `LEAD_PHONE_NUMBER`
2. Certifique-se de que contém apenas dígitos (sem espaços, hífens, parênteses)
3. Faça um novo deploy após adicionar a variável

### Redirecionamento Não Funciona

1. Verifique o console do navegador para erros JavaScript
2. Confirme se o número do WhatsApp está no formato correto
3. Teste a URL do WhatsApp manualmente

### Contador da Fila Não Atualiza

1. Verifique se o elemento HTML tem o ID correto: `fila-counter`
2. Confirme se não há erros JavaScript no console

## Suporte

Para dúvidas ou problemas:

1. Verifique os logs do Netlify em "Site settings" > "Functions"
2. Use o console do navegador (F12) para debug JavaScript
3. Consulte a documentação do [Netlify Environment Variables](https://docs.netlify.com/environment-variables/overview/)

---

**Última atualização**: Setembro 2025  
**Versão**: 2.0 - Com suporte a variáveis de ambiente

<!-- Deploy trigger: Sept 3, 2025, 5:40 PM - Trigger Netlify redeploy -->
