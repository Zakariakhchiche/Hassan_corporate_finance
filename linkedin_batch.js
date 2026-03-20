const posts = [
    {
        "text": "Les chatbots simples sont MORTS. En 2026, la révolution, ce sont les AGENTS AUTONOMES. Contrairement aux chatbots qui répondent, les agents agissent, planifient et utilisent vos outils. C'est ce que je fais avec Hassan, mon assistant OpenClaw. Et vous, votre IA parle ou agit ?\n#IA #AgentsIA #Automation #OpenClaw",
        "date": "16/02/2026",
        "time": "09:00"
    },
    {
        "text": "Plus gros n'est plus synonyme de meilleur. Les SLMs comme Phi-4 ou Mistral gagnent du terrain : Confidentialité (local), Vitesse (latence nulle), Coût réduit. Pas besoin d'un moteur de Boeing pour une citadine. Testez-vous des modèles locaux ?\n#SLM #MistralAI #EdgeComputing",
        "date": "17/02/2026",
        "time": "09:00"
    },
    {
        "text": "\"Garbage In, Garbage Out\". L'IA la plus puissante ne vaut rien sur des données corrompues. Le Data Cleaning est devenu une orchestration automatisée : détection d'anomalies en temps réel et déduplication intelligente. La qualité est votre socle.\n#DataQuality #DataEngineering #BigData",
        "date": "18/02/2026",
        "time": "09:00"
    },
    {
        "text": "Regagnez 10h par semaine. Les Agentic Workflows gèrent vos emails, extraient des insights de rapports massifs et planifient vos rendez-vous. Déléguez le répétitif pour libérer votre créativité. Quelle tâche délégueriez-vous à un gorille numérique ? 🦍\n#Automation #Productivité #HassanTheGorilla",
        "date": "19/02/2026",
        "time": "09:00"
    },
    {
        "text": "Fini les pipelines rigides, place à l'Orchestration Dynamique. Auto-healing, scaling prédictif et interconnexion totale. Le Data Engineer devient architecte de flux. Prêt pour l'étape suivante ?\n#DataEngineering #ModernDataStack #Infrastructure",
        "date": "20/02/2026",
        "time": "09:00"
    }
];

async function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

async function schedulePost(post) {
    console.log(`Scheduling post for ${post.date}...`);
    
    // Open post dialog
    const startBtn = document.querySelector('button.share-mb-launcher') || document.querySelector('button:has-text("Commencer un post")');
    if (!startBtn) { console.error("Start button not found"); return; }
    startBtn.click();
    await sleep(2000);
    
    // Fill text
    const editor = document.querySelector('div[role="textbox"]');
    if (!editor) { console.error("Editor not found"); return; }
    editor.innerText = post.text;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    await sleep(1000);
    
    // Click clock
    const clockBtn = document.querySelector('button[aria-label="Programmer pour plus tard"]');
    if (!clockBtn) { console.error("Clock button not found"); return; }
    clockBtn.click();
    await sleep(1000);
    
    // Set date/time
    const dateInput = document.querySelector('input[type="date"]');
    const timeInput = document.querySelector('input[type="time"]');
    if (dateInput && timeInput) {
        const [d, m, y] = post.date.split('/');
        dateInput.value = `${y}-${m}-${d}`;
        timeInput.value = post.time;
        dateInput.dispatchEvent(new Event('input', { bubbles: true }));
        timeInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
    await sleep(1000);
    
    // Click Next
    const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Suivant'));
    if (nextBtn) nextBtn.click();
    await sleep(1000);
    
    // Click Schedule
    const scheduleBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Programmer'));
    if (scheduleBtn) scheduleBtn.click();
    await sleep(3000);
}

async function runAll() {
    for (const post of posts) {
        await schedulePost(post);
        await sleep(2000);
    }
    alert("Tous les posts ont été programmés !");
}

runAll();
