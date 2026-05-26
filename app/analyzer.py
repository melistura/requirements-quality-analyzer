import re

def split_sentences(text: str):
    # Önce tüm metni normalize edelim
    text = text.strip()

    # Nokta, ünlem, soru işareti ve satır sonlarına göre böl
    sentences = re.split(r'[.\n!?]+', text)

    # Boşları temizle
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences

def classify_requirement(sentence: str):
    sentence_lower = sentence.lower()

    nfr_keywords = [
        "hızlı",
        "güvenli",
        "performans",
        "kullanılabilir",
        "kullanılabilirlik",
        "ölçeklenebilir",
        "erişilebilir",
        "erişilebilirlik",
        "kararlı",
        "stabil",
        "dayanıklı",
        "uyumlu",
        "uyumluluk",
        "gizlilik",
        "mahremiyet",
        "verimli",
        "verimlilik",
        "response time",
        "yanıt süresi",
        "tepki süresi",
        "availability",
        "uptime",
        "latency",
        "throughput",
        "reliable",
        "secure",
        "fast",
        "performance",
        "scalable",
        "usability",
        "accessibility",
        "privacy",
        "maintainable",
        "maintainability",
        "availability",
        "fault tolerant",
        "interoperability"
    ]

    constraint_keywords = [
        "zorunlu",
        "zorundadır",
        "olmalıdır",
        "gereklidir",
        "gerekir",
        "uygun olmalıdır",
        "must",
        "required",
        "shall",
        "has to",
        "kvkk",
        "gdpr",
        "iso",
        "mevzuat",
        "yasal",
        "regülasyon",
        "standarda uygun",
        "standartlara uygun",
        "uyumluluk gereği",
        "yalnızca",
        "sadece",
        "en az",
        "en fazla"
    ]

    fr_keywords = [
        "giriş yap",
        "kayıt ol",
        "listele",
        "görüntüle",
        "oluştur",
        "sil",
        "güncelle",
        "ekle",
        "indir",
        "yükle",
        "ara",
        "filtrele",
        "raporla",
        "hesapla",
        "doğrula",
        "gönder",
        "al",
        "kaydet",
        "giriş yapabil",
        "çıkış yapabil",
        "ödeme yap",
        "şifre sıfırla",
        "giriş yapabilmelidir",
        "görüntüleyebilmelidir",
        "oluşturabilmelidir",
        "güncelleyebilmelidir",
        "silebilmelidir",
        "ekleyebilmelidir",
        "yapabilmelidir",
        "can log in",
        "can view",
        "can create",
        "can update",
        "can delete",
        "can upload",
        "can download",
        "can search",
        "can filter"
    ]

    nfr_score = sum(1 for keyword in nfr_keywords if keyword in sentence_lower)
    constraint_score = sum(1 for keyword in constraint_keywords if keyword in sentence_lower)
    fr_score = sum(1 for keyword in fr_keywords if keyword in sentence_lower)

    if constraint_score > 0:
        return "Non-Functional Requirement"

    if nfr_score > 0:
        return "Non-Functional Requirement"

    if fr_score > 0:
     return "Functional Requirement"

    return "Functional Requirement"




def detect_ambiguity(sentence: str):
    ambiguity_words = [
        "hızlı",
        "kolay",
        "güvenli",
        "kullanıcı dostu",
        "etkili",
        "iyi",
        "uygun",
        "optimal",
        "modern",
        "esnek",
        "başarılı",
        "güçlü",
        "yüksek performanslı",
        "sorunsuz",
        "stabil",
        "kararlı",
        "anlaşılır",
        "basit",
        "makul",
        "yeterli",
        "minimum",
        "maksimum",
        "short",
        "easy",
        "user-friendly",
        "efficient",
        "appropriate",
        "good",
        "optimal",
        "robust"
    ]

    found_words = [word for word in ambiguity_words if word in sentence.lower()]
    return found_words


def evaluate_quality(sentence: str, ambiguity_words: list):
    issues = []
    suggestions = []

    

    if ambiguity_words:
        issues.append("Muğlak ifade içeriyor.")
        suggestions.append("Daha ölçülebilir ve açık bir ifade kullanılması önerilir.")

    if len(sentence.split()) < 3:
        issues.append("Cümle çok kısa olabilir.")
        suggestions.append("Gereksinim daha açıklayıcı biçimde yazılabilir.")

    if "ve" in sentence.lower() and len(sentence.split()) > 8:
        issues.append("Birden fazla gereksinim tek cümlede ifade edilmiş olabilir.")
        suggestions.append("Gereksinimler ayrı cümlelere bölünebilir.")

    if not issues:
        quality = "İyi"
        suggestion = "Sorun tespit edilmedi."
    elif len(issues) == 1:
        quality = "Orta"
        suggestion = suggestions[0]
    else:
        quality = "Düşük"
        suggestion = " ; ".join(suggestions)

    return quality, issues, suggestion


def analyze_requirements(text: str):
    sentences = split_sentences(text)
    results = []

    for sentence in sentences:
        req_type = classify_requirement(sentence)
        ambiguity_words = detect_ambiguity(sentence)
        quality, issues, suggestion = evaluate_quality(sentence, ambiguity_words)

        results.append(
            {
                "sentence": sentence,
                "type": req_type,
                "ambiguity_words": ambiguity_words,
                "quality": quality,
                "issues": issues,
                "suggestion": suggestion,
            }
        )

    return results