"""
Enterprise Phonetic & Multilingual Normalization Engine for Master AI
=====================================================================
Version: 2.1.0-enterprise
Features:
1. Algorithmic Zero-Shot Acronym Expansion:
   - Any unknown uppercase acronym (e.g. JWT, CORS, VPC, SLA, KPI, B2B) is
     automatically hyphenated and converted to clean Devanagari phonetics.
2. Dynamic JSON-backed Knowledge Lexicon:
   - Loads from `phonetic_lexicon.json` with hundreds of pre-compiled tech,
     corporate, and dev jargon terms.
3. Self-Expanding Dynamic Learning:
   - `register_word()` and `scan_script()` allow adding or auto-learning new
     words on the fly for any future video.
4. Cross-Lingual Homograph Disambiguation:
   - 'use' (verb vs pronoun 'उसे'), 'to', 'is', 'in', 'us', 'mat', 'par', 'or'.
5. Syllable Boundary Preservation:
   - Fixes Devanagari 4-consonant cluster drops ('सब्सक्रिप्शन' -> 'सब-स्क्रिप्शन').
6. Human Breath & Pacing Normalization:
   - Eliminates robotic stutters, micro-pauses, and trailing voice fades.
"""

import json
import os
import re
from typing import Dict, Any, List, Optional, Tuple

LEXICON_PATH = os.path.join(os.path.dirname(__file__), "phonetic_lexicon.json")


