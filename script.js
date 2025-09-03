// --- CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE ---
// Para usar variáveis de ambiente no Netlify, você deve configurar no painel admin.
// Esta função busca o número de telefone do lead da variável de ambiente LEAD_PHONE_NUMBER
// Caso a variável não esteja definida, usa um número padrão para desenvolvimento.
function getLeadPhoneNumber() {
    // No Netlify, as variáveis de ambiente são injetadas durante o build via process.env
    // Para JavaScript do frontend, precisamos usar uma abordagem diferente
    // O número deve ser configurado nas Environment Variables do Netlify
    
    // Número padrão para desenvolvimento (será substituído pela variável de ambiente)
    const DEFAULT_LEAD_PHONE = '553288654795';
    
    // Em produção no Netlify, use a variável de ambiente LEAD_PHONE_NUMBER
    // que pode ser configurada em Site Settings > Environment Variables
    const LEAD_PHONE = '%%LEAD_PHONE_NUMBER%%' || DEFAULT_LEAD_PHONE;
    
    // Remove caracteres não numéricos
    return LEAD_PHONE.replace(/[^\d]/g, '');
}

// --- LÓGICA DO REDIRECIONADOR AUTOMÁTICO COM DELAY ---
// 1. Lista com os seus links do WhatsApp usando a variável de ambiente
const leadPhone = getLeadPhoneNumber();
const whatsappLinks = [
    `https://api.whatsapp.com/send/?phone=${leadPhone}&text=Resgatar%20convite%20da%20Imersão%20-%20Mayara%20Fogaça%20e%20Pablo%20Marçal`, // Número principal
    `https://api.whatsapp.com/send/?phone=554391386878&text=Resgatar%20convite%20da%20Imersão%20-%20Mayara%20Fogaça%20e%20Pablo%20Marçal`  // Número secundário (backup)
];

// 2. Pega o contador de acessos do localStorage.
let accessCount = parseInt(localStorage.getItem('whatsappAccessCount')) || 0;

// 3. Calcula qual link usar.
const linkParaRedirecionar = whatsappLinks[accessCount % whatsappLinks.length];

// 4. Mostra no console o link que será aberto (bom para depuração).
console.log(`Acesso #${accessCount + 1}: Redirecionando para ${linkParaRedirecionar} em 5 segundos.`);
console.log(`Lead phone number: ${leadPhone}`);

// 5. Incrementa e salva o contador para o próximo acesso.
accessCount++;
localStorage.setItem('whatsappAccessCount', accessCount);

// --- LÓGICA DA CONTAGEM REGRESSIVA ---
let segundosRestantes = 5;
const countdownElement = document.getElementById('countdown');

const countdownInterval = setInterval(() => {
    segundosRestantes--;
    if (countdownElement) {
        countdownElement.textContent = segundosRestantes;
    }
    if (segundosRestantes <= 0) {
        clearInterval(countdownInterval);
    }
}, 1000);

// --- LÓGICA DO CONTADOR DE FILA COM PICOS ALEATÓRIOS ---
let pessoasNaFila = 298; // Valor inicial atualizado
const maxPessoas = 495; // Limite máximo atualizado
const filaElement = document.getElementById('fila-counter');
const saltos = [7, 11, 15, 20]; // Valores dos picos de contagem

function atualizarFila() {
    // Condição de parada: se atingiu ou passou o máximo, para a simulação.
    if (pessoasNaFila >= maxPessoas) {
        if (filaElement) {
            filaElement.textContent = maxPessoas; // Garante que o número final seja 495
        }
        return; // Para a função
    }

    // Calcula o próximo salto aleatório
    const salto = saltos[Math.floor(Math.random() * saltos.length)];
    pessoasNaFila += salto;

    // Se passar do máximo, ajusta para o valor exato
    if (pessoasNaFila > maxPessoas) {
        pessoasNaFila = maxPessoas;
    }

    // Atualiza o número na tela
    if (filaElement) {
        filaElement.textContent = pessoasNaFila;
    }

    // Define um tempo aleatório para a próxima atualização (entre 250ms e 650ms)
    const proximoIntervalo = Math.random() * 400 + 250;
    setTimeout(atualizarFila, proximoIntervalo);
}

// Inicia o contador da fila
atualizarFila();

// --- REDIRECIONAMENTO ---
// Redireciona o usuário após 5 segundos (5000 milissegundos).
setTimeout(() => {
    window.location.href = linkParaRedirecionar;
}, 5000);
