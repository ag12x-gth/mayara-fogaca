// --- CONFIGURAÇÃO AVANÇADA COM VALIDAÇÃO ---
/**
 * Obtém o número de telefone do lead com validação e fallback
 * @returns {string} Número de telefone validado
 */
function getLeadPhoneNumber() {
    const DEFAULT_LEAD_PHONE = '5511914988880';
    
    try {
        // Suporte futuro para variáveis de ambiente via build process
        const LEAD_PHONE = '%%LEAD_PHONE_NUMBER%%' || DEFAULT_LEAD_PHONE;
        
        // Limpa e valida o número
        const cleanPhone = LEAD_PHONE.replace(/[^\d]/g, '');
        
        // Validação básica de número de telefone brasileiro (10-13 dígitos)
        if (cleanPhone.length >= 10 && cleanPhone.length <= 13) {
            return cleanPhone;
        }
        
        console.warn('Número de telefone inválido, usando padrão:', LEAD_PHONE);
        return DEFAULT_LEAD_PHONE;
    } catch (error) {
        console.error('Erro ao obter número do lead:', error);
        return DEFAULT_LEAD_PHONE;
    }
}

// --- LÓGICA DO REDIRECIONADOR AUTOMÁTICO COM SEGURANÇA ---
/**
 * Sanitiza texto para uso em URLs, prevenindo XSS
 * @param {string} text - Texto a ser sanitizado
 * @returns {string} Texto sanitizado
 */