class PhoneticNormalizer:
    def __init__(self, lexicon_path: str = LEXICON_PATH):
        self.lexicon_path = lexicon_path
        self.load_lexicon()

        # Regex rules for currencies, numbers, and scale multipliers
        self.scale_multipliers = [
            (r"\$(\d+(?:\.\d+)?)\s*[kK]\b", r"\1 हज़ार डॉलर"),
            (r"\$(\d+(?:\.\d+)?)\s*[mM]\b", r"\1 मिलियन डॉलर"),
            (r"\$(\d+(?:\.\d+)?)\s*[bB]\b", r"\1 बिलियन डॉलर"),
            (r"\$(\d+(?:\.\d+)?)", r"\1 डॉलर"),
            (r"₹(\d+(?:\.\d+)?)\s*[kK]\b", r"\1 हज़ार रुपया"),
            (r"₹(\d+(?:\.\d+)?)\s*[lL]\b", r"\1 लाख रुपया"),
            (r"₹(\d+(?:\.\d+)?)\s*[cC][rR]\b", r"\1 करोड़ रुपया"),
            (r"₹(\d+(?:\.\d+)?)", r"\1 रुपया"),
            (r"(\d+)\s*[xX]\b", r"\1 गुना"),
            (r"(\d+)\s*(?:GB|gb)\b", r"\1 जी-बी"),
            (r"(\d+)\s*(?:MB|mb)\b", r"\1 एम-बी"),
            (r"(\d+)\s*(?:TB|tb)\b", r"\1 टी-बी"),
            (r"(\d+)\s*(?:KB|kb)\b", r"\1 के-बी"),
            (r"(\d+(?:\.\d+)?)\s*(?:vCPU|vcpu)\b", r"\1 वी-सी-पी-यू"),
            (r"(\d+)\s*(?:ms|millisec|milliseconds)\b", r"\1 मिली-सेकंड"),
            (r"(\d+)\s*(?:sec|secs|seconds)\b", r"\1 सेकंड"),
            (r"(\d+)\s*(?:min|mins|minutes)\b", r"\1 मिनट"),
            (r"(\d+)\s*(?:hr|hrs|hours)\b", r"\1 घंटे"),
            (r"\b24/7\b", "चौबीसों घंटे"),
            (r"100%", "सौ परसेंट"),
            (r"50%", "पचास परसेंट"),
            (r"0%", "जीरो परसेंट"),
            (r"\b0ms\b", "जीरो मिली-सेकंड"),
            (r"\b0MB\b", "जीरो एम-बी"),
            (r"\b0GB\b", "जीरो जी-बी"),
        ]

    def load_lexicon(self):
        """Loads or reloads the JSON phonetic dictionary."""
        if os.path.exists(self.lexicon_path):
            with open(self.lexicon_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        self.exceptions_as_words = data.get("acronym_exceptions_as_words", {})
        self.tech_tools = data.get("tech_tools_and_frameworks", {})
        self.corporate_slang = data.get("corporate_and_startup_slang", {})
        self.hinglish_words = data.get("everyday_hinglish_loanwords", {})
        self.grammar_words = data.get("hindi_conversational_grammar", {})
        self.cluster_splits = data.get("consonant_cluster_splits", {})
        self.alpha_map = data.get(
            "alphabetic_spelling_map",
            {
                "A": "ए", "B": "बी", "C": "सी", "D": "डी", "E": "ई", "F": "एफ",
                "G": "जी", "H": "एच", "I": "आई", "J": "जे", "K": "के", "L": "एल",
                "M": "एम", "N": "एन", "O": "ओ", "P": "पी", "Q": "क्यू", "R": "आर",
                "S": "एस", "T": "टी", "U": "यू", "V": "वी", "W": "डब्लू", "X": "एक्स",
                "Y": "वाई", "Z": "ज़ेड", "0": "जीरो", "1": "वन", "2": "टू",
                "3": "थ्री", "4": "फोर", "5": "फाइव", "6": "सिक्स", "7": "सेवन",
                "8": "एट", "9": "नाइन",
            },
        )

    def register_word(self, word: str, phonetic_spelling: str, category: str = "tech_tools_and_frameworks"):
        """
        Dynamically registers any new word or phrase into the persistent JSON dictionary.
        Future videos will automatically use this pronunciation.
        """
        if not os.path.exists(self.lexicon_path):
            data = {}
        else:
            with open(self.lexicon_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        if category not in data:
            data[category] = {}

        data[category][word] = phonetic_spelling

        with open(self.lexicon_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.load_lexicon()
        return True

    def algorithmic_expand_acronym(self, match: re.Match) -> str:
        """
        Zero-shot algorithmic acronym expander.
        Takes ANY uppercase sequence (e.g. JWT, CI/CD, VPC, B2B, OKR, KPI)
        and converts it into phonetic hyphenated syllables (e.g. जे-डब्लू-टी).
        """
        token = match.group(0)

        # 1. Check if it's an acronym pronounced as a whole word (e.g. SaaS, RAM, NASA, CRUD)
        if token in self.exceptions_as_words:
            return self.exceptions_as_words[token]

        # 2. Check if it's already in tech tools
        if token in self.tech_tools:
            return self.tech_tools[token]

        # 3. Handle slash-separated acronyms (e.g. CI/CD)
        if "/" in token:
            parts = token.split("/")
            expanded_parts = [self.algorithmic_expand_acronym_str(p) for p in parts]
            return " ".join(expanded_parts)

        # 4. Handle hyphen-separated acronyms (e.g. B2B, P2P)
        return self.algorithmic_expand_acronym_str(token)

    def algorithmic_expand_acronym_str(self, s: str) -> str:
        if s in self.exceptions_as_words:
            return self.exceptions_as_words[s]

        # Build letter-by-letter phonetic representation
        syllables = []
        for ch in s:
            if ch.upper() in self.alpha_map:
                syllables.append(self.alpha_map[ch.upper()])
            elif ch in ["-", "_"]:
                continue
            else:
                syllables.append(ch)

        if syllables:
            return "-".join(syllables)
        return s

    def normalize_dynamic_acronyms(self, text: str) -> str:
        """
        Finds all uppercase acronyms (2-6 chars, with optional digits and slashes like CI/CD, B2B, EC2)
        and expands them algorithmically if not already handled.
        Requires at least one uppercase letter so pure numbers like '50' or '10' are preserved.
        """
        pattern = r"\b(?=[A-Z0-9/]*[A-Z])[A-Z0-9]{2,6}(?:/[A-Z0-9]{2,6})*\b"
        return re.sub(pattern, self.algorithmic_expand_acronym, text)

    def normalize_homographs(self, text: str) -> str:
        """
        Contextual disambiguation for Hinglish/English collisions:
        - 'use' (English verb /juːz/ vs Hindi pronoun /ʊseː/ 'उसे')
        - 'to' (preposition vs Hindi particle 'तो')
        - 'is' / 'us' / 'in' (English verbs/pronouns vs Hindi demonstratives 'इस', 'उस', 'इन')
        - 'mat' (mat vs 'मत')
        - 'par' (par vs 'पर')
        - 'or' (conjunction 'or' vs Hindi 'और')
        """
        # 1. English 'use' as verb
        text = re.sub(
            r"\buse\s+(karo|karna|karke|karte|karta|kartin|karoge|hoga|ho|raha|rahe|sakte|sakti)\b",
            r"इस्तेमाल \1",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"\buse\s+case\b", "यूज़ केस", text, flags=re.IGNORECASE)
        text = re.sub(r"\buse\s+cases\b", "यूज़ केसेज़", text, flags=re.IGNORECASE)
        text = re.sub(r"\bdaily\s+use\b", "डेली यूज़", text, flags=re.IGNORECASE)
        text = re.sub(r"\bpersonal\s+use\b", "पर्सनल यूज़", text, flags=re.IGNORECASE)
        text = re.sub(r"\bfair\s+use\b", "फेयर यूज़", text, flags=re.IGNORECASE)

        # 2. Hindi pronoun 'use' (meaning to him/her/it)
        text = re.sub(
            r"\buse\s+(pata|bolo|batao|lagta|lagi|samajh|bhejo|dekh|dekha|mil|mila|rok|roko|chahiye|de|dobara|phir|kabhi|wapas|bhi|ek\s+baar|kisi|sabse|kuch|seedha)\b",
            r"उसे \1",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"^Use\s+", "उसे ", text)
        text = re.sub(r"([\.!\?।]\s+)Use\s+", r"\1उसे ", text)

        # 3. Devanagari mistranslations of 'use'
        text = re.sub(
            r"(टूल|सॉफ्टवेयर|लाइब्रेरी|कोड|फंक्शन|ऐप|फीचर|सर्विस|क्लाउड|डेटाबेस)\s+को\s+उसे\s+(करो|करें|करना|करके)",
            r"\1 का इस्तेमाल \2",
            text,
        )
        text = re.sub(r"\bउसे\s+(करो|करें|करना|करके|करते|सकते|सकती)\b", r"इस्तेमाल \1", text)

        # 4. Roman Hindi 'to' / 'toh' vs English 'to'
        text = re.sub(
            r"\b(agar|yadi|dekho|suno|batao|socho|pehle|ab|phir|yeh|vo)\s+to\b",
            r"\1 तो",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"\btoh\b", "तो", text, flags=re.IGNORECASE)

        # 5. Roman Hindi 'mat' vs English 'mat'
        text = re.sub(
            r"\bmat\s+(karo|socho|daro|lo|jana|bhulo|batao|rakho|bhejo|bano)\b",
            r"मत \1",
            text,
            flags=re.IGNORECASE,
        )

        # 6. Roman Hindi 'par' vs English 'par'
        text = re.sub(
            r"\b(screen|desktop|server|cloud|github|laptop|page|board|stage)\s+par\b",
            r"\1 पर",
            text,
            flags=re.IGNORECASE,
        )

        # 7. Roman casual 'or' written instead of 'aur' (and)
        text = re.sub(
            r"\s+or\s+(batao|suno|dekho|kya|bhai|sir|mam|phir|ab|hum|tum|aap)\b",
            r" और \1",
            text,
            flags=re.IGNORECASE,
        )

        return text

    def normalize_lexicon_terms(self, text: str) -> str:
        """Substitutes all pre-compiled tech tools and corporate slang."""
        # 1. Tech tools
        for word, phonetic in self.tech_tools.items():
            pattern = rf"\b{re.escape(word)}\b"
            text = re.sub(pattern, phonetic, text, flags=re.IGNORECASE)

        # 2. Corporate slang
        for word, phonetic in self.corporate_slang.items():
            pattern = rf"\b{re.escape(word)}\b"
            text = re.sub(pattern, phonetic, text, flags=re.IGNORECASE)

        # 3. Everyday Hinglish loanwords
        for word, phonetic in self.hinglish_words.items():
            pattern = rf"\b{re.escape(word)}\b"
            text = re.sub(pattern, phonetic, text, flags=re.IGNORECASE)

        # 3. Consonant cluster splits
        for word, phonetic in self.cluster_splits.items():
            pattern = rf"\b{re.escape(word)}\b"
            text = re.sub(pattern, phonetic, text)

        return text

    def normalize_units_and_currency(self, text: str) -> str:
        """Normalizes numbers, metrics, and currency with scale multipliers."""
        for pattern, replacement in self.scale_multipliers:
            text = re.sub(pattern, replacement, text)
        return text

    def normalize_pacing_and_breath(self, text: str) -> str:
        """Cleans unnatural micro-pauses that cause stutters and pitch resets."""
        text = re.sub(r",\s*,+", ",", text)
        text = re.sub(r"\.{2,}", "।", text)
        text = re.sub(r"!+", "!", text)
        text = re.sub(r"\?+", "?", text)
        text = re.sub(r"(?<!\d)\.(?!\d|[a-zA-Z])", "।", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"([,।!?])([^\s])", r"\1 \2", text)
        return text

    def roman_to_devanagari_word(self, word: str) -> str:
        """Syllabic fallback converter for uncataloged Roman words."""
        consonants = {
            'kh': 'ख', 'gh': 'घ', 'ch': 'च', 'chh': 'छ', 'jh': 'झ', 'th': 'थ', 'dh': 'ध',
            'ph': 'फ', 'bh': 'भ', 'sh': 'श', 'shh': 'ष', 'zh': 'ज़',
            'k': 'क', 'g': 'ग', 'j': 'ज', 't': 'त', 'd': 'द', 'n': 'न', 'p': 'प', 'f': 'फ',
            'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'w': 'व', 's': 'स',
            'h': 'ह', 'z': 'ज़', 'q': 'क', 'x': 'क्स'
        }
        vowels_initial = {
            'aa': 'आ', 'ee': 'ई', 'oo': 'ऊ', 'ai': 'ऐ', 'au': 'औ',
            'a': 'अ', 'i': 'इ', 'u': 'उ', 'e': 'ए', 'o': 'ओ'
        }
        vowels_matra = {
            'aa': 'ा', 'ee': 'ी', 'oo': 'ू', 'ai': 'ै', 'au': 'ौ',
            'a': '', 'i': 'ि', 'u': 'ु', 'e': 'े', 'o': 'ो'
        }
        w = word.lower()
        out = []
        i = 0
        n = len(w)
        prev_was_consonant = False
        while i < n:
            if i + 3 <= n and w[i:i+3] in consonants:
                out.append(consonants[w[i:i+3]])
                prev_was_consonant = True
                i += 3
            elif i + 2 <= n and w[i:i+2] in consonants:
                out.append(consonants[w[i:i+2]])
                prev_was_consonant = True
                i += 2
            elif w[i] in consonants:
                out.append(consonants[w[i]])
                prev_was_consonant = True
                i += 1
            elif i + 2 <= n and w[i:i+2] in vowels_matra:
                v = w[i:i+2]
                out.append(vowels_matra[v] if prev_was_consonant else vowels_initial[v])
                prev_was_consonant = False
                i += 2
            elif w[i] in vowels_matra:
                v = w[i]
                out.append(vowels_matra[v] if prev_was_consonant else vowels_initial[v])
                prev_was_consonant = False
                i += 1
            else:
                out.append(w[i])
                prev_was_consonant = False
                i += 1
        return ''.join(out)

    def transliterate_residual_latin(self, text: str) -> str:
        """Ensures that 0% Latin characters remain in the output speech text."""
        def replace_token(match):
            token = match.group(0)
            return self.roman_to_devanagari_word(token)
        return re.sub(r"\b[a-zA-Z]{2,}\b", replace_token, text)

    def normalize_hinglish_to_devanagari(self, text: str) -> str:
        """
        Transliterates Roman Hindi / Hinglish grammatical words into pure Devanagari.
        Eliminates the dangerous script-switching boundary (Latin <-> Devanagari)
        that causes Microsoft Edge-TTS neural models to hesitate, stutter, and reset pitch.
        """
        for word, devanagari in self.grammar_words.items():
            pattern = rf"\b{re.escape(word)}\b"
            text = re.sub(pattern, devanagari, text, flags=re.IGNORECASE)
        # Apply final residual fallback
        text = self.transliterate_residual_latin(text)
        return text

    def normalize_all(self, text: str) -> str:
        """
        Executes the master normalization pipeline in strict logical order:
        1. Contextual Homographs (resolves 'use' / 'to' / 'mat')
        2. Numbers, Currency & Multipliers ($10k, 512MB, 10x)
        3. Lexicon Terms (Tech & Corporate dictionary, Hinglish loanwords)
        4. Algorithmic Zero-Shot Acronym Expander (handles ANY unknown uppercase term)
        5. Universal Roman Hindi to Pure Devanagari Transliteration
        6. Devanagari Consonant Cluster Boundary Splits
        7. Prosodic Breath & Pacing Normalization
        """
        # Step 1: Homographs
        text = self.normalize_homographs(text)

        # Step 2: Numbers, Currencies, Multipliers
        text = self.normalize_units_and_currency(text)

        # Step 3: Lexicon Matches (Tech, Corporate & Conversational Loanwords)
        text = self.normalize_lexicon_terms(text)

        # Step 4: Algorithmic Zero-Shot Acronym Expander for unknown terms!
        text = self.normalize_dynamic_acronyms(text)

        # Step 5: Roman Hindi Grammar to Pure Devanagari (Stutter & Script-Switching Elimination)
        text = self.normalize_hinglish_to_devanagari(text)

        # Step 6: Consonant Clusters in Devanagari
        for word, phonetic in self.cluster_splits.items():
            text = re.sub(rf"\b{re.escape(word)}\b", phonetic, text)

        # Step 7: Pacing & Breath Units
        text = self.normalize_pacing_and_breath(text)

        return text

    @staticmethod
    def get_voice_profile(role: str = "explainer") -> Dict[str, Any]:
        profiles = {
            "senior_mentor": {
                "voice": "Charon",
                "role_desc": "Senior Architect: Calm, authoritative, crystal articulation",
            },
            "junior_dev": {
                "voice": "Puck",
                "role_desc": "Junior Dev: Expressive, relatable, eager to learn",
            },
            "female_lead": {
                "voice": "Kore",
                "role_desc": "Female Lead: Confident, engaging, warm modern cadence",
            },
            "dramatic_narrator": {
                "voice": "Fenrir",
                "role_desc": "Cinematic & Intense Narrator",
            },
            "storyteller": {
                "voice": "Aoede",
                "role_desc": "Expressive Storyteller & Creative Narrator",
            },
        }
        return profiles.get(role, profiles["junior_dev"])


# Singleton instance
default_normalizer = PhoneticNormalizer()


def normalize_text_for_speech(text: str) -> str:
    return default_normalizer.normalize_all(text)


if __name__ == "__main__":
    normalizer = PhoneticNormalizer()
    test_suite = [
        # 1. Unknown Acronyms never explicitly coded (Zero-shot test)
        "Maine naya VPC banaya aur usme JWT authentication aur CORS enable kiya.",
        "Company ka KPI aur OKR meet nahi hua toh CEO ne layoff announce kar diya.",
        "B2B SaaS startup ne $50k ka seed round raise kiya aur MRR 10x badha diya.",
        # 2. Corporate & Hindi Hybrid
        "Arjun ka appraisal meeting tha, manager ne bola bandwidth kam hai aur CTC freeze hai.",
        "Use bolo ki pull request review kare aur standup meeting me blockers bataye.",
        # 3. Cluster & Homograph
        "Agar subscription expire ho gaya toh use dobara mat khareedo, pehle architecture samjho.",
    ]

    print("=== Master AI Enterprise Phonetic Normalizer v2.1.0 ===")
    for s in test_suite:
        print(f"\n[INPUT]:  {s}")
        print(f"[OUTPUT]: {normalizer.normalize_all(s)}")
