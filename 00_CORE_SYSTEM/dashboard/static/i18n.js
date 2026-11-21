/**
 * i18n.js — Master AI Universal Tri-Lingual Engine
 * Powered by Zovron Technologies
 * Supports: Hindi (हिन्दी), Hinglish (रोमन हिंदी), and English
 */

const I18N_DICTIONARY = {
  hindi: {
    brand_sub: "पावर्ड बाय ज़ोवरॉन टेक्नोलॉजीज",
    nav_studio: "रील स्टूडियो",
    nav_vault: "वॉइस वॉल्ट",
    nav_coder: "वेब कोडर",
    nav_automation: "ऑटोमेशन",
    badge_live: "लाइव",
    badge_coming_soon: "जल्द आ रहा है (v2.5)",
    
    studio_title: "स्वायत्त 2D कैरेक्टर रील स्टूडियो",
    studio_desc: "1080x1920 वायरल रील्स बनाएं - लॉक्ड कैरेक्टर रिग्स, लिप-सिंक व शून्य-ओवरफ्लो सबटाइटल्स के साथ।",
    config_title: "रील कॉन्फ़िगरेशन",
    
    label_topic: "वीडियो का मुख्य विषय / हुक",
    placeholder_topic: "उदा. Claude Code on Mobile Termux",
    label_creator_name: "क्रिएटर का नाम / हैंडल",
    label_creator_role: "क्रिएटर का रोल / पद",
    preview_badge_label: "टर्मिनल हेडर बैज:",
    
    label_character: "कैरेक्टर चुनें",
    label_voice_engine: "वॉइस इंजन चुनें",
    btn_audition: "ऑडियो सैंपल सुनें",
    
    label_save_path: "वीडियो सेव फोल्डर (डायनामिक पाथ)",
    save_path_hint: "आपके डेस्कटॉप या मोबाइल के डाउनलोड फोल्डर में स्वतः सेव होगा।",
    
    label_cta: "कॉल टू एक्शन (CTA)",
    placeholder_cta: "उदा. Comment TERMUX for Full Guide",
    
    btn_generate_reel: "⚡ 1080x1920 AI रील रेंडर करें (लाइव पाइपलाइन)",
    btn_rendering: "⏳ रेंडर हो रहा है... कृपया प्रतीक्षा करें",
    
    preview_title: "लाइव रील प्रीव्यू और प्लेयर",
    preview_empty: "अभी कोई वीडियो रेंडर नहीं हुई है। विषय डालकर ऊपर Generate बटन दबाएं!",
    library_title: "आपकी रेंडर्ड वीडियो लाइब्रेरी",
    library_empty: "अभी कोई रेंडर्ड वीडियो उपलब्ध नहीं है।",
    
    // Voice Vault
    vault_title: "मल्टी-प्रोवाइडर वॉइस वॉल्ट (Voice Vault)",
    vault_desc: "सख्त हायरार्की: 1. Gemini TTS ➔ 2. ElevenLabs ➔ 3. Sarvam AI। कोटा खत्म होने पर ऑटोमैटिक स्विच!",
    btn_add_key: "नई API Key जोड़ें",
    
    // Coming soon
    coder_title: "ऑटोनॉमस वेब कोडर और स्केफोल्डर",
    coder_desc: "फुल-स्टैक आर्किटेक्चर जनरेटर और कोड असिस्टेंट।",
    coder_badge: "🚀 विकास जारी है — संस्करण 2.5 में उपलब्ध होगा",
    coder_notice: "यह मॉड्यूल वर्तमान में विकास के अंतिम चरण में है। शीघ्र ही आप इससे पूरे वेब प्रोजेक्ट्स और बैकएंड कोड जनरेट कर पाएंगे।",
    
    automation_title: "मल्टी-एजेंट वर्कफ़्लो और ऑटोमेशन",
    automation_desc: "स्वायत्त सोशल मीडिया ग्रोथ फनल और जॉब रनर।",
    automation_badge: "⚡ विकास जारी है — संस्करण 2.5 में उपलब्ध होगा",
    automation_notice: "यह मॉड्यूल अगली रिलीज़ में उपलब्ध होगा। आप ऑटोमैटिक डीएम, कंटेंट शेड्यूलिंग और एनालिटिक्स ट्रैक कर सकेंगे।",
    btn_notify: "रोडमैप देखें / अपडेट के लिए रजिस्टर करें"
  },

  hinglish: {
    brand_sub: "Powered by Zovron Technologies",
    nav_studio: "Reel Studio",
    nav_vault: "Voice Vault",
    nav_coder: "Web Coder",
    nav_automation: "Automation",
    badge_live: "LIVE",
    badge_coming_soon: "Coming Soon (v2.5)",
    
    studio_title: "Autonomous 2D Character Reel Studio",
    studio_desc: "1080x1920 viral reels banayein — locked character rigs, lip-sync aur zero-overflow subtitles ke saath.",
    config_title: "Reel Configuration",
    
    label_topic: "Video Topic / Core Hook",
    placeholder_topic: "e.g. Claude Code on Mobile Termux",
    label_creator_name: "Creator Name / Handle",
    label_creator_role: "Creator Role / Title",
    preview_badge_label: "Terminal header badge:",
    
    label_character: "Character Archetype Chunein",
    label_voice_engine: "Voice Engine Selection",
    btn_audition: "Audition Sample",
    
    label_save_path: "Video Save Folder (Dynamic Path)",
    save_path_hint: "Desktop ya mobile ke Downloads folder me auto-save hoga.",
    
    label_cta: "Call To Action (CTA)",
    placeholder_cta: "e.g. Comment TERMUX for Full Guide",
    
    btn_generate_reel: "⚡ 1080x1920 AI Reel Render Karein (Live Pipeline)",
    btn_rendering: "⏳ Rendering in progress... Please wait",
    
    preview_title: "Live Reel Preview & Player",
    preview_empty: "Abhi koi video render nahi hui hai. Topic enter karke Generate button dabayein!",
    library_title: "Aapki Rendered Video Library",
    library_empty: "Abhi koi rendered video available nahi hai.",
    
    // Voice Vault
    vault_title: "Multi-Provider Voice Vault",
    vault_desc: "Strict Hierarchy: 1. Gemini TTS ➔ 2. ElevenLabs ➔ 3. Sarvam AI. Quota khatam hone par automatic switch!",
    btn_add_key: "Add New API Key",
    
    // Coming soon
    coder_title: "Autonomous Web Coder & Scaffolder",
    coder_desc: "Full-stack architecture scaffolding aur code generation agent.",
    coder_badge: "🚀 In Active Development — Release in v2.5",
    coder_notice: "Ye module current update me development phase me hai. Version 2.5 me aap yahan se direct full-stack projects generate kar sakenge.",
    
    automation_title: "Multi-Agent Workflow & Growth Automation",
    automation_desc: "Autonomous social media funnel automation aur growth engine.",
    automation_badge: "⚡ In Active Development — Release in v2.5",
    automation_notice: "Ye module next major release me live hoga. Auto-DM, content scheduler aur analytics auto-track honge.",
    btn_notify: "View Roadmap / Early Access"
  },

  english: {
    brand_sub: "Powered by Zovron Technologies",
    nav_studio: "Reel Studio",
    nav_vault: "Voice Vault",
    nav_coder: "Web Coder",
    nav_automation: "Automation",
    badge_live: "LIVE",
    badge_coming_soon: "Coming Soon (v2.5)",
    
    studio_title: "Autonomous 2D Character Reel Studio",
    studio_desc: "Produce broadcast-grade 1080x1920 viral reels with locked character rigs, lip-sync, and zero-overflow subtitles.",
    config_title: "Reel Configuration",
    
    label_topic: "Topic / Core Hook",
    placeholder_topic: "e.g. Claude Code on Mobile Termux",
    label_creator_name: "Creator Name / Handle",
    label_creator_role: "Creator Role / Title",
    preview_badge_label: "Terminal header badge:",
    
    label_character: "Select Character Archetype",
    label_voice_engine: "Voice Engine Selection",
    btn_audition: "Audition Sample",
    
    label_save_path: "Save Video To Folder (Dynamic Path)",
    save_path_hint: "Auto-saved to your Desktop or Mobile Downloads folder.",
    
    label_cta: "Call To Action (CTA)",
    placeholder_cta: "e.g. Comment TERMUX for Full Guide",
    
    btn_generate_reel: "⚡ Render 1080x1920 AI Reel (Live Pipeline)",
    btn_rendering: "⏳ Rendering in progress... Please wait",
    
    preview_title: "Live Reel Preview & Player",
    preview_empty: "No video rendered yet. Enter a topic and tap Generate Reel!",
    library_title: "Your Rendered Library",
    library_empty: "No rendered videos available yet.",
    
    // Voice Vault
    vault_title: "Multi-Provider Voice Vault",
    vault_desc: "Strict Failover Hierarchy: 1. Gemini TTS ➔ 2. ElevenLabs ➔ 3. Sarvam AI. Auto-switches on quota limit!",
    btn_add_key: "Add New API Key",
    
    // Coming soon
    coder_title: "Autonomous Web Coder & Scaffolder",
    coder_desc: "Instant architecture scaffolding, boilerplate generation, and UI components.",
    coder_badge: "🚀 In Active Development — Target Release v2.5",
    coder_notice: "This specialist agent module is currently under active engineering. It will provide autonomous full-stack repo scaffolding in version 2.5.",
    
    automation_title: "Multi-Agent Growth & Task Automation",
    automation_desc: "Autonomous social media funnel automation, Auto-DM dispatch, and scheduler.",
    automation_badge: "⚡ In Active Development — Target Release v2.5",
    automation_notice: "This automation module will go live in the upcoming release. You will be able to orchestrate viral distribution workflows automatically.",
    btn_notify: "View Roadmap / Early Access"
  }
};

let currentLanguage = localStorage.getItem('preferred_language') || 'hinglish';

function setLanguage(lang) {
  if (!I18N_DICTIONARY[lang]) return;
  currentLanguage = lang;
  localStorage.setItem('preferred_language', lang);
  
  // Update toggle pills in UI
  ['hindi', 'hinglish', 'english'].forEach(l => {
    const el = document.getElementById(`lang-btn-${l}`);
    if (el) {
      if (l === lang) {
        el.className = "px-2 py-1 rounded-md text-[10px] font-bold bg-tech-cyan text-black shadow-sm transition-all";
      } else {
        el.className = "px-2 py-1 rounded-md text-[10px] font-medium text-slate-400 hover:text-white transition-all";
      }
    }
  });

  // Apply texts
  const dict = I18N_DICTIONARY[lang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = dict[key];
      } else {
        el.textContent = dict[key];
      }
    }
  });
  window.setLanguage = setLanguage;
}

window.setLanguage = setLanguage;

document.addEventListener('DOMContentLoaded', () => {
  setLanguage(currentLanguage);
});