function sanitizeUrlText(text) {
    return encodeURIComponent(text.replace(/[<>'"&]/g, ''));
}

/**
 * Valida e constrói URL do WhatsApp com tratamento de erro
 * @param {string} phone - Número de telefone
 * @param {string} message - Mensagem a ser enviada
 * @returns {string} URL válida do WhatsApp
 */
function buildWhatsAppUrl(phone, message) {
    try {
        const cleanPhone = phone.replace(/[^\d]/g, '');
        const sanitizedMessage = sanitizeUrlText(message);
        return `https://api.whatsapp.com/send/?phone=${cleanPhone}&text=${sanitizedMessage}`;
    } catch (error) {
        console.error('Erro ao construir URL do WhatsApp:', error);
        return `https://api.whatsapp.com/send/?phone=${phone}`;
    }
}

// 1. Configuração segura dos links do WhatsApp
const leadPhone = getLeadPhoneNumber();
const defaultMessage = 'Resgatar convite da Imersão - Mayara Fogaça e Pablo Marçal';

const whatsappLinks = [
    buildWhatsAppUrl(leadPhone, defaultMessage) // Número principal com sanitização
];

// 2. Gerenciamento seguro do localStorage com tratamento de erro
function getAccessCount() {
    try {
        const count = parseInt(localStorage.getItem('whatsappAccessCount')) || 0;
        return isNaN(count) ? 0 : count;
    } catch (error) {
        console.warn('Erro ao acessar localStorage:', error);
        return 0;
    }
}

function setAccessCount(count) {
    try {
        localStorage.setItem('whatsappAccessCount', count.toString());
    } catch (error) {
        console.warn('Erro ao salvar no localStorage:', error);
    }
}

let accessCount = getAccessCount();

// 3. Seleção segura do link de redirecionamento
const linkParaRedirecionar = whatsappLinks[accessCount % whatsappLinks.length];

// 4. Log estruturado para depuração
console.group('🔗 Configuração de Redirecionamento');
console.log(`📊 Acesso #${accessCount + 1}`);
console.log(`📱 Lead phone: ${leadPhone}`);
console.log(`🎯 Redirecionando para: ${linkParaRedirecionar}`);
console.log(`⏱️ Tempo de espera: 5 segundos`);
console.groupEnd();

// 5. Incremento e persistência do contador
accessCount++;
setAccessCount(accessCount);

// --- LÓGICA DA CONTAGEM REGRESSIVA OTIMIZADA ---
/**
 * Gerencia a contagem regressiva com tratamento de erro
 * @param {number} initialSeconds - Segundos iniciais
 * @param {HTMLElement} element - Elemento DOM do contador
 * @param {Function} onComplete - Callback ao completar
 */
function startCountdown(initialSeconds, element, onComplete) {
    let segundosRestantes = initialSeconds;
    
    const updateDisplay = () => {
        if (element && typeof element.textContent !== 'undefined') {
            element.textContent = segundosRestantes;
        }
    };
    
    const countdownInterval = setInterval(() => {
        segundosRestantes--;
        updateDisplay();
        
        if (segundosRestantes <= 0) {
            clearInterval(countdownInterval);
            if (typeof onComplete === 'function') {
                onComplete();
            }
        }
    }, 1000);
    
    // Atualização inicial
    updateDisplay();
    
    return countdownInterval;
}

// Inicialização segura da contagem regressiva
const countdownElement = document.getElementById('countdown');
if (countdownElement) {
    startCountdown(5, countdownElement, () => {
        console.log('⏰ Contagem regressiva concluída');
    });
} else {
    console.warn('⚠️ Elemento countdown não encontrado');
}

// --- LÓGICA DO CONTADOR DE FILA OTIMIZADA ---
/**
 * Configuração do sistema de fila com validação
 */
const FILA_CONFIG = {
    inicial: 298,
    maximo: 495,
    saltos: [7, 11, 15, 20],
    intervaloMin: 250,
    intervaloMax: 650
};

/**
 * Classe para gerenciar o contador de fila de forma otimizada
 */
class FilaManager {
    constructor(config, elementId) {
        this.config = config;
        this.pessoasNaFila = config.inicial;
        this.element = document.getElementById(elementId);
        this.isRunning = false;
        
        if (!this.element) {
            console.warn(`⚠️ Elemento ${elementId} não encontrado`);
        }
    }
    
    /**
     * Atualiza o display da fila de forma segura
     */
    updateDisplay() {
        if (this.element && typeof this.element.textContent !== 'undefined') {
            this.element.textContent = this.pessoasNaFila;
        }
    }
    
    /**
     * Calcula o próximo salto de forma aleatória
     */
    getRandomJump() {
        const { saltos } = this.config;
        return saltos[Math.floor(Math.random() * saltos.length)];
    }
    
    /**
     * Calcula o próximo intervalo de atualização
     */
    getRandomInterval() {
        const { intervaloMin, intervaloMax } = this.config;
        return Math.random() * (intervaloMax - intervaloMin) + intervaloMin;
    }
    
    /**
     * Inicia a simulação da fila
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateDisplay();
        this.scheduleNext();
        
        console.log('🎯 Simulação de fila iniciada');
    }
    
    /**
     * Para a simulação da fila
     */
    stop() {
        this.isRunning = false;
        console.log('⏹️ Simulação de fila interrompida');
    }
    
    /**
     * Agenda a próxima atualização
     */
    scheduleNext() {
        if (!this.isRunning) return;
        
        // Verifica se atingiu o máximo
        if (this.pessoasNaFila >= this.config.maximo) {
            this.pessoasNaFila = this.config.maximo;
            this.updateDisplay();
            this.stop();
            console.log('🏁 Fila atingiu o máximo:', this.config.maximo);
            return;
        }
        
        // Calcula próximo salto
        const salto = this.getRandomJump();
        this.pessoasNaFila += salto;
        
        // Ajusta se passou do máximo
        if (this.pessoasNaFila > this.config.maximo) {
            this.pessoasNaFila = this.config.maximo;
        }
        
        this.updateDisplay();
        
        // Agenda próxima atualização
        const proximoIntervalo = this.getRandomInterval();
        setTimeout(() => this.scheduleNext(), proximoIntervalo);
    }
}

// Inicialização do gerenciador de fila
const filaManager = new FilaManager(FILA_CONFIG, 'fila-counter');
filaManager.start();

// --- REDIRECIONAMENTO AVANÇADO COM FALLBACKS ---
/**
 * Executa redirecionamento com fallbacks e tratamento de erro
 * @param {string} url - URL de destino
 * @param {number} delay - Delay em milissegundos
 */
function performRedirect(url, delay = 5000) {
    console.group('🚀 Iniciando redirecionamento');
    console.log(`🎯 URL: ${url}`);
    console.log(`⏱️ Delay: ${delay}ms`);
    
    const redirectTimeout = setTimeout(() => {
        try {
            // Verificação de segurança da URL
            const urlObj = new URL(url);
            if (!['https:', 'http:'].includes(urlObj.protocol)) {
                throw new Error('Protocolo não permitido');
            }
            
            console.log('✅ Executando redirecionamento...');
            window.location.href = url;
            
        } catch (error) {
            console.error('❌ Erro no redirecionamento:', error);
            
            // Fallback: mostrar link manual
            showManualRedirectOption(url);
        }
    }, delay);
    
    console.groupEnd();
    
    // Retorna função para cancelar se necessário
    return () => clearTimeout(redirectTimeout);
}

/**
 * Mostra opção de redirecionamento manual em caso de falha
 * @param {string} url - URL de destino
 */
function showManualRedirectOption(url) {
    const container = document.querySelector('.container');
    if (container) {
        const manualLink = document.createElement('div');
        manualLink.innerHTML = `
            <p style="color: #e74c3c; margin-top: 20px;">
                ⚠️ Redirecionamento automático falhou
            </p>
            <a href="${url}" 
               style="display: inline-block; background: #25D366; color: white; 
                      padding: 12px 24px; text-decoration: none; border-radius: 6px; 
                      margin-top: 10px; font-weight: bold;"
               target="_blank">
                📱 Abrir WhatsApp Manualmente
            </a>
        `;
        container.appendChild(manualLink);
    }
}

// Executar redirecionamento principal
const cancelRedirect = performRedirect(linkParaRedirecionar, 5000);

// Cleanup em caso de navegação ou erro
window.addEventListener('beforeunload', () => {
    if (typeof cancelRedirect === 'function') {
        cancelRedirect();
    }
});

// --- MONITORAMENTO E ANALYTICS APRIMORADOS ---
/**
 * Envia evento personalizado para Google Analytics
 * @param {string} eventName - Nome do evento
 * @param {Object} eventData - Dados do evento
 */
function trackEvent(eventName, eventData = {}) {
    try {
        if (typeof gtag === 'function') {
            gtag('event', eventName, {
                custom_parameter: true,
                ...eventData
            });
            console.log(`📊 Evento rastreado: ${eventName}`, eventData);
        }
    } catch (error) {
        console.warn('⚠️ Erro no tracking:', error);
    }
}

// Rastreamento de eventos importantes
trackEvent('page_load', {
    lead_phone: leadPhone,
    access_count: accessCount
});

trackEvent('redirect_scheduled', {
    target_url: linkParaRedirecionar,
    delay_seconds: 5
});
